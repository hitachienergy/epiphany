CLUSTER_DOC_ANY = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'any',
    'name': 'default',
    'specification': {
        'name': 'test',
        'admin_user': {
            'name': 'operations',
            'key_path': '/shared/.ssh/epiphany-operations/id_rsa'},
        'components': {
            'repository': {
                'count': 1,
                'machines': ['default-repository']},
            'kubernetes_master': {
                'count': 1,
                'machines': ['default-k8s-master1']},
            'kubernetes_node': {
                'count': 2,
                'machines': ['default-k8s-node1', 'default-k8s-node2']},
            'logging': {
                'count': 1,
                'machines': ['default-logging']},
            'monitoring': {
                'count': 1,
                'machines': ['default-monitoring']},
            'kafka': {
                'count': 2,
                'machines': ['default-kafka1', 'default-kafka2']},
            'postgresql': {
                'count': 1,
                'machines': ['default-postgresql']},
            'load_balancer': {
                'count': 1,
                'machines': ['default-loadbalancer']},
            'rabbitmq': {
                'count': 1,
                'machines': ['default-rabbitmq']},
            'opensearch': {
                'count': 1,
                'machines': ['default-opensearch']}
        }
    },
    'version': '2.0.1dev'
}


EXPECTED_CLUSTER_DOC_ANY = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'any',
    'name': 'default',
    'specification': {
        'name': 'test',
        'components': {
            'repository': {
                'count': 1,
                'machines': ['default-repository']},
            'kubernetes_master': {
                'count': 1,
                'machines': ['default-k8s-master1']},
            'kubernetes_node': {
                'count': 2,
                'machines': ['default-k8s-node1', 'default-k8s-node2']},
            'logging': {
                'count': 1,
                'machines': ['default-logging']},
            'monitoring': {
                'count': 1,
                'machines': ['default-monitoring']},
            'kafka': {
                'count': 2,
                'machines': ['default-kafka1', 'default-kafka2']},
            'postgresql': {
                'count': 1,
                'machines': ['default-postgresql']},
            'load_balancer': {
                'count': 1,
                'machines': ['default-loadbalancer']},
            'rabbitmq': {
                'count': 1,
                'machines': ['default-rabbitmq']},
            'opensearch': {
                'count': 1,
                'machines': ['default-opensearch']}
        }
    },
    'version': '2.0.1dev'
}


CLUSTER_DOC_AZURE = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'azure',
    'name': 'default',
    'specification': {
        'name': 'test',
        'prefix': 'prefix',
        'admin_user': {
            'name': 'operations',
            'key_path': '/shared/.ssh/epiphany-operations/id_rsa'},
        'cloud': {
            'subscription_name': 'YOUR-SUB-NAME',
            'k8s_as_cloud_service': False,
            'use_public_ips': False,
            'default_os_image': 'default'},
        'components': {
            'repository': {'count': 1},
            'kubernetes_master': {'count': 1},
            'kubernetes_node': {'count': 2},
            'logging': {'count': 1},
            'monitoring': {'count': 1},
            'kafka': {'count': 2},
            'postgresql': {'count': 1},
            'load_balancer': {'count': 1},
            'rabbitmq': {'count': 1},
            'opensearch': {'count': 1}
        }
    },
    'version': '2.0.1dev'
}


EXPECTED_CLUSTER_DOC_AZURE = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'azure',
    'name': 'default',
    'specification': {
        'name': 'test',
        'prefix': 'prefix',
        'cloud': {
            'k8s_as_cloud_service': False,
            'use_public_ips': False,
            'default_os_image': 'default'},
        'components': {
            'repository': {'count': 1},
            'kubernetes_master': {'count': 1},
            'kubernetes_node': {'count': 2},
            'logging': {'count': 1},
            'monitoring': {'count': 1},
            'kafka': {'count': 2},
            'postgresql': {'count': 1},
            'load_balancer': {'count': 1},
            'rabbitmq': {'count': 1},
            'opensearch': {'count': 1}
        }
    },
    'version': '2.0.1dev'
}

CLUSTER_DOC_AWS = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'aws',
    'name': 'default',
    'specification': {
        'name': 'test',
        'prefix': 'prefix',
        'admin_user': {
            'name': 'ubuntu',
            'key_path': '/shared/.ssh/epiphany-operations/id_rsa'},
        'cloud': {
            'k8s_as_cloud_service': False,
            'use_public_ips': False,
            'credentials': {
                'access_key_id': 'XXXX-XXXX-XXXX',
                'secret_access_key': 'XXXXXXXXXXXXXXXX'},
            'default_os_image': 'default'
        },
        'components': {
            'repository': {'count': 1},
            'kubernetes_master': {'count': 1},
            'kubernetes_node': {'count': 2},
            'logging': {'count': 1},
            'monitoring': {'count': 1},
            'kafka': {'count': 2},
            'postgresql': {'count': 1},
            'load_balancer': {'count': 1},
            'rabbitmq': {'count': 1},
            'opensearch': {'count': 1}
        }
    },
    'version': '2.0.1dev'
}


EXPECTED_CLUSTER_DOC_AWS = {
    'kind': 'epiphany-cluster',
    'title': 'Epiphany cluster Config',
    'provider': 'aws',
    'name': 'default',
    'specification': {
        'name': 'test',
        'prefix': 'prefix',
        'cloud': {
            'k8s_as_cloud_service': False,
            'use_public_ips': False,
            'default_os_image': 'default'
        },
        'components': {
            'repository': {'count': 1},
            'kubernetes_master': {'count': 1},
            'kubernetes_node': {'count': 2},
            'logging': {'count': 1},
            'monitoring': {'count': 1},
            'kafka': {'count': 2},
            'postgresql': {'count': 1},
            'load_balancer': {'count': 1},
            'rabbitmq': {'count': 1},
            'opensearch': {'count': 1}
        }
    },
    'version': '2.0.1dev'
}


COMMON_DOCS = [
    {
        'kind': 'configuration/feature-mappings',
        'title': 'Feature mapping to components',
        'name': 'default'
    },
    {
        'kind': 'configuration/image-registry',
        'title': 'Epiphany image registry',
        'name': 'default'
    }
]


NOT_NEEDED_DOCS = [
    {
        'kind': 'infrastructure/machine',
        'provider': 'any',
        'name': 'default-loadbalancer',
        'specification': {
            'hostname': 'loadbalancer',
            'ip': '192.168.100.110'
        },
        'version': '2.0.1dev'
    },
    {
        'kind': 'infrastructure/machine',
        'provider': 'any',
        'name': 'default-rabbitmq',
        'specification': {
          'hostname': 'rabbitmq',
          'ip': '192.168.100.111'
        },
        'version': '2.0.1dev'
    },
    {
        'kind': 'infrastructure/machine',
        'provider': 'any',
        'name': 'default-opensearch',
        'specification': {
          'hostname': 'opensearch',
          'ip': '192.168.100.112'
        },
        'version': '2.0.1dev'
    }
]


MANIFEST_WITH_ADDITIONAL_DOCS = [ CLUSTER_DOC_ANY ] + COMMON_DOCS + NOT_NEEDED_DOCS
