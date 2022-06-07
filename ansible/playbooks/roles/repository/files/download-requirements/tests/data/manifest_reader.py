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
version: 2.0.0dev
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
version: 2.0.0dev
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
version: 2.0.0dev
{FEATURE_MAPPINGS}
"""


INPUT_MANIFEST_WITH_IMAGES = f"""
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
      count: 0
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 0
    opensearch:
      count: 0
version: 2.0.0dev
{FEATURE_MAPPINGS}
---
kind: configuration/image-registry
title: Epiphany image registry
name: default
specification:
  description: Local registry with Docker images
  registry_image:
    name: registry:2.8.0
    file_name: registry-2.8.0.tar
  images_to_load:
    x86_64:
      generic:
        applications:
          - name: epiphanyplatform/keycloak:14.0.0
            file_name: keycloak-14.0.0.tar
        rabbitmq:
          - name: rabbitmq:3.8.9
            file_name: rabbitmq-3.8.9.tar
        kubernetes-master:
          - name: kubernetesui/dashboard:v2.3.1
            file_name: dashboard-v2.3.1.tar
          - name: kubernetesui/metrics-scraper:v1.0.7
            file_name: metrics-scraper-v1.0.7.tar
        postgresql:
          - name: bitnami/pgpool:4.2.4
            file_name: pgpool-4.2.4.tar
      current:
        haproxy:
          - name: haproxy:2.2.2-alpine
            file_name: haproxy-2.2.2-alpine.tar
        kubernetes-master:
          - name: k8s.gcr.io/kube-apiserver:v1.22.4
            file_name: kube-apiserver-v1.22.4.tar
          - name: k8s.gcr.io/kube-controller-manager:v1.22.4
            file_name: kube-controller-manager-v1.22.4.tar
      legacy:
        kubernetes-master:
          - name: k8s.gcr.io/kube-apiserver:v1.21.7
            file_name: kube-apiserver-v1.21.7.tar
          - name: k8s.gcr.io/kube-controller-manager:v1.21.7
            file_name: kube-controller-manager-v1.21.7.tar
          - name: k8s.gcr.io/kube-proxy:v1.21.7
            file_name: kube-proxy-v1.21.7.tar
          - name: k8s.gcr.io/kube-scheduler:v1.21.7
            file_name: kube-scheduler-v1.21.7.tar
          - name: k8s.gcr.io/coredns/coredns:v1.8.0
            file_name: coredns-v1.8.0.tar
          - name: k8s.gcr.io/etcd:3.4.13-0
            file_name: etcd-3.4.13-0.tar
          - name: k8s.gcr.io/pause:3.4.1
            file_name: pause-3.4.1.tar
    aarch64:
      generic:
        applications:
          - name: epiphanyplatform/keycloak:14.0.0
            file_name: keycloak-14.0.0.tar
        rabbitmq:
          - name: rabbitmq:3.8.9
            file_name: rabbitmq-3.8.9.tar
        kubernetes-master:
          - name: kubernetesui/dashboard:v2.3.1
            file_name: dashboard-v2.3.1.tar
          - name: kubernetesui/metrics-scraper:v1.0.7
            file_name: metrics-scraper-v1.0.7.tar
      current:
        haproxy:
          - name: haproxy:2.2.2-alpine
            file_name: haproxy-2.2.2-alpine.tar
        kubernetes-master:
          - name: k8s.gcr.io/kube-apiserver:v1.22.4
            file_name: kube-apiserver-v1.22.4.tar
      legacy:
        kubernetes-master:
          - name: k8s.gcr.io/kube-apiserver:v1.21.7
            file_name: kube-apiserver-v1.21.7.tar
          - name: k8s.gcr.io/kube-scheduler:v1.21.7
            file_name: kube-scheduler-v1.21.7.tar
          - name: k8s.gcr.io/coredns/coredns:v1.8.0
            file_name: coredns-v1.8.0.tar
          - name: k8s.gcr.io/etcd:3.4.13-0
            file_name: etcd-3.4.13-0.tar
          - name: k8s.gcr.io/pause:3.4.1
            file_name: pause-3.4.1.tar
version: 2.0.1dev
provider: any
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
version: 2.0.0dev
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
                           'zookeeper'],
    'requested-images': []
}


EXPECTED_FEATURE_MAPPINGS_WITH_DASHBOARDS = {
    'requested-components': ['monitoring', 'repository'],
    'requested-features': ['filebeat',
                           'firewall',
                           'grafana',
                           'image-registry',
                           'node-exporter',
                           'prometheus',
                           'repository'],
    'requested-images': []
}


EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_X86_64 = {
    'requested-components': ['repository'],
    'requested-features': ['filebeat',
                           'firewall',
                           'image-registry',
                           'node-exporter',
                           'repository'],
    'requested-images': [
        'bitnami/pgpool:4.2.4',
        'epiphanyplatform/keycloak:14.0.0',
        'haproxy:2.2.2-alpine',
        'k8s.gcr.io/coredns/coredns:v1.8.0',
        'k8s.gcr.io/etcd:3.4.13-0',
        'k8s.gcr.io/kube-apiserver:v1.21.7',
        'k8s.gcr.io/kube-apiserver:v1.22.4',
        'k8s.gcr.io/kube-controller-manager:v1.21.7',
        'k8s.gcr.io/kube-controller-manager:v1.22.4',
        'k8s.gcr.io/kube-proxy:v1.21.7',
        'k8s.gcr.io/kube-scheduler:v1.21.7',
        'k8s.gcr.io/pause:3.4.1',
        'kubernetesui/dashboard:v2.3.1',
        'kubernetesui/metrics-scraper:v1.0.7',
        'rabbitmq:3.8.9',
        'registry:2.8.0'
    ]
}


EXPECTED_FEATURE_MAPPINGS_WITH_IMAGES_ARM64 = {
    'requested-components': ['repository'],
    'requested-features': ['filebeat',
                           'firewall',
                           'image-registry',
                           'node-exporter',
                           'repository'],
    'requested-images': [
        'epiphanyplatform/keycloak:14.0.0',
        'haproxy:2.2.2-alpine',
        'k8s.gcr.io/coredns/coredns:v1.8.0',
        'k8s.gcr.io/etcd:3.4.13-0',
        'k8s.gcr.io/kube-apiserver:v1.21.7',
        'k8s.gcr.io/kube-apiserver:v1.22.4',
        'k8s.gcr.io/kube-scheduler:v1.21.7',
        'k8s.gcr.io/pause:3.4.1',
        'kubernetesui/dashboard:v2.3.1',
        'kubernetesui/metrics-scraper:v1.0.7',
        'rabbitmq:3.8.9',
        'registry:2.8.0'
    ]
}
