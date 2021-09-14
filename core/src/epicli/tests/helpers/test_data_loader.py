import os
import pytest
from cli.helpers.build_saver import get_build_path
from cli.helpers.data_loader import get_data_dir_path, get_provider_subdir_path, load_manifest_docs, load_json_obj,\
    load_template_file, types, DATA_FOLDER_PATH
from tests.helpers.constants import CLUSTER_NAME_LOAD, TEST_DOCS, NON_EXISTING_CLUSTER, OUTPUT_PATH, TEST_INVENTORY, TEST_JSON,\
    TEST_JSON_NAME, TEST_CLUSTER_MODEL

SCRIPT_DIR = "/workspaces/epiphany/core/src/epicli/data"


def test_get_data_dir_path():
    assert get_data_dir_path() == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH))


def test_get_provider_subdir_path():
    assert get_provider_subdir_path("terraform", "aws") == os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, "aws", "terraform"))


def test_load_manifest_docs():
    build_path = get_build_path(CLUSTER_NAME_LOAD)
    docs = load_manifest_docs(build_path)
    assert docs == TEST_DOCS


def test_load_not_existing_manifest_docs():
    build_path = get_build_path(NON_EXISTING_CLUSTER)
    with pytest.raises(Exception):
        load_manifest_docs(build_path)


def test_load_json_obj():
    loaded_json = load_json_obj(os.path.join(OUTPUT_PATH, TEST_JSON_NAME))
    assert loaded_json == TEST_JSON


def test_load_template_file():
    template = load_template_file(types.ANSIBLE, "common", "ansible_inventory")
    content = template.render(inventory=TEST_INVENTORY,
                              cluster_model=TEST_CLUSTER_MODEL)
    assert 'test-1 ansible_host=10.0.0.1' in content
    assert 'test-2 ansible_host=10.0.0.2' in content
    assert 'test-3 ansible_host=10.0.0.3' in content
    assert 'test-4 ansible_host=10.0.0.4' in content
    assert 'ansible_user=operations' in content
    assert 'ansible_ssh_private_key_file=id_rsa' in content
