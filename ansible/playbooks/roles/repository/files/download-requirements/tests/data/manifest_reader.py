INPUT_MANIFEST_FEATURE_MAPPINGS = """
---
kind: epiphany-cluster
title: Epiphany cluster Config
provider: any
name: default
specification:
  name: new_cluster
  admin_user:
    name: operations
    key_path: /shared/.ssh/epiphany-operations/id_rsa
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
      count: 1
    kafka:
      count: 2
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 0
    opendistro_for_elasticsearch:
      count: 0
version: 2.0.0dev
---
kind: configuration/feature-mappings
title: Feature mapping to roles
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
    - kibana
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
    opendistro_for_elasticsearch:
    - opendistro-for-elasticsearch
    - node-exporter
    - filebeat
    - firewall
    repository:
    - repository
    - image-registry
    - firewall
    - filebeat
    - node-exporter
version: 2.0.0dev
provider: azure
"""


EXPECTED_FEATURE_MAPPINGS = {
    'detected-components': ['kafka', 'monitoring', 'repository'],
    'detected-features': ['filebeat',
                          'firewall',
                          'grafana',
                          'image-registry',
                          'jmx-exporter',
                          'kafka',
                          'kafka-exporter',
                          'node-exporter',
                          'prometheus',
                          'repository',
                          'zookeeper']
}
