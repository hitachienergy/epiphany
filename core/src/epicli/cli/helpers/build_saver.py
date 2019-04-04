import os

from cli.helpers.data_loader import load_template_file
from cli.helpers.yaml_helpers import dump_all


OUTPUT_FOLDER_PATH = '../../output/'
TERRAFORM_OUTPUT_DIR = 'terraform/'
MANIFEST_FILE_NAME = 'manifest.yml'
INVENTORY_FILE_NAME = 'inventory'


def save_manifest(docs, cluster_name):
    build_dir = get_build_path(cluster_name)
    with open(os.path.join(build_dir, MANIFEST_FILE_NAME), 'w') as stream:
        dump_all(docs, stream)


def save_inventory(inventory, cluster_model):
    cluster_name = cluster_model.specification.name
    build_dir = get_build_path(cluster_name)

    template = load_template_file("ansible", "common", "ansible_inventory")

    content = template.render(inventory=inventory, cluster_model=cluster_model)

    with open(os.path.join(build_dir, INVENTORY_FILE_NAME), 'w') as file:
        file.write(content)


def save_terraform_file(content, cluster_name, filename):
    terraform_dir = get_terraform_path(cluster_name)
    with open(os.path.join(terraform_dir, filename), 'w') as terraform_output_file:
        terraform_output_file.write(content)


def get_output_path():
    output_dir = os.path.join(os.path.dirname(__file__), OUTPUT_FOLDER_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir;


def get_build_path(cluster_name):
    build_dir = os.path.join(get_output_path(), cluster_name)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    return build_dir


def get_inventory_path(cluster_name):
    return os.path.join(get_build_path(cluster_name), INVENTORY_FILE_NAME)


def get_terraform_path(cluster_name):
    terraform_dir = os.path.join(get_build_path(cluster_name), TERRAFORM_OUTPUT_DIR)
    if not os.path.exists(terraform_dir):
        os.makedirs(terraform_dir)
    return terraform_dir
