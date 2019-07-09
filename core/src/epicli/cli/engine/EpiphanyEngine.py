
import os
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.build_saver import save_manifest
from cli.helpers.yaml_helpers import safe_load_all
from cli.helpers.Log import Log
from cli.helpers.provider_class_loader import provider_class_loader
from cli.engine.DefaultMerger import DefaultMerger
from cli.engine.SchemaValidator import SchemaValidator
from cli.engine.ConfigurationAppender import ConfigurationAppender
from cli.engine.TerraformTemplateGenerator import TerraformTemplateGenerator
from cli.engine.TerraformRunner import TerraformRunner
from cli.engine.AnsibleRunner import AnsibleRunner


class EpiphanyEngine:
    def __init__(self, input_data):
        self.file = input_data.file
        self.skip_infrastructure = input_data.no_infra if hasattr(input_data, 'no_infra') else False
        self.logger = Log(__name__)

        self.cluster_model = None
        self.input_docs = []
        self.configuration_docs = []
        self.infrastructure_docs = []


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def process_input_docs(self):
        # Load the user input YAML docs from the input file.
        if os.path.isabs(self.file):
            path_to_load = self.file
        else:
            path_to_load = os.path.join(os.getcwd(), self.file)
        user_file_stream = open(path_to_load, 'r')
        self.input_docs = safe_load_all(user_file_stream)

        # Merge the input docs with defaults
        with DefaultMerger(self.input_docs) as doc_merger:
            self.input_docs = doc_merger.run()

        # Get the cluster model.
        self.cluster_model = select_single(self.input_docs, lambda x: x.kind == 'epiphany-cluster')
        if self.cluster_model is None:
            raise Exception('No cluster model defined in input YAML file')

        # Validate input documents
        with SchemaValidator(self.cluster_model, self.input_docs) as schema_validator:
            schema_validator.run()

    def process_infrastructure_docs(self):
        # Build the infrastructure docs
        with provider_class_loader(self.cluster_model.provider, 'InfrastructureBuilder')(
                self.input_docs) as infrastructure_builder:
            self.infrastructure_docs = infrastructure_builder.run()

        # Validate infrastructure documents
        with SchemaValidator(self.cluster_model, self.infrastructure_docs) as schema_validator:
            schema_validator.run()

    def process_configuration_docs(self):
        # Append with components and configuration docs
        with ConfigurationAppender(self.input_docs) as config_appender:
            self.configuration_docs = config_appender.run()

        # Validate configuration documents
        with SchemaValidator(self.cluster_model, self.configuration_docs) as schema_validator:
            schema_validator.run()

    def collect_infrastructure_config(self):
        with provider_class_loader(self.cluster_model.provider, 'InfrastructureConfigCollector')(
                [*self.input_docs, *self.configuration_docs, *self.infrastructure_docs]) as config_collector:
            config_collector.run()

    def verify(self):
        try:
            self.process_input_docs()

            self.process_configuration_docs()

            self.process_infrastructure_docs()

            save_manifest([*self.input_docs, *self.configuration_docs, *self.infrastructure_docs], self.cluster_model.specification.name)

            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True) #TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1

    def apply(self):
        try:
            self.process_input_docs()

            self.process_infrastructure_docs()

            if not self.skip_infrastructure:
                # Generate terraform templates
                with TerraformTemplateGenerator(self.cluster_model, self.infrastructure_docs) as template_generator:
                    template_generator.run()

                # Run Terraform to create infrastructure
                with TerraformRunner(self.cluster_model.specification.name) as tf_runner:
                    tf_runner.run()

            self.process_configuration_docs()

            self.collect_infrastructure_config()

            # Run Ansible to provision infrastructure
            docs = [*self.input_docs, *self.configuration_docs, *self.infrastructure_docs]
            with AnsibleRunner(self.cluster_model, docs) as ansible_runner:
                ansible_runner.run()

            # Save docs to manifest file
            save_manifest(docs, self.cluster_model.specification.name)

            return 0
        except Exception as e:
            self.logger.error(e, exc_info=True)  # TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            return 1

    def dry_run(self):

        self.process_input_docs()

        self.process_configuration_docs()

        return [*self.input_docs, *self.configuration_docs]

