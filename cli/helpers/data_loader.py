import os
import glob
import json
from collections import namedtuple

import jinja2
from jinja2 import Template

from cli.helpers.yaml_helpers import safe_load_all, safe_load
from cli.helpers.objdict_helpers import dict_to_objdict


BASE_DIR_PROD = '/epicli'
BASE_DIR_DEV = os.path.join(os.path.dirname(__file__), '../../')
BASE_DIR = (
    BASE_DIR_PROD
    if os.path.exists(BASE_DIR_PROD)
    else BASE_DIR_DEV
)
SCHEMA_DIR = os.path.join(BASE_DIR, 'schema')

Types = namedtuple('FileType', 'DEFAULT VALIDATION TERRAFORM ANSIBLE')
types = Types(DEFAULT='defaults',
              VALIDATION='validation',
              TERRAFORM='terraform',
              ANSIBLE='ansible')


def load_schema_obj(file_type, provider, kind):
    path_to_file = os.path.join(SCHEMA_DIR, provider, file_type, kind+'.yml')
    if os.path.isfile(path_to_file):
        return load_yaml_file(path_to_file)
    else:
        path_to_file = os.path.join(SCHEMA_DIR, 'common', file_type, kind + '.yml')
        return load_yaml_file(path_to_file)


def load_all_schema_objs(file_type, provider, kind):
    path_to_file = os.path.join(SCHEMA_DIR, provider, file_type, kind+'.yml')
    if os.path.isfile(path_to_file):
        return load_yamls_file(path_to_file)
    else:
        path_to_file = os.path.join(SCHEMA_DIR, 'common', file_type, kind + '.yml')
        return load_yamls_file(path_to_file)


def load_all_schema_objs_from_directory(file_type, provider, directory):
    directory_path = os.path.join(SCHEMA_DIR, provider, file_type, directory)
    docs = []
    for filename in glob.glob(os.path.join(directory_path, '*.yml')):
        documents = load_yamls_file(filename)
        docs += documents
    return docs


def load_yaml_file(path_to_file):
    with open(path_to_file, 'r') as stream:
        return safe_load(stream)


def load_yamls_file(path_to_file):
    with open(path_to_file, 'r') as stream:
        return safe_load_all(stream)


def load_template_file(file_type, provider, kind):
    path_to_file = os.path.join(BASE_DIR, file_type, provider, kind + '.j2')
    with open(path_to_file, 'r') as stream:
        return Template(stream.read(), undefined=jinja2.StrictUndefined)


def load_json_obj(path_to_file):
    with open(path_to_file, 'r') as stream:
        obj = json.load(stream)
        return dict_to_objdict(obj)
