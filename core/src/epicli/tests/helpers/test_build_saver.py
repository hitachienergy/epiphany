import os
from ruamel.yaml import YAML
from cli.helpers.build_saver import get_build_path, get_output_path, get_terraform_path, get_ansible_path,\
    get_ansible_vault_path, get_ansible_config_file_path, get_inventory_path, get_manifest_path,\
    save_manifest,\
    TERRAFORM_OUTPUT_DIR, ANSIBLE_OUTPUT_DIR, ANSIBLE_VAULT_OUTPUT_DIR, INVENTORY_FILE_NAME,\
    MANIFEST_FILE_NAME

CLUSTER_NAME = "test"
OUTPUT_PATH = "/workspaces/epiphany/core/src/epicli/test_results/"
SP_FILE_NAME = 'sp.yml'
SPEC_OUTPUT_DIR = 'spec_tests/'
DOCS = [{'kind' : 'epiphany-cluster', 'title': 'Epiphany cluster Config', 'provider': 'any',\
         'name': 'default', 'specification': {'name': 'default',\
         'admin_user': {'name': 'operations', 'key_path': 'id_rsa'}}},
        {'kind': 'infrastructure/machine', 'provider': 'any', 'name' :'default-repository'}]

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


def test_get_manifest_path():
    assert get_manifest_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, MANIFEST_FILE_NAME)


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

# Todo: Finish test
def test_save_manifest():
    save_manifest(DOCS, CLUSTER_NAME, manifest_name=MANIFEST_FILE_NAME)
    assert 1 == 1
