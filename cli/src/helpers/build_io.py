import os
import shutil

from pathlib import Path

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

from cli.src.Config import Config
from cli.src.helpers.data_loader import (ANSIBLE_PLAYBOOK_PATH,
                                         load_template_file, load_yamls_file,
                                         template_types)
from cli.src.helpers.yaml_helpers import dump, dump_all

TERRAFORM_OUTPUT_DIR = 'terraform/'
SP_FILE_NAME = 'sp.yml'
ANSIBLE_INVENTORY_FILE = 'inventory'
ANSIBLE_CFG_FILE = 'ansible.cfg'
ANSIBLE_OUTPUT_DIR = 'ansible/'
ANSIBLE_VAULT_OUTPUT_DIR = 'vault/'
SPEC_OUTPUT_DIR = 'spec_tests/'


def save_sp(service_principle, cluster_name):
    terraform_dir = get_terraform_path(cluster_name)
    path = os.path.join(terraform_dir, SP_FILE_NAME)
    with open(path, 'w') as stream:
        dump(service_principle, stream)
    return path


def save_inventory(inventory, cluster_model, build_dir=None):
    if build_dir is None:
        cluster_name = cluster_model.specification.name
        build_dir = get_build_path(cluster_name)
    template = load_template_file(template_types.ANSIBLE, '', ANSIBLE_INVENTORY_FILE)
    content = template.render(inventory=inventory, cluster_model=cluster_model)
    file_path = os.path.join(build_dir, ANSIBLE_INVENTORY_FILE)
    save_to_file(file_path, content)


def load_inventory(inventory_path):
    return InventoryManager(loader=DataLoader(), sources=inventory_path)


def save_ansible_config_file(ansible_config_file_settings, ansible_config_file_path):
    template = load_template_file(template_types.ANSIBLE, '', ANSIBLE_CFG_FILE)
    content = template.render(ansible_config_file_settings=ansible_config_file_settings)
    save_to_file(ansible_config_file_path, content)


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
    return os.path.join(get_build_path(cluster_name), ANSIBLE_INVENTORY_FILE)


def get_inventory_path_for_build(build_directory):
    return  os.path.join(build_directory, ANSIBLE_INVENTORY_FILE)


def get_ansible_config_file_path(cluster_name):
    return os.path.join(get_ansible_path(cluster_name), ANSIBLE_CFG_FILE)


def get_ansible_config_file_path_for_build(build_directory):
    return os.path.join(get_ansible_path_for_build(build_directory), ANSIBLE_CFG_FILE)


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


def delete_files_matching_glob(dir_path, pattern):
    for file in Path(dir_path).glob(pattern):
        file.unlink()


def delete_directory(dir_path):
    shutil.rmtree(dir_path, ignore_errors=True)


def copy_files_recursively(src, dst):
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_file(src, dst):
    shutil.copy2(src, dst)
