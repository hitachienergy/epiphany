FEATURE_MAPPINGS = """
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


INPUT_MANIFEST_FEATURE_MAPPINGS = f"""
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
      count: 0
    kafka:
      count: 2
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 0
    opensearch:
      count: 0
version: 2.0.1dev
{FEATURE_MAPPINGS}
"""


INPUT_MANIFEST_WITH_DASHBOARDS = f"""
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
{FEATURE_MAPPINGS}
"""


INPUT_MANIFEST_IMAGES_NO_DOCUMENT = f"""
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
      count: 0
    kafka:
      count: 2
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 1
    opensearch:
      count: 0
version: 2.0.1dev
{FEATURE_MAPPINGS}
"""


INPUT_MANIFEST_WITH_K8S_AS_CLOUD_SERVICE = f"""
kind: epiphany-cluster
title: Epiphany cluster Config
provider: any
name: default
specification:
  name: new_cluster
  admin_user:
    name: operations
    key_path: /shared/.ssh/epiphany-operations/id_rsa
  cloud:
    k8s_as_cloud_service: true
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
{FEATURE_MAPPINGS}
"""


EXPECTED_FEATURE_MAPPINGS = {
    'requested-components': ['kafka', 'repository'],
    'requested-features': ['filebeat',
                           'firewall',
                           'image-registry',
                           'jmx-exporter',
                           'kafka',
                           'kafka-exporter',
                           'node-exporter',
                           'repository',
                           'zookeeper']
}


EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS = {
    'requested-components': ['monitoring', 'repository'],
    'requested-features': ['filebeat',
                           'firewall',
                           'grafana',
                           'image-registry',
                           'node-exporter',
                           'prometheus',
                           'repository']
}
