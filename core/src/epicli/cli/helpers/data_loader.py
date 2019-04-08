import os
from cli.helpers.yaml_helpers import safe_load_all, safe_load
from collections import namedtuple
import jinja2
from jinja2 import Template

DATA_FOLDER_PATH = '../../data/'

Types = namedtuple('FileType', 'DEFAULT VALIDATION TERRAFORM ANSIBLE')
types = Types(DEFAULT='defaults',
              VALIDATION='validation',
              TERRAFORM='terraform',
              ANSIBLE='ansible')


def load_yaml_obj(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
    with open(path_to_file, 'r') as stream:
        return safe_load(stream)


def load_all_yaml_objs(file_type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, file_type, kind+'.yml')
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

