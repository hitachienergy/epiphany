import yaml
import os
import cli.models.data_file_consts as model_constants
import cli.config.template_generator_config as template_generator_config
from cli.engine.dict_merge import merge_dict
from cli.helpers.list_helpers import select_first
from cli.helpers.defaults_loader import load_file_from_defaults, load_all_docs_from_defaults
from cli.helpers.build_saver import save_build
from cli.helpers.config_merger import merge_with_defaults
from cli.engine.aws.AWSConfigBuilder import AWSConfigBuilder
from cli.modules.template_generator import TemplateGenerator

from cli.modules.terraform_runner.TerraformRunner import TerraformRunner


class EpiphanyEngine:

    def __init__(self, input_data):

        self.BUILD_FOLDER_PATH = '../../build/'

        self.file_path = input_data.file
        self.context = input_data.context

    def __enter__(self):
        return self

    def run(self):
        docs = self.merge_with_user_input_with_defaults()
        cluster_model = self.find_document(docs, "kind", "epiphany-cluster")
        infrastructure_builder = self.get_infrastructure_builder_for_provider(cluster_model["provider"])
        infrastructure = infrastructure_builder.build(cluster_model, docs)

        for component_key, component_value in cluster_model["specification"]["components"].items():
            if component_value["count"] < 1:
                continue
            self.append_component_configuration(docs, component_key, component_value, cluster_model)

        result = docs + infrastructure
        save_build(result, self.context)

        # todo generate .tf files
        script_dir = os.path.dirname(__file__)
        terraform_build_directory = os.path.join(script_dir, self.BUILD_FOLDER_PATH, self.context, "terraform")

        if not os.path.exists(terraform_build_directory):
            os.makedirs(terraform_build_directory)

        template_generator = TemplateGenerator.TemplateGenerator()

        for document in result:
            yaml_document = yaml.load(str(document))

            if yaml_document["kind"] != "epiphany-cluster":
                content = template_generator.generate_terraform_file_content(document=yaml_document,
                                                                             templates_paths=
                                                                             template_generator_config.
                                                                             templates_paths)

                terraform_output_file_path = os.path.join(terraform_build_directory, yaml_document["name"] + ".tf")
                print(terraform_output_file_path)

                with open(terraform_output_file_path, 'w') as terraform_output_file:
                    terraform_output_file.write(content)

        # todo run terraform
        # todo set path to terraform files
        print(terraform_build_directory)
        tf = TerraformRunner(terraform_build_directory)
        tf.init()
        tf.plan()
        tf.apply(auto_approve=True)

        # todo validate

        # todo generate ansible inventory
        # todo adjust ansible to new schema
        # todo run ansible

    def merge_with_user_input_with_defaults(self):
        if os.path.isabs(self.file_path):
            path_to_load = self.file_path
        else:
            path_to_load = os.path.join(os.getcwd(), self.file_path)

        user_file_stream = open(path_to_load, 'r')
        user_yaml_files = yaml.safe_load_all(user_file_stream)

        state_docs = list()

        for user_file_yaml in user_yaml_files:
            files = load_all_docs_from_defaults(user_file_yaml[model_constants.PROVIDER],
                                                user_file_yaml[model_constants.KIND])
            file_with_defaults = select_first(files, lambda x: x[model_constants.NAME] == "default")
            merge_dict(file_with_defaults, user_file_yaml)
            state_docs.append(file_with_defaults)

        return state_docs

    def __exit__(self, exc_type, exc_value, traceback):
        print("close")

    @staticmethod
    def find_document(documents, field_name, value):
        if documents is not None:
            matches = list(filter(lambda x: x[field_name] == value, documents))
            if len(matches) > 0:
                return matches[0]
        return None

    @staticmethod
    def get_infrastructure_builder_for_provider(provider):
        if provider.lower() == "aws":
            return AWSConfigBuilder()

    @staticmethod
    def append_component_configuration(docs, component_key, component_value, cluster_model):

        features_map = select_first(docs, lambda x: x[model_constants.KIND] == 'configuration/feature-mapping')
        if features_map is None:
            features_map = load_file_from_defaults(cluster_model[model_constants.PROVIDER],
                                                   'configuration/feature-mapping')
        config_selector = component_value["configuration"]
        for feature_key in features_map["specification"][component_key]:
            config = select_first(docs, lambda x: x[model_constants.KIND] == 'configuration/' + feature_key and x[
                model_constants.NAME] == config_selector)
            if config is None:
                config = merge_with_defaults(cluster_model[model_constants.PROVIDER], 'configuration/' + feature_key,
                                             config_selector)
            docs.append(config)

    @staticmethod
    def add_data_if_not_defined(docs, provider, kind):
        if not select_first(docs, lambda x: x[model_constants.KIND] == kind):
            files = load_all_docs_from_defaults(provider, kind)
            docs.append(select_first(files, lambda x: x[model_constants.NAME] == "default"))
