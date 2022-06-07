from typing import Dict, List


INPUT_MANIFEST_DOCS: str = """kind: epiphany-cluster
title: Epiphany cluster Config
provider: azure
name: default
specification:
  name: custom-cluster
  prefix: prefix
  admin_user:
    name: operations
    key_path: /root/id_rsa
  cloud:
    subscription_name: PGGA-Epiphany-Dev
    k8s_as_cloud_service: false
    use_public_ips: true
    default_os_image: default
  components:
    repository:
      count: 1
    kubernetes_master:
      count: 0
    kubernetes_node:
      count: 0
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 0
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 0
    opensearch:
      count: 0
version: 2.0.1dev
---
kind: configuration/feature-mappings
title: Feature mapping to components
name: default
specification:
  mappings:
    kafka:
    - zookeeper
    - jmx-exporter
    - kafka
    - kafka-exporter
    - node-exporter
    - filebeat
    - firewall
    rabbitmq:
    - rabbitmq
    - node-exporter
    - filebeat
    - firewall
    logging:
    - logging
    - opensearch-dashboards
    - node-exporter
    - filebeat
    - firewall
    load_balancer:
    - haproxy
    - node-exporter
    - filebeat
    - firewall
    monitoring:
    - prometheus
    - grafana
    - node-exporter
    - filebeat
    - firewall
    postgresql:
    - postgresql
    - postgres-exporter
    - node-exporter
    - filebeat
    - firewall
    custom:
    - repository
    - image-registry
    - kubernetes-master
    - node-exporter
    - filebeat
    - rabbitmq
    - postgresql
    - prometheus
    - grafana
    - node-exporter
    - logging
    - firewall
    - rook
    single_machine:
    - repository
    - image-registry
    - kubernetes-master
    - helm
    - applications
    - rabbitmq
    - postgresql
    - firewall
    - rook
    kubernetes_master:
    - kubernetes-master
    - helm
    - applications
    - rook
    - node-exporter
    - filebeat
    - firewall
    kubernetes_node:
    - kubernetes-node
    - node-exporter
    - filebeat
    - firewall
    opensearch:
    - opensearch
    - node-exporter
    - filebeat
    - firewall
    repository:
    - repository
    - image-registry
    - firewall
    - filebeat
    - node-exporter
version: 2.0.1dev
provider: azure
"""


