import os
import sys
import glob
import json
from collections import namedtuple

import jinja2
from jinja2 import Template

from cli.helpers.yaml_helpers import safe_load_all, safe_load
from cli.helpers.objdict_helpers import dict_to_objdict


BASE_DIR = os.path.dirname(__file__)
#TODO: Look at this in depth since by default sys.prefix should return /urs/local
DATA_FOLDER_PATH_SYSTEM = os.path.join(sys.prefix, 'local/epicli/data').replace('local/local', 'local')
DATA_FOLDER_PATH_LOCAL = os.path.join(BASE_DIR, '../../data')
DATA_FOLDER_PATH = (
    DATA_FOLDER_PATH_SYSTEM
    if os.path.exists(DATA_FOLDER_PATH_SYSTEM)
    else DATA_FOLDER_PATH_LOCAL
)
MANIFEST_FILE_NAME = 'manifest.yml'

Types = namedtuple('FileType', 'DEFAULT VALIDATION TERRAFORM ANSIBLE')
types = Types(DEFAULT='defaults',
              VALIDATION='validation',
              TERRAFORM='terraform',
              ANSIBLE='ansible')


def load_yaml_obj(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
    if os.path.isfile(path_to_file):
        return load_yaml_file(path_to_file)
    else:
        path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, 'common', file_type, kind + '.yml')
        return load_yaml_file(path_to_file)


def load_all_yaml_objs(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
    return load_file_from_path(script_dir, path_to_file, file_type, kind)


def load_file_from_path(script_dir, path_to_file, file_type, kind):
    if os.path.isfile(path_to_file):
        return load_yamls_file(path_to_file)
    else:
        path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, 'common', file_type, kind + '.yml')
        return load_yamls_file(path_to_file)


def load_yaml_file(path_to_file):
    with open(path_to_file, 'r') as stream:
        return safe_load(stream)


def load_yamls_file(path_to_file):
    with open(path_to_file, 'r') as stream:
        return safe_load_all(stream)


def load_template_file(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind + '.j2')
    with open(path_to_file, 'r') as stream:
        return Template(stream.read(), undefined=jinja2.StrictUndefined)


def load_json_obj(path_to_file):
    with open(path_to_file, 'r') as stream:
        obj = json.load(stream)
        return dict_to_objdict(obj)


# currently valid options for directory param are 'defaults/infrastructure'|'defaults/configuration'
def load_all_documents_from_folder(provider, directory):
    script_dir = os.path.dirname(__file__)
    directory_path = os.path.join(script_dir, DATA_FOLDER_PATH, provider, directory)
    docs = []
    for filename in glob.glob(os.path.join(directory_path, '*.yml')):
        documents = load_file_from_path(script_dir, filename, None, None)
        docs += documents
    return docs


def load_manifest_docs(build_dir):
    path_to_manifest = os.path.join(build_dir, MANIFEST_FILE_NAME)
    if not os.path.isfile(path_to_manifest):
        raise Exception('No manifest.yml inside the build folder')

    return load_yamls_file(path_to_manifest)


def get_data_dir_path():
    script_dir = os.path.dirname(__file__)
    directory_path = os.path.join(script_dir, DATA_FOLDER_PATH)
    return os.path.abspath(directory_path)


def get_provider_subdir_path(file_type, provider):
    return os.path.join(get_data_dir_path(), provider, file_type)
