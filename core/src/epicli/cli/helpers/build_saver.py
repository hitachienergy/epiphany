import distutils
import shutil
import os
from os import listdir
from os.path import isfile, join
from distutils import dir_util
from cli.helpers.data_loader import load_template_file, types
from cli.helpers.yaml_helpers import dump_all, dump
from cli.helpers.Config import Config

TERRAFORM_OUTPUT_DIR = 'terraform/'
MANIFEST_FILE_NAME = 'manifest.yml'
SP_FILE_NAME = 'sp.yml'
INVENTORY_FILE_NAME = 'inventory'
ANSIBLE_OUTPUT_DIR = 'ansible/'
ANSIBLE_VAULT_OUTPUT_DIR = 'vault/'
SPEC_OUTPUT_DIR = 'spec_tests/'

BUILD_EPICLI = 'BUILD_EPICLI'
BUILD_LEGACY = 'BUILD_LEGACY_02X'

def save_manifest(docs, cluster_name, manifest_name=MANIFEST_FILE_NAME):
    build_dir = get_build_path(cluster_name)
    path = os.path.join(build_dir, manifest_name)
    with open(path, 'w') as stream:
        dump_all(docs, stream)
    return path


def save_sp(service_principle, cluster_name):
    terraform_dir = get_terraform_path(cluster_name)
    path = os.path.join(terraform_dir, SP_FILE_NAME)
    with open(path, 'w') as stream:
        dump(service_principle, stream)
    return path


def save_inventory(inventory, cluster_model, build_dir=None):
    if build_dir == None:
        cluster_name = cluster_model.specification.name
        build_dir = get_build_path(cluster_name)
    template = load_template_file(types.ANSIBLE, "common", "ansible_inventory")
    content = template.render(inventory=inventory, cluster_model=cluster_model)
    file_path = os.path.join(build_dir, INVENTORY_FILE_NAME)
    save_to_file(file_path, content)


def save_ansible_config_file(ansible_config_file_settings, ansible_config_file_path):
    template = load_template_file(types.ANSIBLE, "common", "ansible.cfg")
    content = template.render(ansible_config_file_settings=ansible_config_file_settings)
    save_to_file(ansible_config_file_path, content)


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
    if not os.path.exists(Config().output_dir):
        os.makedirs(Config().output_dir)
    return Config().output_dir


def get_build_path(cluster_name):
    build_dir = os.path.join(get_output_path(), cluster_name)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    return build_dir


def get_inventory_path(cluster_name):
    return os.path.join(get_build_path(cluster_name), INVENTORY_FILE_NAME)


def get_inventory_path_for_build(build_directory):
    build_version = check_build_output_version(build_directory)
    inventory =  os.path.join(build_directory, INVENTORY_FILE_NAME)
    if build_version == BUILD_EPICLI: 
        return inventory
    if build_version == BUILD_LEGACY: 
        files = [f for f in listdir(inventory) if isfile(join(inventory, f))]
        if len(files) != 1:
            raise Exception(f'Not a valid legacy build directory.')
        return join(inventory, files[0]) 


def get_ansible_config_file_path(cluster_name):
    return os.path.join(get_ansible_path(cluster_name), "ansible.cfg")


def get_ansible_config_file_path_for_build(build_directory):
    return os.path.join(get_ansible_path_for_build(build_directory), "ansible.cfg")


def check_build_output_version(build_directory):
    if not os.path.exists(build_directory):
        raise Exception('Build directory does not exist')

    manifest_path = os.path.join(build_directory, INVENTORY_FILE_NAME)

    # if manifest is in the build root/inventory we are dealing with post 0.3.0
    if os.path.exists(manifest_path) and not os.path.isdir(manifest_path):
        return BUILD_EPICLI
    
    # if manifest is in root/inventory/.... we are dealing with pre 0.3.0
    if os.path.exists(manifest_path) and os.path.isdir(manifest_path):
        return BUILD_LEGACY

    # if we come here its a new run or upgrade in which case its EPICLI
    return BUILD_EPICLI


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

def get_ansible_vault_path(cluster_name):
    ansible_vault_dir = os.path.join(get_build_path(cluster_name), ANSIBLE_VAULT_OUTPUT_DIR)
    if not os.path.exists(ansible_vault_dir):
        os.makedirs(ansible_vault_dir)
    return ansible_vault_dir

def get_ansible_path_for_build(build_directory):
    ansible_dir = os.path.join(build_directory, ANSIBLE_OUTPUT_DIR)
    if not os.path.exists(ansible_dir):
        os.makedirs(ansible_dir)
    return ansible_dir    

def copy_files_recursively(src, dst):
    distutils.dir_util.copy_tree(src, dst)

def copy_file(src, dst):
    shutil.copy2(src, dst)
