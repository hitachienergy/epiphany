import os
import sys
from pathlib import Path

from cli.src.Config import Config
from cli.src.ansible.AnsibleRunner import AnsibleRunner
from cli.src.helpers.build_io import get_inventory_path, load_inventory
from cli.src.helpers.cli_helpers import query_yes_no
from cli.src.helpers.data_loader import load_schema_obj, schema_types
from cli.src.helpers.naming_helpers import get_os_name_normalized
from cli.src.Log import Log
from cli.src.providers.provider_class_loader import provider_class_loader
from cli.src.schema.ConfigurationAppender import ConfigurationAppender
from cli.src.schema.DefaultMerger import DefaultMerger
from cli.src.schema.ManifestHandler import ManifestHandler
from cli.src.schema.SchemaValidator import SchemaValidator
from cli.src.Step import Step
from cli.src.terraform.TerraformRunner import TerraformRunner
from cli.version import VERSION


class Apply(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.logger = Log(__name__)
        self.input_manifest = input_data.input_manifest
        self.skip_infrastructure = getattr(input_data, 'no_infra', False)
        self.skip_config = getattr(input_data, 'skip_config', False)
        self.ansible_options = {'forks': getattr(input_data, 'ansible_forks'),
                                'profile_tasks': getattr(input_data, 'profile_ansible_tasks', False)}
        self.ping_retries: int = input_data.ping_retries

        self.input_mhandler: ManifestHandler = ManifestHandler(input_file=Path(self.input_manifest))
        self.old_mhandler: ManifestHandler
        self.output_mhandler: ManifestHandler
        self.inventory = None

        self.cluster_name = ''

        Config().full_download = input_data.full_download
        Config().input_manifest_path = Path(self.input_manifest)

    def load_documents(self):
        # Load the input docs from the input manifest
        self.input_mhandler.read_manifest()

        # Check the cluster model and name
        try:
            self.input_mhandler.cluster_model
        except KeyError as ke:
            raise Exception('No cluster model defined in input YAML file') from ke

        # Load possible manifest when doing a re-apply
        self.old_mhandler = ManifestHandler(cluster_name=self.input_mhandler.cluster_name)
        if self.old_mhandler.exists():
            self.old_mhandler.read_manifest()

        # Load possible inventory when doing re-apply
        path_to_inventory = get_inventory_path(self.input_mhandler.cluster_name)
        if os.path.isfile(path_to_inventory):
            self.inventory = load_inventory(path_to_inventory)

    def process_documents(self):
        # Merge the input docs with defaults
        with DefaultMerger(self.input_mhandler.docs) as doc_merger:
            merged_docs = doc_merger.run()

        # Validate cluster model.
        with SchemaValidator(self.input_mhandler.cluster_model.provider, [self.input_mhandler.cluster_model]) as schema_validator:
            schema_validator.run()

        # Build the infrastructure docs
        with provider_class_loader(self.input_mhandler.cluster_model.provider, 'InfrastructureBuilder')(
                merged_docs, self.old_mhandler.docs) as infrastructure_builder:
            infra_docs = infrastructure_builder.run()

        # Append with components and configuration docs
        with ConfigurationAppender(merged_docs) as config_appender:
            config_docs = config_appender.run()

        self.output_mhandler = ManifestHandler(cluster_name=self.input_mhandler.cluster_name)
        self.output_mhandler.add_docs(config_docs)
        self.output_mhandler.add_docs(infra_docs)

    def validate_documents(self):
        # Validate all documents documents
        with SchemaValidator(self.output_mhandler.cluster_model.provider, self.output_mhandler.docs) as schema_validator:
            schema_validator.run()

        # Some other general checks we should add with advanced schema validation later
        self.assert_no_master_downscale()
        self.assert_no_postgres_nodes_number_change()
        self.assert_compatible_terraform()
        self.assert_consistent_os_family()

        # Save manifest as we have all information for Terraform apply
        self.output_mhandler.write_manifest()

    def apply_terraform(self):
        if  self.skip_infrastructure or self.output_mhandler.cluster_model['provider'] == 'any':
            return

        # Run Terraform to create infrastructure
        with TerraformRunner(self.output_mhandler.cluster_model, self.output_mhandler.infra_docs) as tf_runner:
            tf_runner.apply()

    def collect_infrastructure_config(self):
        if  self.output_mhandler.cluster_model['provider'] == 'any':
            return

        with provider_class_loader(self.output_mhandler.cluster_model.provider,
                                   'InfrastructureConfigCollector')(self.output_mhandler.docs) as config_collector:
            kube_doc = config_collector.run()
            if kube_doc:
                self.output_mhandler.update_doc(kube_doc)  # update kubernetes config doc

        # Save manifest again as we have some new information for Ansible apply
        self.output_mhandler.write_manifest()

    def apply_ansible(self):
        if self.skip_config:
            return

        with AnsibleRunner(self.output_mhandler.cluster_model, self.output_mhandler.docs, ansible_options=self.ansible_options,
                            ping_retries=self.ping_retries) as ansible_runner:
            ansible_runner.apply()

    def apply(self):
        self.load_documents()

        self.process_documents()

        self.validate_documents()

        self.apply_terraform()

        self.collect_infrastructure_config()

        self.apply_ansible()

        return 0

    # NOTE: All asserts below should eventually be replaced/removed with advanced
    # configuration validation or fixes made to the affected components.
    def assert_compatible_terraform(self):
        if self.skip_infrastructure:
            return

        cluster_model = self.output_mhandler.cluster_model
        if cluster_model:
            old_major_version = int(cluster_model.version.split('.')[0])
            new_major_version = int(VERSION.split('.')[0])
            if old_major_version == 1 and new_major_version == 2:
                if not query_yes_no("You are trying to re-apply a Epiphany 2.x configuration against an existing Epiphany 1.x cluster."
                                    "The Terraform is not compatible between these versions and requires manual action described in the documentation."
                                    "If you haven't done Terraform upgrade yet, it will break your cluster. Do you want to continue?"):
                    sys.exit(0)

    def assert_consistent_os_family(self):
        virtual_machine_docs = self.output_mhandler['infrastructure/virtual-machine']

        os_indicators = {
            get_os_name_normalized(vm_doc)
            for vm_doc in virtual_machine_docs
        }

        if len(os_indicators) > 1:
            raise Exception("Detected mixed Linux distros in config, Epirepo will not work properly. Please inspect your config manifest. Forgot to define repository VM document?")

    def assert_no_master_downscale(self):
        components = self.output_mhandler.cluster_model.specification.components

        # Skip downscale assertion for single machine clusters
        if ('single_machine' in components) and (int(components['single_machine']['count']) > 0):
            return

        if self.inventory:
            both_present = all([
                'kubernetes_master' in self.inventory.list_groups(),
                'kubernetes_master' in components,
            ])

            if both_present:
                prev_master_count = len(self.inventory.list_hosts(pattern='kubernetes_master'))
                next_master_count = int(components['kubernetes_master']['count'])

                if prev_master_count > next_master_count:
                    raise Exception("ControlPlane downscale is not supported yet. Please revert your 'kubernetes_master' count to previous value or increase it to scale up Kubernetes.")

    def __load_configuration_doc(self, kind: str) -> dict:
        doc = self.input_mhandler[kind]

        if doc:
            with DefaultMerger(doc) as doc_merger:
                return doc_merger.run()[0]
        else:
            return load_schema_obj(schema_types.DEFAULT, 'common', kind)


    def assert_no_postgres_nodes_number_change(self):
        feature_mappings = self.__load_configuration_doc('configuration/feature-mappings')
        features = self.__load_configuration_doc('configuration/features')

        components = self.output_mhandler.cluster_model.specification.components
        if self.inventory:
            next_postgres_node_count = 0
            prev_postgres_node_count = len(self.inventory.list_hosts(pattern='postgresql'))
            postgres_available = [x for x in features.specification.features if x.name == 'postgresql']
            if postgres_available[0].enabled:
                for key, features in feature_mappings.specification.mappings.items():
                    if ('postgresql') in features and key in components:
                        next_postgres_node_count = next_postgres_node_count + components[key].count

            if prev_postgres_node_count > 0 and prev_postgres_node_count != next_postgres_node_count:
                    raise Exception("Postgresql scaling is not supported yet. Please revert your 'postgresql' node count to previous value.")
