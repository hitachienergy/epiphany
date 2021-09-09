import os
from ruamel.yaml import YAML
from cli.helpers.yaml_helpers import safe_load_all, safe_load
from cli.helpers.build_saver import get_build_path, get_output_path, get_terraform_path, get_ansible_path,\
    get_ansible_vault_path, get_ansible_config_file_path, get_inventory_path, get_manifest_path,\
    save_manifest, save_sp,\
    TERRAFORM_OUTPUT_DIR, ANSIBLE_OUTPUT_DIR, ANSIBLE_VAULT_OUTPUT_DIR, INVENTORY_FILE_NAME,\
    MANIFEST_FILE_NAME, SP_FILE_NAME

CLUSTER_NAME = "test"
OUTPUT_PATH = "/workspaces/epiphany/core/src/epicli/test_results/"
SPEC_OUTPUT_DIR = 'spec_tests/'
TEST_DOCS = [{'kind': 'epiphany-cluster', 'title': 'Epiphany cluster Config', 'provider': 'any',
         'name': 'default', 'specification': {'name': 'default',
                                              'admin_user': {'name': 'operations', 'key_path': 'id_rsa'}}},
        {'kind': 'infrastructure/machine', 'provider': 'any', 'name': 'default-repository'}]
TEST_SP = {'appId': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx', 'displayName': 'test-rg', 'name': 'http://test-rg',\
'password': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'tenant': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

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


def test_save_manifest():
    save_manifest(TEST_DOCS, CLUSTER_NAME, manifest_name=MANIFEST_FILE_NAME)
    manifest_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, MANIFEST_FILE_NAME)
    manifest_stream = open(manifest_path, 'r')
    manifest_file_content = safe_load_all(manifest_stream)
    assert TEST_DOCS == manifest_file_content

def test_save_sp():
    save_sp(TEST_SP, CLUSTER_NAME)
    sp_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, TERRAFORM_OUTPUT_DIR, SP_FILE_NAME)
    sp_stream = open(sp_path, 'r')
    sp_file_content = safe_load(sp_stream)
    assert TEST_SP == sp_file_content