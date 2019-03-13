import yaml
import os


DEFAULTS_FOLDER_PATH = '../../data/'


def load_file_from_defaults(provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DEFAULTS_FOLDER_PATH, provider, 'defaults', kind+'.yml')
    with open(path_to_file, 'r') as stream:
        return yaml.safe_load(stream)


def load_all_docs_from_defaults(provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DEFAULTS_FOLDER_PATH, provider, 'defaults', kind+'.yml')
    with open(path_to_file, 'r') as stream:
        return list(yaml.safe_load_all(stream))
