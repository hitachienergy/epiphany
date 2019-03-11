import yaml
import os
import cli.models.data_file_consts as model_constants
from cli.engine.dict_merge import merge_dict

DEFAULTS_FOLDER_PATH = '../../data/'
BUILD_FOLDER_PATH = '../../build/'
OUTPUT_FILE_NAME = 'manifest.yml'


class EpiphanyEngine:
    def __init__(self, input_data):
        self.file_path = input_data.file
        self.context = input_data.context
        self.script_dir = os.path.dirname(__file__)
        self.data_defaults_folder_path = os.path.join(self.script_dir, DEFAULTS_FOLDER_PATH)

    def __enter__(self):
        return self

    @staticmethod
    def find_document(documents, field_name, value):
        if documents is not None:
            matches = list(filter(lambda x: x[field_name] == value, documents))
            if len(matches) > 0:
                return matches[0]
        return None

    @staticmethod
    def select_first(documents, query):
        if documents is not None:
            for x in documents:
                if query(x):
                    return x
        return None

    @staticmethod
    def select_all(documents, query):
        if documents is not None:
            result = list()
            for x in documents:
                if query(x):
                    result.append(x)
            return result
        return None

    def run(self):
        docs = self.merge_with_defaults()
        cluster_model = self.find_document(docs, "kind", "epiphany-cluster")
        for component_key, component_value in cluster_model["specification"]["components"].items():
            if component_value["count"] < 1:
                continue
            self.append_infrastructure(docs, component_value, cluster_model)
            # todo append each VM with name, tags, address pools
            self.append_component_configuration(docs, component_key, component_value, cluster_model)

        self.add_data_if_not_defined(docs, cluster_model[model_constants.PROVIDER], "infrastructure/network")
        # todo add rest of infra data
        self.dump_epiphany_manifest(docs)

        # todo validate
        # todo generate .tf files
        # todo run terraform
        # todo generate ansible inventory
        # todo run ansible

    def dump_epiphany_manifest(self, docs):
        build_directory = os.path.join(self.script_dir, BUILD_FOLDER_PATH, self.context)
        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        with open(os.path.join(build_directory, OUTPUT_FILE_NAME), 'w') as stream:
            yaml.dump_all(docs, stream, default_flow_style=False)

    def append_infrastructure(self, docs, component_value, cluster_model):
        machine_selector = component_value["machine"]
        infrastructure = self.get_configuration(docs, cluster_model, 'infrastructure/virtual-machine', machine_selector)
        if infrastructure is not None:
            docs.append(infrastructure)

    def append_component_configuration(self, docs, component_key, component_value, cluster_model):
        file_path_with_mapping = os.path.join(self.data_defaults_folder_path,
                                              cluster_model[model_constants.PROVIDER], 'defaults',
                                              'configuration/feature-mapping.yml')
        features_map = self.select_first(docs, lambda x: x[model_constants.KIND] == 'configuration/feature-mapping')
        if features_map is None:
            with open(file_path_with_mapping, 'r') as stream:
                features_map = yaml.safe_load(stream)
        config_selector = component_value["configuration"]
        for feature_key in features_map["specification"][component_key]:
            config = self.get_configuration(docs, cluster_model, 'configuration/' + feature_key, config_selector)
            if config is not None:
                docs.append(config)

    def get_configuration(self, docs, cluster_model, feature_kind, config_selector):

        config = self.select_first(docs, lambda x: x[model_constants.KIND] == feature_kind and x[model_constants.NAME] == config_selector)
        if config is None:
            file_path_with_defaults = os.path.join(self.data_defaults_folder_path,
                                                   cluster_model[model_constants.PROVIDER], 'defaults',
                                                   feature_kind+'.yml')
            with open(file_path_with_defaults, 'r') as stream:
                files = list(yaml.safe_load_all(stream))
                config_spec = self.select_first(files, lambda x: x[model_constants.NAME] == config_selector)
                if config_selector != "default":
                    default_config = self.select_first(files, lambda x: x[model_constants.NAME] == "default")
                    merge_dict(default_config, config_spec)
                    return default_config
                return config_spec
        return None

    def add_data_if_not_defined(self, docs, provider, kind):
        if not self.select_first(docs, lambda x: x[model_constants.KIND] == kind):
            file_path_with_defaults = os.path.join(self.data_defaults_folder_path,
                                                   provider, 'defaults',
                                                   kind + '.yml')
            with open(file_path_with_defaults, 'r') as stream:
                files = yaml.safe_load_all(stream)
                # docs.append(self.find_document(files, "name", "default"))
                docs.append(self.select_first(files, lambda x: x[model_constants.NAME] == "default"))

    def merge_with_defaults(self):
        if os.path.isabs(self.file_path):
            path_to_load = self.file_path
        else:
            path_to_load = os.path.join(os.getcwd(), self.file_path)

        user_file_stream = open(path_to_load, 'r')
        user_yaml_files = yaml.safe_load_all(user_file_stream)

        state_docs = list()

        for user_file_yaml in user_yaml_files:
            file_path_with_defaults = os.path.join(self.data_defaults_folder_path,
                                                   user_file_yaml[model_constants.PROVIDER], 'defaults', user_file_yaml[model_constants.KIND]+'.yml')
            with open(file_path_with_defaults, 'r') as stream:
                files = yaml.safe_load_all(stream)
                file_with_defaults = self.select_first(files, lambda x: x[model_constants.NAME] == "default")
                merge_dict(file_with_defaults, user_file_yaml)
                state_docs.append(file_with_defaults)

        return state_docs

    def __exit__(self, exc_type, exc_value, traceback):
        print("close")
