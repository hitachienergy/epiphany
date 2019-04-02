import os
import importlib
from cli.helpers.objdict_helpers import dict_to_objdict
from cli.helpers.doc_list_helpers import select_single
from cli.helpers.build_saver import save_build
from cli.helpers.yaml_helpers import safe_load_all
from cli.engine.DefaultMerger import DefaultMerger
from cli.engine.SchemaValidator import SchemaValidator
from cli.engine.ConfigurationAppender import ConfigurationAppender
from cli.engine.AnsibleRunner import AnsibleRunner
from cli.engine.TerraformRunner import TerraformRunner


class EpiphanyEngine:
    def __init__(self, input_data):
        self.BUILD_FOLDER_PATH = '../../build/'
        self.file_path = input_data.file
        self.context = input_data.context

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

        cluster_model = select_single(docs, lambda x: x.kind == "epiphany-cluster")

        # Build the infrastructure docs
        with self.get_infrastructure_builder(cluster_model.provider)() as infrastructure_builder:
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

        # todo generate .tf files
        script_dir = os.path.dirname(__file__)
        terraform_build_directory = os.path.join(script_dir, self.BUILD_FOLDER_PATH, self.context, "terraform")

        # todo run terraform
        # todo set path to terraform files
        with TerraformRunner(terraform_build_directory, cluster_model, infrastructure) as tf_runner:
            tf_runner.run()

        # todo generate ansible inventory
        with AnsibleRunner(dict_to_objdict(cluster_model), docs) as ansible_runner:
            ansible_runner.run()

        # todo adjust ansible to new schema
        # todo run ansible

    @staticmethod
    def get_infrastructure_builder(provider):
        try:
            return getattr(importlib.import_module('cli.engine.' + provider.lower() + '.InfrastructureBuilder'), 'InfrastructureBuilder')
        except:
            raise Exception('No InfrastructureBuilder for ' + provider)



