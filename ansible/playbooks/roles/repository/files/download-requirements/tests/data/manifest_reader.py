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
    logging:
      - opensearch
      - opensearch-dashboards
      - node-exporter
      - filebeat
      - firewall
    monitoring:
      - prometheus
      - grafana
      - node-exporter
      - filebeat
      - firewall
    custom:
      - repository
      - node-exporter
      - filebeat
      - prometheus
      - grafana
      - node-exporter
      - opensearch
      - firewall
    single_machine:
      - repository
      - firewall
    repository:
      - repository
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
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 2
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
    logging:
      count: 0
    monitoring:
      count: 1
    kafka:
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
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 2
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
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 0
version: 2.0.1dev
{FEATURE_MAPPINGS}
"""


EXPECTED_FEATURE_MAPPINGS = {
    'requested-components': ['kafka', 'repository'],
    'requested-features': ['filebeat',
                           'firewall',
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
                           'node-exporter',
                           'prometheus',
                           'repository']
}
