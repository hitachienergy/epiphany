import os
from cli.helpers.build_saver import get_build_path, get_output_path, get_terraform_path, get_ansible_path,\
    get_ansible_vault_path, get_ansible_config_file_path, get_inventory_path,\
    TERRAFORM_OUTPUT_DIR, ANSIBLE_OUTPUT_DIR, ANSIBLE_VAULT_OUTPUT_DIR, INVENTORY_FILE_NAME

CLUSTER_NAME = "test"
OUTPUT_PATH = "/workspaces/epiphany/core/src/epicli/test_results/"
MANIFEST_FILE_NAME = 'manifest.yml'
SP_FILE_NAME = 'sp.yml'
SPEC_OUTPUT_DIR = 'spec_tests/'

# TODO: Check directory creation for tests
# TODO: Sort imports

def test_get_output_path():
    assert get_output_path() == os.path.join(OUTPUT_PATH)


def test_get_build_path():
    assert get_build_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME)


def test_get_inventory_path():
    assert get_inventory_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, INVENTORY_FILE_NAME)


def test_get_terraform_path():
    assert get_terraform_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, TERRAFORM_OUTPUT_DIR)


def test_get_ansible_path():
    assert get_ansible_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR)


def test_get_ansible_vault_path():
    assert get_ansible_vault_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_VAULT_OUTPUT_DIR)


def test_get_ansible_config_file_path():
    assert get_ansible_config_file_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR, 'ansible.cfg')
