from cli.helpers.build_saver import get_build_path, get_output_path, get_terraform_path, get_ansible_path,\
    get_ansible_vault_path, get_ansible_config_file_path

CLUSTER_NAME = "test"
OUTPUT_PATH = "/workspaces/epiphany/core/src/epicli/test_results/"
TERRAFORM_OUTPUT_DIR = 'terraform/'
MANIFEST_FILE_NAME = 'manifest.yml'
SP_FILE_NAME = 'sp.yml'
INVENTORY_FILE_NAME = 'inventory'
ANSIBLE_OUTPUT_DIR = 'ansible/'
ANSIBLE_VAULT_OUTPUT_DIR = 'vault/'
SPEC_OUTPUT_DIR = 'spec_tests/'

def test_get_output_path():
    assert get_output_path() == f"{OUTPUT_PATH}"

def test_get_build_path():
    assert get_build_path(CLUSTER_NAME) == f"{OUTPUT_PATH}test"

def test_get_terraform_path():
    assert get_terraform_path(CLUSTER_NAME) == f"{OUTPUT_PATH}test/terraform/"

def test_get_ansible_path():
    assert get_ansible_path(CLUSTER_NAME) == f"{OUTPUT_PATH}test/ansible/"

def test_get_ansible_vault_path():
    assert get_ansible_vault_path(CLUSTER_NAME) == f"{OUTPUT_PATH}test/vault/"

def test_get_ansible_config_file_path():
    assert get_ansible_config_file_path(CLUSTER_NAME) == f"{OUTPUT_PATH}test/ansible/ansible.cfg"