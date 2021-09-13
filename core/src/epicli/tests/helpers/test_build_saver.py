import os
from ruamel.yaml import YAML
from collections import OrderedDict
from cli.helpers.yaml_helpers import safe_load_all, safe_load
from cli.helpers.objdict_helpers import dict_to_objdict
from cli.helpers.build_saver import get_build_path, get_output_path, get_terraform_path, get_ansible_path,\
    get_ansible_vault_path, get_ansible_config_file_path, get_inventory_path, get_manifest_path,\
    save_manifest, save_sp, save_inventory, save_ansible_config_file, get_inventory_path_for_build,\
    get_ansible_config_file_path_for_build, get_ansible_path_for_build,\
    TERRAFORM_OUTPUT_DIR, ANSIBLE_OUTPUT_DIR, ANSIBLE_VAULT_OUTPUT_DIR, INVENTORY_FILE_NAME,\
    MANIFEST_FILE_NAME, SP_FILE_NAME

CLUSTER_NAME = 'test'
OUTPUT_PATH = '/workspaces/epiphany/core/src/epicli/test_results/'
SPEC_OUTPUT_DIR = 'spec_tests/'
TEST_DOCS = \
    [{'kind': 'epiphany-cluster',
      'title': 'Epiphany cluster Config',
      'provider': 'any',
      'name': 'default',
      'specification': {'name': 'default',
                        'admin_user': {'name': 'operations', 'key_path': 'id_rsa'}}},
     {'kind': 'infrastructure/machine', 'provider': 'any', 'name': 'default-repository'}]
TEST_SP = {'appId': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx',
           'displayName': 'test-rg',
           'name': 'http://test-rg',
           'password': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
           'tenant': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}
TEST_INVENTORY = [{'hosts':
                   [{'ip': '10.0.0.1', 'name': 'test-1'},
                    {'ip': '10.0.0.2', 'name': 'test-2'}],
                   'role': 'postgresql'},
                  {'hosts':
                   [{'ip': '10.0.0.3', 'name': 'test-3'},
                    {'ip': '10.0.0.4', 'name': 'test-4'}],
                   'role': 'filebeat'}]
TEST_CLUSTER_MODEL = \
    {'kind': 'epiphany-cluster',
     'title': 'Epiphany cluster Config',
     'provider': 'azure',
     'name': CLUSTER_NAME,
     'specification':
     {'prefix': 'test',
      'name': CLUSTER_NAME,
      'admin_user': {'name': 'operations', 'key_path': 'id_rsa'},
      'cloud':
      {
          'subscription_name': 'Test-Dev',
          'vnet_address_pool': '10.1.0.0/20',
          'use_public_ips': False,
          'use_service_principal': False,
          'region': 'West Europe',
          'credentials': {'key': '1111-1111-1111',
                          'secret': 'XXXXXXXXXXXXXXX'},
          'default_os_image': 'default'},
      }
     }
ANSIBLE_CONFIG_FILE_SETTINGS = [('defaults', {
                                 'interpreter_python': 'auto_legacy_silent', 'allow_world_readable_tmpfiles': 'true'})]

# TODO: Check directory creation for tests


def test_get_output_path():
    output_path = os.path.join(OUTPUT_PATH)
    result_path = get_output_path()
    assert os.path.exists(output_path)
    assert result_path == output_path


def test_get_build_path():
    build_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME)
    result_path = get_build_path(CLUSTER_NAME)
    assert os.path.exists(build_path)
    assert result_path == build_path


def test_get_inventory_path():
    assert get_inventory_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, INVENTORY_FILE_NAME)


def test_get_manifest_path():
    assert get_manifest_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, MANIFEST_FILE_NAME)


def test_get_terraform_path():
    terraform_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, TERRAFORM_OUTPUT_DIR)
    result_path = get_terraform_path(CLUSTER_NAME)
    assert os.path.exists(terraform_path)
    assert result_path == terraform_path


def test_get_ansible_path():
    assert get_ansible_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR)


def test_get_ansible_vault_path():
    ansible_vault_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_VAULT_OUTPUT_DIR)
    result_path = get_ansible_vault_path(CLUSTER_NAME)
    assert os.path.exists(ansible_vault_path)
    assert result_path == ansible_vault_path


def test_get_ansible_config_file_path():
    assert get_ansible_config_file_path(CLUSTER_NAME) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR, 'ansible.cfg')


def test_get_inventory_path_for_build():
    assert get_inventory_path_for_build(os.path.join(
        OUTPUT_PATH, CLUSTER_NAME)) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, INVENTORY_FILE_NAME)


def test_get_ansible_path_for_build():
    ansible_path_for_build_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR)
    result_path = get_ansible_path_for_build(os.path.join(
        OUTPUT_PATH, CLUSTER_NAME))
    assert os.path.exists(ansible_path_for_build_path)
    assert result_path == ansible_path_for_build_path


def test_get_ansible_config_file_path_for_build():
    assert get_ansible_config_file_path_for_build(os.path.join(
        OUTPUT_PATH, CLUSTER_NAME)) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR,  "ansible.cfg")


def test_save_manifest():
    save_manifest(TEST_DOCS, CLUSTER_NAME, MANIFEST_FILE_NAME)
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


def test_save_inventory():
    cluster_model = dict_to_objdict(TEST_CLUSTER_MODEL)
    save_inventory(TEST_INVENTORY, cluster_model)
    f = open(os.path.join(OUTPUT_PATH, CLUSTER_NAME,
             INVENTORY_FILE_NAME), mode='r')
    inventory_content = f.read()
    assert 'test-1 ansible_host=10.0.0.1' in inventory_content
    assert 'test-2 ansible_host=10.0.0.2' in inventory_content
    assert 'test-3 ansible_host=10.0.0.3' in inventory_content
    assert 'test-4 ansible_host=10.0.0.4' in inventory_content
    assert 'ansible_user=operations' in inventory_content
    assert 'ansible_ssh_private_key_file=id_rsa' in inventory_content


def test_save_ansible_config_file():
    config_file_settings = OrderedDict(ANSIBLE_CONFIG_FILE_SETTINGS)
    ansible_config_file_path = os.path.join(
        OUTPUT_PATH, CLUSTER_NAME, ANSIBLE_OUTPUT_DIR, 'ansible.cfg')
    save_ansible_config_file(
        config_file_settings, ansible_config_file_path)
    f = open(ansible_config_file_path, mode='r')
    ansible_config_file_content = f.read()
    assert 'interpreter_python = auto_legacy_silent' in ansible_config_file_content
    assert 'allow_world_readable_tmpfiles = true' in ansible_config_file_content
