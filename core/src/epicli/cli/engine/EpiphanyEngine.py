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

    def __enter__(self):
        return self

    def run(self):
        self.merge_with_defaults()

    def merge_with_defaults(self):
        # todo validation
        if os.path.isabs(self.file_path):
            path_to_load = self.file_path
        else:
            path_to_load = os.path.join(os.getcwd(), self.file_path)

        user_file_stream = open(path_to_load, 'r')
        user_yaml_files = yaml.safe_load_all(user_file_stream)
        state_docs = list()
        script_dir = os.path.dirname(__file__)

        for user_file_yaml in user_yaml_files:
            file_path_with_defaults = os.path.join(script_dir, DEFAULTS_FOLDER_PATH,
                                                   user_file_yaml[model_constants.PROVIDER], 'defaults', user_file_yaml[model_constants.KIND]+'.yml')
            with open(file_path_with_defaults, 'r') as stream:
                file_with_defaults = yaml.safe_load(stream)
                merge_dict(file_with_defaults, user_file_yaml)
                state_docs.append(file_with_defaults)

        build_directory = os.path.join(script_dir, BUILD_FOLDER_PATH, self.context)
        if not os.path.exists(build_directory):
            os.makedirs(build_directory)

        # todo go through all defaults for provider

        with open(os.path.join(build_directory, OUTPUT_FILE_NAME), 'w') as stream:
            yaml.dump_all(state_docs, stream, default_flow_style=False)

    def __exit__(self, exc_type, exc_value, traceback):
        print("close")
