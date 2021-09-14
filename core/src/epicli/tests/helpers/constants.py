OUTPUT_PATH = '/workspaces/epiphany/core/src/epicli/test_results/'
CLUSTER_NAME_SAVE = 'test-save'
CLUSTER_NAME_LOAD = 'test-load'
NON_EXISTING_CLUSTER = 'test-aaaa'
TEST_DOCS = \
    [{'kind': 'epiphany-cluster',
      'title': 'Epiphany cluster Config',
      'provider': 'any',
      'name': 'default',
      'specification': {'name': 'default',
                        'admin_user': {'name': 'operations', 'key_path': 'id_rsa'}}},
     {'kind': 'infrastructure/machine', 'provider': 'any', 'name': 'default-repository'}]
TEST_JSON = {'kind': 'epiphany-cluster',
      'title': 'Epiphany cluster Config'}
TEST_JSON_NAME = "test.json"