import os
import sys

from cli.src.ansible.AnsibleRunner import AnsibleRunner
from cli.src.helpers.build_io import (get_build_path, get_inventory_path,
                                      get_manifest_path, load_inventory,
                                      load_manifest, save_manifest)
from cli.src.helpers.cli_helpers import query_yes_no
from cli.src.helpers.data_loader import load_schema_obj, types
from cli.src.helpers.doc_list_helpers import (select_all, select_first,
                                              select_single)
from cli.src.helpers.naming_helpers import get_os_name_normalized
from cli.src.helpers.yaml_helpers import safe_load_all
from cli.src.Log import Log
from cli.src.providers.provider_class_loader import provider_class_loader
from cli.src.schema.ConfigurationAppender import ConfigurationAppender
from cli.src.schema.DefaultMerger import DefaultMerger
from cli.src.schema.SchemaValidator import SchemaValidator
from cli.src.Step import Step
from cli.src.terraform.TerraformRunner import TerraformRunner
from cli.version import VERSION


class Apply(Step):
    def __init__(self, input_data):
        super().__init__(__name__)
        self.logger = Log(__name__)
        self.file = input_data.file
        self.skip_infrastructure = getattr(input_data, 'no_infra', False)
        self.skip_config = getattr(input_data, 'skip_config', False)
        self.ansible_options = {'forks': getattr(input_data, 'ansible_forks'),
                                'profile_tasks': getattr(input_data, 'profile_ansible_tasks', False)}
        self.ping_retries: int = input_data.ping_retries

        self.input_docs = []
        self.manifest_docs = []
        self.inventory = None

        self.cluster_model = None
        self.cluster_name = ''
        self.configuration_docs = []
        self.infrastructure_docs = []
        self.all_docs = []


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        pass


    def load_documents(self):
        # Load the input docs from the input
        if os.path.isabs(self.file):
            path_to_load = self.file
        else:
            path_to_load = os.path.join(os.getcwd(), self.file)
        user_file_stream = open(path_to_load, 'r')
        self.input_docs = safe_load_all(user_file_stream)

        # Get the cluster model and name
        self.cluster_model = select_single(self.input_docs, lambda x: x.kind == 'epiphany-cluster')
        if self.cluster_model is None:
            raise Exception('No cluster model defined in input YAML file')
        self.cluster_name = self.cluster_model.specification.name

        # Load possible manifest when doing a re-apply
        path_to_manifest = get_manifest_path(self.cluster_name)
        if os.path.isfile(path_to_manifest):
            self.manifest_docs = load_manifest(get_build_path(self.cluster_name))

        # Load possible inventory when doing re-apply
        path_to_inventory = get_inventory_path(self.cluster_name)
        if os.path.isfile(path_to_inventory):
            self.inventory = load_inventory(path_to_inventory)


    def process_documents(self):
        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

        # Update cluster model after merging
        self.cluster_model = select_single(self.input_docs, lambda x: x.kind == 'epiphany-cluster')

        # Validate cluster model.
        with SchemaValidator(self.cluster_model.provider, [self.cluster_model]) as schema_validator:
            schema_validator.run()

         # Build the infrastructure docs
        with provider_class_loader(self.cluster_model.provider, 'InfrastructureBuilder')(
                self.input_docs, self.manifest_docs) as infrastructure_builder:
            self.infrastructure_docs = infrastructure_builder.run()

        # Append with components and configuration docs
        with ConfigurationAppender(self.input_docs) as config_appender:
            self.configuration_docs = config_appender.run()

        # Merge all documents to a single list
        self.all_docs = [*self.configuration_docs, *self.infrastructure_docs]


    def validate_documents(self):
        # Validate all documents documents
        with SchemaValidator(self.cluster_model.provider, self.all_docs) as schema_validator:
            schema_validator.run()

        # Some other general checks we should add with advanced schema validation later
        self.assert_no_master_downscale()
        self.assert_no_postgres_nodes_number_change()
        self.assert_compatible_terraform()
        self.assert_consistent_os_family()

        # Save manifest as we have all information for Terraform apply
        save_manifest(self.all_docs, self.cluster_name)


    def run_terraform(self):
        if  self.skip_infrastructure or self.cluster_model['provider'] == 'any':
            return

        # Run Terraform to create infrastructure
        with TerraformRunner(self.cluster_model, self.infrastructure_docs) as tf_runner:
            tf_runner.apply()


    def collect_infrastructure_config(self):
        with provider_class_loader(self.cluster_model.provider, 'InfrastructureConfigCollector')(self.all_docs) as config_collector:
            config_collector.run()

        # Save manifest again as we have some new information for Ansible apply
        save_manifest(self.all_docs, self.cluster_name)


    def run_ansible(self):
        if self.skip_config:
            return

        with AnsibleRunner(self.cluster_model, self.all_docs, ansible_options=self.ansible_options,
                            ping_retries=self.ping_retries) as ansible_runner:
            ansible_runner.apply()


    def apply(self):
        self.load_documents()

        self.process_documents()

        self.validate_documents()

        self.run_terraform()

        self.collect_infrastructure_config()

        self.run_ansible()

        return 0


    # NOTE: All asserts below should eventually be replaced/removed with advanced
    # configuration validation or fixes made to the affected components.

    def assert_compatible_terraform(self):
        if self.skip_infrastructure:
            return

        cluster_model = select_first(self.manifest_docs, lambda x: x.kind == 'epiphany-cluster')
        if cluster_model:
            old_major_version = int(cluster_model.version.split('.')[0])
            new_major_version = int(VERSION.split('.')[0])
            if old_major_version == 1 and new_major_version == 2:
                if not query_yes_no("You are trying to re-apply a Epiphany 2.x configuration against an existing Epiphany 1.x cluster."
                                    "The Terraform is not compatible between these versions and requires manual action described in the documentation."
                                    "If you haven't done Terraform upgrade yet, it will break your cluster. Do you want to continue?"):
                    sys.exit(0)


    def assert_consistent_os_family(self):
        virtual_machine_docs = select_all(
            self.infrastructure_docs,
            lambda x: x.kind == 'infrastructure/virtual-machine',
        )

        os_indicators = {
            get_os_name_normalized(vm_doc)
            for vm_doc in virtual_machine_docs
        }

        if len(os_indicators) > 1:
            raise Exception("Detected mixed Linux distros in config, Epirepo will not work properly. Please inspect your config manifest. Forgot to define repository VM document?")


    def assert_no_master_downscale(self):
        components = self.cluster_model.specification.components

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


    def assert_no_postgres_nodes_number_change(self):
        feature_mapping = select_first(self.input_docs, lambda x: x.kind == 'configuration/feature-mapping')
        if feature_mapping:
            with DefaultMerger([feature_mapping]) as doc_merger:
                feature_mapping = doc_merger.run()
            feature_mapping = feature_mapping[0]
        else:
            feature_mapping = load_schema_obj(types.DEFAULT, 'common', 'configuration/feature-mapping')

        components = self.cluster_model.specification.components
        if self.inventory:
            next_postgres_node_count = 0
            prev_postgres_node_count = len(self.inventory.list_hosts(pattern='postgresql'))
            postgres_available = [x for x in feature_mapping.specification.available_roles if x.name == 'postgresql']
            if postgres_available[0].enabled:
                for key, roles in feature_mapping.specification.roles_mapping.items():
                    if ('postgresql') in roles and key in components:
                        next_postgres_node_count = next_postgres_node_count + components[key].count

            if prev_postgres_node_count > 0 and prev_postgres_node_count != next_postgres_node_count:
                    raise Exception("Postgresql scaling is not supported yet. Please revert your 'postgresql' node count to previous value.")
