import distutils
import shutil
from distutils import dir_util
import os
from cli.helpers.data_loader import load_template_file, types
from cli.helpers.yaml_helpers import dump_all
from cli.helpers.Config import Config

TERRAFORM_OUTPUT_DIR = 'terraform/'
MANIFEST_FILE_NAME = 'manifest.yml'
INVENTORY_FILE_NAME = 'inventory'
ANSIBLE_OUTPUT_DIR = 'ansible/'


def save_manifest(docs, cluster_name, manifest_name=MANIFEST_FILE_NAME):
    build_dir = get_build_path(cluster_name)
    path = os.path.join(build_dir, manifest_name)
    with open(path, 'w') as stream:
        dump_all(docs, stream)
    return path


def save_inventory(inventory, cluster_model):
    cluster_name = cluster_model.specification.name
    build_dir = get_build_path(cluster_name)
    template = load_template_file(types.ANSIBLE, "common", "ansible_inventory")
    content = template.render(inventory=inventory, cluster_model=cluster_model)
    file_path = os.path.join(build_dir, INVENTORY_FILE_NAME)
    save_to_file(file_path, content)


# method cleans generated .tf files (not tfstate)
def clear_terraform_templates(cluster_name):
    terraform_dir = get_terraform_path(cluster_name)
    files = os.listdir(terraform_dir)
    for file in files:
        if file.endswith(".tf"):
            os.remove(os.path.join(terraform_dir, file))


def save_terraform_file(content, cluster_name, filename):
    terraform_dir = get_terraform_path(cluster_name)
    terraform_output_file_path = os.path.join(terraform_dir, filename)
    save_to_file(terraform_output_file_path, content)


def save_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def get_output_path():
    output_dir = os.path.join(os.path.dirname(__file__), Config().output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def get_build_path(cluster_name):
    build_dir = os.path.join(get_output_path(), cluster_name)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    return build_dir


def get_inventory_path(cluster_name):
    return os.path.join(get_build_path(cluster_name), INVENTORY_FILE_NAME)


def get_inventory_path_for_build(build_directory):
    return os.path.join(build_directory, INVENTORY_FILE_NAME)


def get_terraform_path(cluster_name):
    terraform_dir = os.path.join(get_build_path(cluster_name), TERRAFORM_OUTPUT_DIR)
    if not os.path.exists(terraform_dir):
        os.makedirs(terraform_dir)
    return terraform_dir


def get_ansible_path(cluster_name):
    ansible_dir = os.path.join(get_build_path(cluster_name), ANSIBLE_OUTPUT_DIR)
    if not os.path.exists(ansible_dir):
        os.makedirs(ansible_dir)
    return ansible_dir


def copy_files_recursively(src, dst):
    distutils.dir_util.copy_tree(src, dst)


def copy_file(src, dst):
    shutil.copy2(src, dst)

