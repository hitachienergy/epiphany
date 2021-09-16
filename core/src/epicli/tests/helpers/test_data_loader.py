import glob
import os

import pytest

from cli.helpers.build_saver import get_build_path
from tests.helpers.constants import CLUSTER_NAME_LOAD, NON_EXISTING_CLUSTER, TEST_DOCS,  OUTPUT_PATH, TEST_INVENTORY, TEST_JSON,\
    TEST_JSON_NAME, TEST_CLUSTER_MODEL
from cli.helpers.data_loader import get_data_dir_path, get_provider_subdir_path, load_manifest_docs, load_json_obj,\
    load_template_file, load_yaml_obj, load_all_yaml_objs, load_file_from_path, load_all_documents_from_folder, types,\
    DATA_FOLDER_PATH

TEST_MINIMAL_CLUSTER_CONFIG = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'aws',
    'name': 'default',
    'specification':
    {
        'name': 'name',
        'prefix': 'prefix',
        'admin_user':
        {
            'name': 'operations',
            'key_path': '/user/.ssh/epiphany-operations/id_rsa'
        },
        'cloud':
        {
            'k8s_as_cloud_service': False,
            'use_public_ips': False,
            'credentials':
            {
                'key': 'XXXX-XXXX-XXXX',
                'secret': 'XXXXXXXXXXXXXXXX'
            },
            'default_os_image': 'default'
        },
        'components':
        {
            'repository': {'count': 1},
            'kubernetes_master': {'count': 1},
            'kubernetes_node': {'count': 2},
            'logging': {'count': 1},
            'monitoring': {'count': 1},
            'kafka': {'count': 2},
            'postgresql': {'count': 1},
            'load_balancer': {'count': 1},
            'rabbitmq': {'count': 1}
        }
    }
}

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_get_data_dir_path():
    assert get_data_dir_path() == os.path.realpath(os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH))


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
    content = template.render(inventory=TEST_INVENTORY, cluster_model=TEST_CLUSTER_MODEL)
    assert 'test-1 ansible_host=10.0.0.1' in content
    assert 'test-2 ansible_host=10.0.0.2' in content
    assert 'test-3 ansible_host=10.0.0.3' in content
    assert 'test-4 ansible_host=10.0.0.4' in content
    assert 'ansible_user=operations' in content
    assert 'ansible_ssh_private_key_file=id_rsa' in content


def test_load_all_yaml_objs():
    yaml_objs = load_all_yaml_objs(types.DEFAULT, "aws", 'configuration/minimal-cluster-config')
    assert yaml_objs == [TEST_MINIMAL_CLUSTER_CONFIG]


def test_load_yaml_obj():
    yaml_obj = load_yaml_obj(types.DEFAULT, 'aws', 'configuration/minimal-cluster-config')
    assert yaml_obj == TEST_MINIMAL_CLUSTER_CONFIG


def test_load_file_from_path():
    path_to_file = os.path.realpath(
        os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, 'aws', types.DEFAULT, 'configuration/minimal-cluster-config.yml'))
    loaded_file = load_file_from_path(SCRIPT_DIR, path_to_file, types.DEFAULT, 'configuration/minimal-cluster-config')
    assert loaded_file == [TEST_MINIMAL_CLUSTER_CONFIG]


def test_load_all_documents_from_folder():
    defaults = load_all_documents_from_folder('common', 'defaults/configuration')
    directory_path = os.path.join(SCRIPT_DIR, DATA_FOLDER_PATH, 'common', 'defaults/configuration')
    assert len(defaults) == len(glob.glob(os.path.join(directory_path, '*.yml')))
