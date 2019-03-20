from cli.helpers.yaml_helpers import dump_all
import os

BUILD_FOLDER_PATH = '../../build/'
OUTPUT_FILE_NAME = 'manifest.yml'


def save_build(docs, context):
    script_dir = os.path.dirname(__file__)
    build_directory = os.path.join(script_dir, BUILD_FOLDER_PATH, context)
    if not os.path.exists(build_directory):
        os.makedirs(build_directory)
    with open(os.path.join(build_directory, OUTPUT_FILE_NAME), 'w') as stream:
        dump_all(docs, stream, default_flow_style=False)
