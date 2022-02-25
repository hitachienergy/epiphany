import glob
import json
import os
from collections import namedtuple

import jinja2
from jinja2 import Template

from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.helpers.yaml_helpers import safe_load, safe_load_all

BASE_DIR_PROD = '/epicli'
BASE_DIR_DEV = os.path.join(os.path.dirname(__file__), '../../../')
BASE_DIR = (
    BASE_DIR_PROD
    if os.path.exists(BASE_DIR_PROD)
    else BASE_DIR_DEV
)
SCHEMA_DIR = os.path.join(BASE_DIR, 'schema')
TERRAFORM_PATH = os.path.join(BASE_DIR, 'terraform')
ANSIBLE_PATH = os.path.join(BASE_DIR, 'ansible')
ANSIBLE_PLAYBOOK_PATH = os.path.join(ANSIBLE_PATH, 'playbooks')

TemplateTypes = namedtuple('TemplateTypes', 'TERRAFORM ANSIBLE')
template_types = TemplateTypes(TERRAFORM='terraform', ANSIBLE='ansible')

SchemaTypes = namedtuple('SchemaTypes', 'DEFAULT VALIDATION')
schema_types = SchemaTypes(DEFAULT='defaults', VALIDATION='validation')


def load_schema_obj(schema_type, provider, kind):
    path_to_file = os.path.join(SCHEMA_DIR, provider, schema_type, f'{kind}.yml')
    if os.path.isfile(path_to_file):
        return load_yaml_file(path_to_file)
    else:
        path_to_file = os.path.join(SCHEMA_DIR, 'common', schema_type, f'{kind}.yml')
        return load_yaml_file(path_to_file)


def load_all_schema_objs(schema_type, provider, kind):
    path_to_file = os.path.join(SCHEMA_DIR, provider, schema_type, f'{kind}.yml')
    if os.path.isfile(path_to_file):
        return load_yamls_file(path_to_file)
    else:
        path_to_file = os.path.join(SCHEMA_DIR, 'common', schema_type, f'{kind}.yml')
        return load_yamls_file(path_to_file)


def load_all_schema_objs_from_directory(schema_type, provider, directory):
    directory_path = os.path.join(SCHEMA_DIR, provider, schema_type, directory)
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


def load_template_file(template_type, provider, kind):
    path_to_file = os.path.join(BASE_DIR, template_type, provider, kind + '.j2')
    with open(path_to_file, 'r') as stream:
        return Template(stream.read(), undefined=jinja2.StrictUndefined)


def load_json_obj(path_to_file):
    with open(path_to_file, 'r') as stream:
        obj = json.load(stream)
        return dict_to_objdict(obj)
