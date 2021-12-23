import glob
import os

import pytest

from cli.helpers.build_io import get_build_path
from cli.helpers.data_loader import load_schema_obj, load_all_schema_objs, load_all_schema_objs_from_directory,\
        load_template_file, load_json_obj, types, SCHEMA_DIR

from tests.unit.helpers.constants import CLUSTER_NAME_LOAD, NON_EXISTING_CLUSTER, TEST_DOCS,  OUTPUT_PATH, TEST_INVENTORY, TEST_JSON,\
    TEST_JSON_NAME, TEST_CLUSTER_MODEL

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
            'name': 'ubuntu',
            'key_path': '/shared/.ssh/epiphany-operations/id_rsa'
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


def test_load_schema_obj():
    yaml_obj = load_schema_obj(types.DEFAULT, 'aws', 'configuration/minimal-cluster-config')
    assert yaml_obj == TEST_MINIMAL_CLUSTER_CONFIG


def test_load_all_schema_objs():
    yaml_objs = load_all_schema_objs(types.DEFAULT, 'aws', 'configuration/minimal-cluster-config')
    assert yaml_objs == [TEST_MINIMAL_CLUSTER_CONFIG]


def test_load_all_schema_objs_from_directory():
    defaults = load_all_schema_objs_from_directory(types.DEFAULT, 'common', 'configuration')
    directory_path = os.path.join(SCHEMA_DIR, 'common', types.DEFAULT, 'configuration')
    assert len(defaults) == len(glob.glob(os.path.join(directory_path, '*.yml')))


def test_load_template_file():
    template = load_template_file(types.ANSIBLE, '', 'inventory')
    content = template.render(inventory=TEST_INVENTORY, cluster_model=TEST_CLUSTER_MODEL)
    assert 'test-1 ansible_host=10.0.0.1' in content
    assert 'test-2 ansible_host=10.0.0.2' in content
    assert 'test-3 ansible_host=10.0.0.3' in content
    assert 'test-4 ansible_host=10.0.0.4' in content
    assert 'ansible_user=operations' in content
    assert 'ansible_ssh_private_key_file=id_rsa' in content


def test_load_json_obj():
    loaded_json = load_json_obj(os.path.join(OUTPUT_PATH, TEST_JSON_NAME))
    assert loaded_json == TEST_JSON


def test_load_not_existing_manifest_docs():
    build_path = get_build_path(NON_EXISTING_CLUSTER)
    with pytest.raises(Exception):
        load_manifest(build_path)
