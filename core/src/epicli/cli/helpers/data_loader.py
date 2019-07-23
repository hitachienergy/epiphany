import os
import sys
from cli.helpers.yaml_helpers import safe_load_all, safe_load
from collections import namedtuple
import jinja2
import json
from cli.helpers.objdict_helpers import dict_to_objdict
from jinja2 import Template
import glob

BASE_DIR = os.path.dirname(__file__)
#TODO: Look at this in depth since by default sys.prefix should return /urs/local
DATA_FOLDER_PATH_SYSTEM = os.path.join(sys.prefix, 'local/epicli/data').replace('local/local', 'local')
DATA_FOLDER_PATH_LOCAL = os.path.join(BASE_DIR, '../../data')
DATA_FOLDER_PATH = (
    DATA_FOLDER_PATH_SYSTEM
    if os.path.exists(DATA_FOLDER_PATH_SYSTEM)
    else DATA_FOLDER_PATH_LOCAL
)

Types = namedtuple('FileType', 'DEFAULT VALIDATION TERRAFORM ANSIBLE')
types = Types(DEFAULT='defaults',
              VALIDATION='validation',
              TERRAFORM='terraform',
              ANSIBLE='ansible')


def load_yaml_obj(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as stream:
            return safe_load(stream)
    else:
        path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, 'common', file_type, kind + '.yml')
        with open(path_to_file, 'r') as stream:
            return safe_load(stream)


def load_all_yaml_objs(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
    return load_file_from_path(script_dir, path_to_file, file_type, kind)


def load_file_from_path(script_dir, path_to_file, file_type, kind):
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as stream:
            return safe_load_all(stream)
    else:
        path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, 'common', file_type, kind + '.yml')
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