EXPECTED_PARSED_MANIFEST_DOCS: List[Dict] = [
    {'kind': 'epiphany-cluster',
     'title': 'Epiphany cluster Config',
     'provider': 'azure',
     'name': 'default',
     'specification': {
         'name': 'custom-cluster',
         'prefix': 'prefix',
         'admin_user': {
             'name': 'operations',
             'key_path': '/root/id_rsa'
         },
         'cloud': {
             'subscription_name': 'PGGA-Epiphany-Dev',
             'k8s_as_cloud_service': False,
             'use_public_ips': True,
             'default_os_image': 'default'
         },
         'components': {
             'repository':        { 'count': 1 },
             'kubernetes_master': { 'count': 0 },
             'kubernetes_node':   { 'count': 0 },
             'logging':           { 'count': 0 },
             'monitoring':        { 'count': 0 },
             'kafka':             { 'count': 0 },
             'postgresql':        { 'count': 0 },
             'load_balancer':     { 'count': 0 },
             'rabbitmq':          { 'count': 0 },
             'opensearch':        { 'count': 0 }
         }
     },
     'version': '2.0.1dev'
    },
    {'kind': 'configuration/feature-mappings',
     'title': 'Feature mapping to components',
     'name': 'default',
     'specification': {
         'mappings': {
             'kafka': [
                 'zookeeper',
                 'jmx-exporter',
                 'kafka',
                 'kafka-exporter',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'rabbitmq': [
                 'rabbitmq',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'logging': [
                 'logging',
                 'opensearch-dashboards',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'load_balancer': [
                 'haproxy',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'monitoring': [
                 'prometheus',
                 'grafana',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'postgresql': [
                 'postgresql',
                 'postgres-exporter',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'custom': [
                 'repository',
                 'image-registry',
                 'kubernetes-master',
                 'node-exporter',
                 'filebeat',
                 'rabbitmq',
                 'postgresql',
                 'prometheus',
                 'grafana',
                 'node-exporter',
                 'logging',
                 'firewall',
                 'rook'
             ],
             'single_machine': [
                 'repository',
                 'image-registry',
                 'kubernetes-master',
                 'helm',
                 'applications',
                 'rabbitmq',
                 'postgresql',
                 'firewall',
                 'rook'
             ],
             'kubernetes_master': [
                 'kubernetes-master',
                 'helm',
                 'applications',
                 'rook',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'kubernetes_node': [
                 'kubernetes-node',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'opensearch': [
                 'opensearch',
                 'node-exporter',
                 'filebeat',
                 'firewall'
             ],
             'repository': [
                 'repository',
                 'image-registry',
                 'firewall',
                 'filebeat',
                 'node-exporter'
             ]
         }
     },
     'version': '2.0.1dev',
     'provider': 'azure'
    }
]


INPUT_DOC_TO_UPDATE_BASE = [
    {'kind': 'epiphany-cluster',
     'title': 'Epiphany cluster Config',
     'provider': 'azure',
     'name': 'default',
     'specification': {
         'name': 'custom-cluster',
         'prefix': 'prefix',
         'admin_user': {
             'name': 'operations',
             'key_path': '/root/id_rsa'
         },
         'cloud': {
             'subscription_name': 'PGGA-Epiphany-Dev',
             'k8s_as_cloud_service': False,
             'use_public_ips': True,
             'default_os_image': 'default'
         },
         'components': {
             'repository':        { 'count': 1 },
             'kubernetes_master': { 'count': 0 },
             'kubernetes_node':   { 'count': 0 },
             'logging':           { 'count': 0 },
             'monitoring':        { 'count': 0 },
             'kafka':             { 'count': 0 },
             'postgresql':        { 'count': 0 },
             'load_balancer':     { 'count': 0 },
             'rabbitmq':          { 'count': 0 },
             'opensearch':        { 'count': 0 }
         }
     },
     'version': '2.0.1dev'
    },
    {'kind': 'infrastructure/virtual-machine',
     'title': 'Virtual Machine Infra',
     'provider': 'azure',
     'name': 'load-balancer-machine',
     'specification': {
         'size': 'Standard_DS1_v2',
         'security': {
             'rules': [
                 {'_merge': True},
                 {'name': 'haproxy_metrics',
                  'description': 'Allow haproxy_metrics traffic',
                  'priority': 201,
                  'direction': 'Inbound',
                  'access': 'Allow',
                  'protocol': 'Tcp',
                  'source_port_range': '*',
                  'destination_port_range': 9101,
                  'source_address_prefix': '10.1.0.0/20',
                  'destination_address_prefix': '0.0.0.0/0'}
             ]
         }
     },
     'version': '2.0.1dev'
    },
]


INPUT_DOC_TO_UPDATE_TWO_INFRA_DOCS = (INPUT_DOC_TO_UPDATE_BASE +
    [{'kind': 'infrastructure/virtual-machine',
      'title': 'Some infrastructure doc',
      'provider': 'azure',
      'name': 'some-machine',
      'specification': {
          'field': False,
      },
      'version': '2.0.1dev'
     }])


EXPECTED_UPDATED_DOC_BASE = [
    {'kind': 'epiphany-cluster',
     'title': 'Epiphany cluster Config',
     'provider': 'azure',
     'name': 'default',
     'specification': {
         'name': 'custom-cluster',
         'prefix': 'prefix',
         'admin_user': {
             'name': 'operations',
             'key_path': '/root/id_rsa'
         },
         'cloud': {
             'subscription_name': 'PGGA-Epiphany-Dev',
             'k8s_as_cloud_service': False,
             'use_public_ips': True,
             'default_os_image': 'default'
         },
         'components': {
             'repository':        { 'count': 1 },
             'kubernetes_master': { 'count': 0 },
             'kubernetes_node':   { 'count': 0 },
             'logging':           { 'count': 0 },
             'monitoring':        { 'count': 0 },
             'kafka':             { 'count': 0 },
             'postgresql':        { 'count': 0 },
             'load_balancer':     { 'count': 0 },
             'rabbitmq':          { 'count': 0 },
             'opensearch':        { 'count': 0 }
         }
     },
     'version': '2.0.1dev'
    },
    {'kind': 'infrastructure/virtual-machine',
     'title': 'Virtual Machine Infra',
     'provider': 'azure',
     'name': 'load-balancer-machine',
     'specification': {
         'size': 'Standard_DS1_v2',
         'security': {
             'rules': [
                 {'_merge': True},
                 {'name': 'haproxy_metrics',
                  'description': 'Allow haproxy_metrics traffic',
                  'priority': 201,
                  'direction': 'Inbound',
                  'access': 'Allow',
                  'protocol': 'Tcp',
                  'source_port_range': '*',
                  'destination_port_range': 9101,
                  'source_address_prefix': '10.1.0.0/20',
                  'destination_address_prefix': '0.0.0.0/0'}
             ]
         }
     },
     'version': '2.0.1dev'
    },
]


EXPECTED_UPDATED_DOC_WITH_TWO_INFRA_DOCS = (EXPECTED_UPDATED_DOC_BASE +
    [{'kind': 'infrastructure/virtual-machine',
      'title': 'Some infrastructure doc',
      'provider': 'azure',
      'name': 'some-machine',
      'specification': {
          'field': True,
      },
      'version': '2.0.1dev'
     }])


EXPECTED_UPDATED_DOC_WITH_NEW_DOC_ADDED = (EXPECTED_UPDATED_DOC_BASE +
    [{'kind': 'some/other',
      'title': 'Some other doc',
      'provider': 'azure',
      'version': '2.0.1dev'
     }])
