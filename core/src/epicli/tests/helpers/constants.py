CLUSTER_NAME_SAVE = 'test-save'
CLUSTER_NAME_LOAD = 'test-load'
TEST_DOCS = \
    [{'kind': 'epiphany-cluster',
      'title': 'Epiphany cluster Config',
      'provider': 'any',
      'name': 'default',
      'specification': {'name': 'default',
                        'admin_user': {'name': 'operations', 'key_path': 'id_rsa'}}},
     {'kind': 'infrastructure/machine', 'provider': 'any', 'name': 'default-repository'}]