from typing import List


FILES: List[str] = [
    # --- Exporters ---
    'https://github.com/prometheus/haproxy_exporter/releases/download/v0.10.0/haproxy_exporter-0.10.0.linux-amd64.tar.gz',
    'https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.14.0/jmx_prometheus_javaagent-0.14.0.jar',
    'https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-amd64.tar.gz',
    'https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz',
    'https://github.com/prometheus-community/postgres_exporter/releases/download/v0.9.0/postgres_exporter-0.9.0.linux-amd64.tar.gz',
    # --- Misc ---
    'https://archive.apache.org/dist/kafka/2.6.0/kafka_2.12-2.6.0.tgz',
    'https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz',
    'https://github.com/prometheus/alertmanager/releases/download/v0.17.0/alertmanager-0.17.0.linux-amd64.tar.gz',
    'https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-amd64.tar.gz',
    'https://archive.apache.org/dist/ignite/2.9.1/apache-ignite-2.9.1-bin.zip',
    'https://releases.hashicorp.com/vault/1.7.0/vault_1.7.0_linux_amd64.zip',
    'https://get.helm.sh/helm-v3.2.0-linux-amd64.tar.gz',
    'https://github.com/hashicorp/vault-helm/archive/v0.11.0.tar.gz',
    # --- Helm charts ---
    'https://charts.bitnami.com/bitnami/node-exporter-1.1.2.tgz',
    'https://helm.elastic.co/helm/filebeat/filebeat-7.9.2.tgz',
    # --- Grafana Dashboards <url> <new filename> ---
    # Kubernetes Cluster
    'https://grafana.com/api/dashboards/7249/revisions/1/download=grafana_dashboard_7249.json',
    # Kubernetes cluster monitoring (via Prometheus)
    'https://grafana.com/api/dashboards/315/revisions/3/download=grafana_dashboard_315.json',
    # Node Exporter for Prometheus
    'https://grafana.com/api/dashboards/11074/revisions/9/download=grafana_dashboard_11074.json',
    # Node Exporter Server Metrics
    'https://grafana.com/api/dashboards/405/revisions/8/download=grafana_dashboard_405.json',
    # Postgres Overview
    'https://grafana.com/api/dashboards/455/revisions/2/download=grafana_dashboard_455.json',
    # PostgreSQL Database
    'https://grafana.com/api/dashboards/9628/revisions/7/download=grafana_dashboard_9628.json',
    # RabbitMQ Monitoring
    'https://grafana.com/api/dashboards/4279/revisions/4/download=grafana_dashboard_4279.json',
    # Node Exporter Full
    'https://grafana.com/api/dashboards/1860/revisions/23/download=grafana_dashboard_1860.json',
    # Kafka Exporter Overview
    'https://grafana.com/api/dashboards/7589/revisions/5/download=grafana_dashboard_7589.json',
    # HAproxy Servers | HAproxy
    'https://grafana.com/api/dashboards/367/revisions/3/download=grafana_dashboard_367.json',
    # Docker and Host Monitoring w/ Prometheus
    'https://grafana.com/api/dashboards/179/revisions/5/download=grafana_dashboard_179.json',
    # Kubernetes pod and cluster monitoring (via Prometheus)
    'https://grafana.com/api/dashboards/6663/revisions/1/download=grafana_dashboard_6663.json',
    # RabbitMQ cluster monitoring (via Prometheus)
    'https://grafana.com/api/dashboards/10991/revisions/11/download=grafana_dashboard_10991.json'
]
