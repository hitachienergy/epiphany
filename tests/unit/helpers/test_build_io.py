import os
from collections import OrderedDict

import pytest

from cli.src.helpers.build_io import (ANSIBLE_CFG_FILE, ANSIBLE_INVENTORY_FILE,
                                      ANSIBLE_OUTPUT_DIR,
                                      ANSIBLE_VAULT_OUTPUT_DIR,
                                      SP_FILE_NAME,
                                      TERRAFORM_OUTPUT_DIR,
                                      get_ansible_config_file_path,
                                      get_ansible_config_file_path_for_build,
                                      get_ansible_path,
                                      get_ansible_path_for_build,
                                      get_ansible_vault_path, get_build_path,
                                      get_inventory_path,
                                      get_inventory_path_for_build,
                                      get_output_path,
                                      get_terraform_path,
                                      save_ansible_config_file, save_inventory,
                                      save_sp)
from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.helpers.yaml_helpers import safe_load
from cli.src.schema.ManifestHandler import ManifestHandler
from tests.unit.helpers.constants import (CLUSTER_NAME_LOAD, CLUSTER_NAME_SAVE,
                                          NON_EXISTING_CLUSTER, OUTPUT_PATH,
                                          TEST_CLUSTER_MODEL, TEST_DOCS,
                                          TEST_INVENTORY)

TEST_SP = {'appId': 'xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx',
           'displayName': 'test-rg',
           'name': 'http://test-rg',
           'password': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
           'tenant': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}
ANSIBLE_CONFIG_FILE_SETTINGS = [('defaults', {
                                 'interpreter_python': 'auto_legacy_silent',
                                 'allow_world_readable_tmpfiles': 'true'
                                 })]


def test_get_output_path():
    output_path = os.path.join(OUTPUT_PATH)
    result_path =  os.path.normpath(get_output_path())
    assert os.path.exists(output_path)
    assert result_path == output_path


def test_get_build_path():
    build_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE)
    result_path = get_build_path(CLUSTER_NAME_SAVE)
    assert os.path.exists(build_path)
    assert result_path == build_path


def test_get_inventory_path():
    assert get_inventory_path(CLUSTER_NAME_SAVE) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_INVENTORY_FILE)


def test_get_manifest_path():
    mhandler = ManifestHandler(cluster_name=CLUSTER_NAME_SAVE)
    assert str(mhandler.manifest_path) == os.path.join(CLUSTER_NAME_SAVE, 'manifest.yml')


def test_get_terraform_path():
    terraform_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, TERRAFORM_OUTPUT_DIR)
    result_path = get_terraform_path(CLUSTER_NAME_SAVE)
    assert os.path.exists(terraform_path)
    assert result_path == terraform_path


def test_get_ansible_path():
    assert get_ansible_path(CLUSTER_NAME_SAVE) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_OUTPUT_DIR)


def test_get_ansible_vault_path():
    ansible_vault_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_VAULT_OUTPUT_DIR)
    result_path = get_ansible_vault_path(CLUSTER_NAME_SAVE)
    assert os.path.exists(ansible_vault_path)
    assert result_path == ansible_vault_path


def test_get_ansible_config_file_path():
    assert get_ansible_config_file_path(CLUSTER_NAME_SAVE) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_OUTPUT_DIR, ANSIBLE_CFG_FILE)


def test_get_inventory_path_for_build():
    assert get_inventory_path_for_build(os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE)) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_INVENTORY_FILE)


def test_get_ansible_path_for_build():
    ansible_path_for_build_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_OUTPUT_DIR)
    result_path = get_ansible_path_for_build(os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE))
    assert os.path.exists(ansible_path_for_build_path)
    assert result_path == ansible_path_for_build_path


def test_get_ansible_config_file_path_for_build():
    assert get_ansible_config_file_path_for_build(os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE)) == os.path.join(
        OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_OUTPUT_DIR,  ANSIBLE_CFG_FILE)


def test_load_manifest():
    mhandler = ManifestHandler(build_path=CLUSTER_NAME_LOAD)
    mhandler.read_manifest()
    assert mhandler.docs == TEST_DOCS


def test_save_sp():
    save_sp(TEST_SP, CLUSTER_NAME_SAVE)
    sp_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, TERRAFORM_OUTPUT_DIR, SP_FILE_NAME)
    with open(sp_path, 'r', encoding='utf-8') as sp_stream:
        sp_file_content = safe_load(sp_stream)
        assert TEST_SP == sp_file_content


def test_save_inventory():
    cluster_model = dict_to_objdict(TEST_CLUSTER_MODEL)
    save_inventory(TEST_INVENTORY, cluster_model)
    with open(os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_INVENTORY_FILE), mode='r', encoding='utf-8') as f:
        inventory_content = f.read()
        assert 'test-1 ansible_host=10.0.0.1' in inventory_content
        assert 'test-2 ansible_host=10.0.0.2' in inventory_content
        assert 'test-3 ansible_host=10.0.0.3' in inventory_content
        assert 'test-4 ansible_host=10.0.0.4' in inventory_content
        assert 'ansible_user=operations' in inventory_content
        assert 'ansible_ssh_private_key_file=id_rsa' in inventory_content


def test_save_ansible_config_file():
    config_file_settings = OrderedDict(ANSIBLE_CONFIG_FILE_SETTINGS)
    ansible_config_file_path = os.path.join(OUTPUT_PATH, CLUSTER_NAME_SAVE, ANSIBLE_OUTPUT_DIR, ANSIBLE_CFG_FILE)
    save_ansible_config_file(config_file_settings, ansible_config_file_path)
    with open(ansible_config_file_path, mode='r', encoding='utf-8') as f:
        ansible_config_file_content = f.read()
        assert 'interpreter_python = auto_legacy_silent' in ansible_config_file_content
        assert 'allow_world_readable_tmpfiles = true' in ansible_config_file_content
