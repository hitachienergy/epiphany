import os
from cli.helpers.yaml_helpers import safe_load_all, safe_load
import jinja2
from jinja2 import Template

DATA_FOLDER_PATH = '../../data/'


def load_yaml_obj(type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, type, kind+'.yml')
    with open(path_to_file, 'r') as stream:
        return safe_load(stream)


def load_all_yaml_objs(type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, type, kind+'.yml')
    if os.path.isfile(path_to_file):
        with open(path_to_file, 'r') as stream:
            return safe_load_all(stream)
    else:
        path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, 'common', type, kind + '.yml')
        with open(path_to_file, 'r') as stream:
            return safe_load_all(stream)


def load_template_file(type, provider, kind):
    script_dir = os.path.dirname(__file__)
    path_to_file = os.path.join(script_dir, DATA_FOLDER_PATH, provider, type, kind + '.j2')
    with open(path_to_file, 'r') as stream:
        return Template(stream.read(), undefined=jinja2.StrictUndefined)



