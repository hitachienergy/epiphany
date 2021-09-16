OUTPUT_PATH = '/workspaces/epiphany/core/src/epicli/test_results/'
CLUSTER_NAME_SAVE = 'test-save'
CLUSTER_NAME_LOAD = 'test-load'
NON_EXISTING_CLUSTER = 'test-aaaa'
TEST_DOCS = [
    {
        'kind': 'epiphany-cluster',
        'title': 'Epiphany cluster Config',
        'provider': 'any',
        'name': 'default',
        'specification':
        {
            'name': 'default',
            'admin_user':
            {
                'name': 'operations',
                'key_path': 'id_rsa'
            }
        }
    },
    {
        'kind': 'infrastructure/machine',
        'provider': 'any',
        'name': 'default-repository'
    }
]
TEST_JSON = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config'
}
TEST_JSON_NAME = "test.json"
TEST_CLUSTER_MODEL = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'azure',
    'name': CLUSTER_NAME_SAVE,
    'specification':
    {
        'prefix': 'test',
        'name': CLUSTER_NAME_SAVE,
        'admin_user':
        {
            'name': 'operations',
            'key_path': 'id_rsa'
        },
        'cloud':
        {
            'subscription_name': 'Test-Dev',
            'vnet_address_pool': '10.1.0.0/20',
            'use_public_ips': False,
            'use_service_principal': False,
            'region': 'West Europe',
            'credentials': {
                'key': '1111-1111-1111',
                'secret': 'XXXXXXXXXXXXXXX'
            },
            'default_os_image': 'default'
        },
    }
}
TEST_INVENTORY = [{
    'hosts':
    [{'ip': '10.0.0.1',
      'name': 'test-1'},
     {'ip': '10.0.0.2',
     'name': 'test-2'}],
    'role': 'postgresql'
},
    {
    'hosts':
    [{'ip': '10.0.0.3',
      'name': 'test-3'},
     {'ip': '10.0.0.4',
     'name': 'test-4'}],
    'role': 'filebeat'
}]
