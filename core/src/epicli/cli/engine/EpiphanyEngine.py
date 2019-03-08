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
            config = self.get_machine_data(component_value, docs, cluster_model)
            if config is not None:
                docs.append(config)

        build_directory = os.path.join(self.script_dir, BUILD_FOLDER_PATH, self.context)
        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        self.add_data_if_not_defined(docs, cluster_model[model_constants.PROVIDER], "infrastructure/network") # todo add rest of infra data

        with open(os.path.join(build_directory, OUTPUT_FILE_NAME), 'w') as stream:
            yaml.dump_all(docs, stream, default_flow_style=False)

        # todo validate
        # todo generate .tf files
        # todo run terraform
        # todo generate ansible inventory
        # todo run ansible

    def get_machine_data(self, component_value, docs, cluster_model):
        machine_selector = component_value["machine"]
        all_machines = self.select_all(docs, lambda x: x[model_constants.KIND] == "infrastructure/virtual-machine")
        machine = self.select_first(all_machines, lambda x: x[model_constants.NAME] == machine_selector)
        if machine is None:
            file_path_with_defaults = os.path.join(self.data_defaults_folder_path,
                                                   cluster_model[model_constants.PROVIDER], 'defaults',
                                                   'infrastructure/virtual-machine.yml')
            with open(file_path_with_defaults, 'r') as stream:
                files = list(yaml.safe_load_all(stream))
                machine_spec = self.select_first(files, lambda x: x[model_constants.NAME] == machine_selector) # self.find_document(files, "name", machine_selector)

                if machine_selector != "default":
                    default_machine = self.select_first(files, lambda x: x[model_constants.NAME] == "default")
                    merge_dict(default_machine, machine_spec)
                    return default_machine
                return machine_spec
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
