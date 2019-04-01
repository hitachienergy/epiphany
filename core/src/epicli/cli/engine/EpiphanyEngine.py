import os
from cli.helpers.objdict_helpers import merge_objdict, dict_to_objdict
from cli.helpers.doc_list_helpers import select_first, select_single
import cli.helpers.data_types as data_types
from cli.helpers.data_loader import load_data_file, load_all_data_files
from cli.helpers.build_saver import save_build
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.AWSConfigBuilder import AWSConfigBuilder
from cli.helpers.yaml_helpers import safe_load_all
from cli.modules.template_generator import TemplateGenerator
from cli.modules.terraform_runner.TerraformRunner import TerraformRunner
from engine.DocumentMerger import DocumentMerger
from engine.SchemaValidator import SchemaValidator
import cli.config.template_generator_config as template_generator_config
import cli.helpers.terraform_file_helper as terraform_file_helper
from cli.engine.AnsibleRunner import AnsibleRunner


class EpiphanyEngine:
    def __init__(self, input_data):
        self.BUILD_FOLDER_PATH = '../../build/'
        self.file_path = input_data.file
        self.context = input_data.context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self

    def run(self):
        # Load the user input YAML docs from the input file
        if os.path.isabs(self.file_path):
            path_to_load = self.file_path
        else:
            path_to_load = os.path.join(os.getcwd(), self.file_path)
        user_file_stream = open(path_to_load, 'r')
        docs = safe_load_all(user_file_stream)

        # Merge the input docs with defaults
        with DocumentMerger() as doc_merger:
            docs = doc_merger.merge(docs)

        cluster_model = select_single(docs, lambda x: x.kind == "epiphany-cluster")

        # Build the infrastucture docs
        infrastructure_builder = self.get_infrastructure_builder_for_provider(cluster_model.provider)
        infrastructure = infrastructure_builder.build(cluster_model, docs)

        for component_key, component_value in cluster_model.specification.components.items():
            if component_value.count < 1:
                continue
            self.append_component_configuration(docs, component_key, component_value)

        result = docs + infrastructure
        save_build(result, cluster_model.specification.name)

        with SchemaValidator() as schema_validator:
            schema_validator.validate(result, cluster_model.provider)
        return

        # todo generate .tf files
        script_dir = os.path.dirname(__file__)
        terraform_build_directory = os.path.join(script_dir, self.BUILD_FOLDER_PATH, self.context, "terraform")

        terraform_file_helper.create_terraform_output_dir(terraform_build_directory)

        template_generator = TemplateGenerator.TemplateGenerator()

        terraform_file_helper.generate_terraform_file([cluster_model], template_generator,
                                                      template_generator_config, terraform_build_directory)

        terraform_file_helper.generate_terraform_file(infrastructure, template_generator, template_generator_config,
                                                      terraform_build_directory)

        # todo run terraform
        # todo set path to terraform files
        tf = TerraformRunner(terraform_build_directory)
        tf.init()
        tf.plan()
        tf.apply(auto_approve=True)

        # todo validate
        print("Running ansible.")
        # todo generate ansible inventory
        with AnsibleRunner(dict_to_objdict(cluster_model), result) as runner:
            runner.run()

        # todo adjust ansible to new schema
        # todo run ansible

    @staticmethod
    def get_infrastructure_builder_for_provider(provider):
        if provider.lower() == "aws":
            return AWSConfigBuilder()
        elif provider.lower() == "azure":
            return AWSConfigBuilder()
        else:
            raise NotImplementedError()


    @staticmethod
    def append_component_configuration(docs, component_key, component_value):

        features_map = select_first(docs, lambda x: x.kind == 'configuration/feature-mapping')
        if features_map is None:
            features_map = load_data_file(data_types.DEFAULT, 'common', 'configuration/feature-mapping')
            docs.append(features_map)
        config_selector = component_value.configuration
        for feature_key in features_map.specification[component_key]:
            config = select_first(docs,
                                  lambda x: x.kind == 'configuration/' + feature_key and x.name == config_selector)
            if config is None:
                config = merge_with_defaults('common', 'configuration/' + feature_key, config_selector)
            docs.append(config)
