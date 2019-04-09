
import os
import logging
import sys
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.build_saver import save_manifest
from cli.helpers.yaml_helpers import safe_load_all
from cli.helpers.Log import Log
from cli.helpers.provider_class_loader import provider_class_loader
from cli.engine.DefaultMerger import DefaultMerger
from cli.engine.SchemaValidator import SchemaValidator
from cli.engine.ConfigurationAppender import ConfigurationAppender
from cli.engine.TemplateGenerator import TemplateGenerator
from cli.engine.TerraformRunner import TerraformRunner
from cli.engine.AnsibleRunner import AnsibleRunner


class EpiphanyEngine:
    def __init__(self, input_data):
        self.file_path = input_data.file
        # Todo: set the context from the commandline
        # self.context = input_data.context
        # Todo: set log level from cmdline
        Log.setup_logging(logging.INFO)
        self.logger = Log.get_logger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        try:
            # Load the user input YAML docs from the input file
            if os.path.isabs(self.file_path):
                path_to_load = self.file_path
            else:
                path_to_load = os.path.join(os.getcwd(), self.file_path)
            user_file_stream = open(path_to_load, 'r')
            docs = safe_load_all(user_file_stream)

            # Merge the input docs with defaults
            with DefaultMerger(docs) as doc_merger:
                docs = doc_merger.run()

            # TODO For now we only except input YALMs which provide a epiphany-cluster model kind.
            cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')
            if cluster_model is None:
                raise Exception('No cluster model defined in input YAML file')

            # Validate input documents
            with SchemaValidator(cluster_model, docs) as schema_validator:
                schema_validator.run()

            # Build the infrastructure docs
            with provider_class_loader(cluster_model.provider, 'InfrastructureBuilder')() as infrastructure_builder:
                infrastructure = infrastructure_builder.run(cluster_model, docs)

            # Append with components and configuration docs
            with ConfigurationAppender(cluster_model, docs) as config_appender:
                config_appender.run()

            # Merge component configurations with infrastructure
            docs = [*docs, *infrastructure]

            # Validate generated documents.
            with SchemaValidator(cluster_model, docs) as schema_validator:
                schema_validator.run()

            # Save docs to manifest file
            save_manifest(docs, cluster_model.specification.name)

            # Generate terraform templates
            with TemplateGenerator(cluster_model, infrastructure) as template_generator:
                template_generator.run()

            # Run Terraform to create infrastructure
            with TerraformRunner(cluster_model) as tf_runner:
                tf_runner.run()

            # Run Ansible to provision infrastructure
            with AnsibleRunner(cluster_model, docs) as ansible_runner:
                ansible_runner.run()
        except Exception as e:
            self.logger.error(e, exc_info=True) #TODO extensive debug output might not always be wanted. Make this configurable with input flag?
            sys.exit(1)




