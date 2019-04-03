import os
import logging
from cli.helpers.objdict_helpers import dict_to_objdict
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.build_saver import save_build
from cli.helpers.yaml_helpers import safe_load_all
from cli.helpers.Log import Log
from cli.helpers.provider_class_loader import provider_class_loader
from cli.engine.DefaultMerger import DefaultMerger
from cli.engine.SchemaValidator import SchemaValidator
from cli.engine.ConfigurationAppender import ConfigurationAppender
from cli.engine.AnsibleRunner import AnsibleRunner
from cli.engine.TerraformRunner import TerraformRunner


class EpiphanyEngine:
    def __init__(self, input_data):
        # todo se output dir from cmdline
        self.OUTPUT_FOLDER_PATH = os.path.join( os.path.dirname(__file__), '../../output/')
        if not os.path.exists(self.OUTPUT_FOLDER_PATH):
            os.makedirs(self.OUTPUT_FOLDER_PATH)
        self.file_path = input_data.file
        self.context = input_data.context
        # todo set log level from cmdline
        Log.setup_logging(logging.INFO)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
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

        cluster_model = select_single(docs, lambda x: x.kind == 'epiphany-cluster')

        # Build the infrastructure docs
        with provider_class_loader(cluster_model.provider, 'InfrastructureBuilder')() as infrastructure_builder:
            infrastructure = infrastructure_builder.run(cluster_model, docs)

        # Append with components and configuration docs
        with ConfigurationAppender(cluster_model, docs) as config_appender:
            config_appender.run()

        # Merge component configurations with infrastructure and save to manifest
        docs = [*docs, *infrastructure]

        # Save docs to manifest file
        save_build(docs, cluster_model.specification.name)

        # Validate docs
        with SchemaValidator(cluster_model, docs) as schema_validator:
            schema_validator.run()

        # Run Terraform to provision infrastructure
        terraform_build_directory = os.path.join(self.OUTPUT_FOLDER_PATH, cluster_model.specification.name, 'terraform')
        with TerraformRunner(terraform_build_directory, cluster_model, infrastructure) as tf_runner:
            tf_runner.run()

        # Run Ansible to provision infrastructure
        with AnsibleRunner(dict_to_objdict(cluster_model), docs) as ansible_runner:
            ansible_runner.run()




