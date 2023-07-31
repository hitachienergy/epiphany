from typing import Dict


FILE_REQUIREMENTS = """
files:
  # --- Exporters ---
  kafka-exporter:
    options:
      - url: 'https://github.com/danielqsj/kafka_exporter/releases/download/v1.4.0/kafka_exporter-1.4.0.linux-amd64.tar.gz'
        sha256: ffda682e82daede726da8719257a088f8e23dcaa4e2ac8b2b2748a129aea85f0
    deps: [kafka-exporter]

  jmx-prometheus-javaagent:
    options:
      - url: 'https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar'
        sha256: 0ddc6834f854c03d5795305193c1d33132a24fbd406b4b52828602f5bc30777e
    deps: [kafka]

  node-exporter:
    options:
      - url: 'https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz'
        sha256: 68f3802c2dd3980667e4ba65ea2e1fb03f4a4ba026cca375f15a0390ff850949
    deps: [node-exporter]

  postgres-exporter:
    options:
      - url: 'https://github.com/prometheus-community/postgres_exporter/releases/download/v0.10.0/postgres_exporter-0.10.0.linux-amd64.tar.gz'
        sha256: 1d1a008c5e29673b404a9ce119b7516fa59974aeda2f47d4a0446d102abce8a1
    deps: [postgres-exporter]

  # --- Misc ---
  kafka:
    options:
      - url: 'https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz'
        sha256: 175a4134efc569a586d58916cd16ce70f868b13dea2b5a3d12a67b1395d59f98
    deps: [kafka]

  apache-zookeeper:
    options:
      - url: 'https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz'
        sha256: c35ed6786d59b73920243f1a324d24c2ddfafb379041d7a350cc9a341c52caf3
    deps: [zookeeper]

  alertmanager:
    options:
      - url: 'https://github.com/prometheus/alertmanager/releases/download/v0.23.0/alertmanager-0.23.0.linux-amd64.tar.gz'
        sha256: 77793c4d9bb92be98f7525f8bc50cb8adb8c5de2e944d5500e90ab13918771fc
    deps: [prometheus]

  prometheus:
    options:
      - url: 'https://github.com/prometheus/prometheus/releases/download/v2.31.1/prometheus-2.31.1.linux-amd64.tar.gz'
        sha256: 7852dc11cfaa039577c1804fe6f082a07c5eb06be50babcffe29214aedf318b3
    deps: [prometheus]

  # --- Helm charts ---
  node-exporter-chart:
    options:
      - url: 'https://charts.bitnami.com/bitnami/node-exporter-2.3.17.tgz'
        sha256: ec586fabb775a4f05510386899cf348391523c89ff5a1d4097b0592e675ade7f
    deps: [kubernetes-master, k8s-as-cloud-service]

  filebeat-chart:
    options:
      - url: 'https://helm.elastic.co/helm/filebeat/filebeat-7.12.1.tgz'
        sha256: 5838058fe06372390dc335900a7707109cc7287a84164ca245d395af1f9c0a79
    deps: [kubernetes-master, k8s-as-cloud-service]

  # --- OpenSearch Bundle ---
  opensearch:
    options:
      - url: 'https://artifacts.opensearch.org/releases/bundle/opensearch/1.2.4/opensearch-1.2.4-linux-x64.tar.gz'
        sha256: d40f2696623b6766aa235997e2847a6c661a226815d4ba173292a219754bd8a8
    deps: [opensearch]

  opensearch-dashboards:
    options:
      - url: 'https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/1.2.0/opensearch-dashboards-1.2.0-linux-x64.tar.gz'
        sha256: 14623798e61be6913e2a218d6ba3e308e5036359d7bda58482ad2f1340aa3c85
    deps: [opensearch-dashboards]

  opensearch-perf-top:
    options:
      - url: 'https://github.com/opensearch-project/perftop/releases/download/1.2.0.0/opensearch-perf-top-1.2.0.0-linux-x64.zip'
        sha256: e8f9683976001a8cf59a9f86da5caafa10b88643315f0af2baa93a9354d41e2b
    deps: [opensearch]
"""


DASHBOARD_REQUIREMENTS = """
grafana-dashboards:
  grafana_dashboard_7249:
    url: 'https://grafana.com/api/dashboards/7249/revisions/1/download'
    sha256: 41cc2794b1cc9fc537baf045fee12d086d23632b4c8b2e88985274bb9862e731
  grafana_dashboard_315:
    url: 'https://grafana.com/api/dashboards/315/revisions/3/download'
    sha256: ee46dd6e68a9950aa78e8c88ae5e565c8ebde6cbdbe08972a70f06c5486618fb
  grafana_dashboard_11074:
    url: 'https://grafana.com/api/dashboards/11074/revisions/9/download'
    sha256: 893f4029ee9b3e0797ebad989dd47b8df516ed4d078f28ded2d6d8df7bbd1065
  grafana_dashboard_405:
    url: 'https://grafana.com/api/dashboards/405/revisions/8/download'
    sha256: 97675027cbd5b7241e93a2b598654c4b466bc909eeb6358ba123d500094d913c
  grafana_dashboard_455:
    url: 'https://grafana.com/api/dashboards/455/revisions/2/download'
    sha256: c66b91ab8d258b0dc005d3ee4dac3a5634a627c79cc8053875f76ab1e369a362
  grafana_dashboard_9628:
    url: 'https://grafana.com/api/dashboards/9628/revisions/7/download'
    sha256: c64cc38ad9ebd7af09551ee83e669a38f62a76e7c80929af5668a5852732b376
  grafana_dashboard_4279:
    url: 'https://grafana.com/api/dashboards/4279/revisions/4/download'
    sha256: 74d47be868da52c145240ab5586d91ace9e9218ca775af988f9d60e501907a25
  grafana_dashboard_1860:
    url: 'https://grafana.com/api/dashboards/1860/revisions/23/download'
    sha256: 225faab8bf35c1723af14d4c069882ccb92b455d1941c6b1cf3d95a1576c13d7
  grafana_dashboard_7589:
    url: 'https://grafana.com/api/dashboards/7589/revisions/5/download'
    sha256: cf020e14465626360418e8b5746818c80d77c0301422f3060879fddc099c2151
  grafana_dashboard_789:
    url: 'https://grafana.com/api/dashboards/789/revisions/1/download'
    sha256: 6a9b4bdc386062287af4f7d56781103a2e45a51813596a65f03c1ae1d4d3e919
  grafana_dashboard_179:
    url: 'https://grafana.com/api/dashboards/179/revisions/7/download'
    sha256: 8d67350ff74e715fb1463f2406f24a73377357d90344f8200dad9d1b2a8133c2
  grafana_dashboard_6663:
    url: 'https://grafana.com/api/dashboards/6663/revisions/1/download'
    sha256: d544d88069e1b793ff3d8f6970df641ad9a66217e69b629621e1ecbb2f06aa05
  grafana_dashboard_10991:
    url: 'https://grafana.com/api/dashboards/10991/revisions/11/download'
    sha256: 66340fa3256d432287cba75ab5177eb058c77afa7d521a75d58099f95b1bff50
"""

IMAGE_REQUIREMENTS = """
images: {}
"""


ALL_REQUIREMENTS: Dict[str, Dict] = {
    'files': {
        'https://github.com/danielqsj/kafka_exporter/releases/download/v1.4.0/kafka_exporter-1.4.0.linux-amd64.tar.gz': {
            'sha256': 'ffda682e82daede726da8719257a088f8e23dcaa4e2ac8b2b2748a129aea85f0',
            'deps': ['kafka-exporter']
        },
        'https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar': {
            'sha256': '0ddc6834f854c03d5795305193c1d33132a24fbd406b4b52828602f5bc30777e',
            'deps': ['kafka']
        },
        'https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz': {
            'sha256': '68f3802c2dd3980667e4ba65ea2e1fb03f4a4ba026cca375f15a0390ff850949',
            'deps': ['node-exporter']
        },
        'https://github.com/prometheus-community/postgres_exporter/releases/download/v0.10.0/postgres_exporter-0.10.0.linux-amd64.tar.gz': {
            'sha256': '1d1a008c5e29673b404a9ce119b7516fa59974aeda2f47d4a0446d102abce8a1',
            'deps': ['postgres-exporter']
        }
    },
    'grafana-dashboards': {
        'grafana_dashboard_7249': {
            'url': 'https://grafana.com/api/dashboards/7249/revisions/1/download',
            'sha256': '41cc2794b1cc9fc537baf045fee12d086d23632b4c8b2e88985274bb9862e731'
        },
        'grafana_dashboard_315': {
            'url': 'https://grafana.com/api/dashboards/315/revisions/3/download',
            'sha256': 'ee46dd6e68a9950aa78e8c88ae5e565c8ebde6cbdbe08972a70f06c5486618fb'
        },
        'grafana_dashboard_11074': {
            'url': 'https://grafana.com/api/dashboards/11074/revisions/9/download',
            'sha256': '893f4029ee9b3e0797ebad989dd47b8df516ed4d078f28ded2d6d8df7bbd1065'
        }
    },
    'images': {},
    'packages': {}
}


EXPECTED_VERBOSE_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components requested:
- kafka
- repository

Features requested:
- filebeat
- firewall
- jmx-exporter
- kafka
- kafka-exporter
- node-exporter
- repository
- zookeeper
--------------------------------------------------
"""


EXPECTED_VERBOSE_DASHBOARD_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components requested:
- monitoring
- repository

Features requested:
- filebeat
- firewall
- grafana
- node-exporter
- prometheus
- repository

Dashboards to download:
- grafana_dashboard_10991
- grafana_dashboard_11074
- grafana_dashboard_179
- grafana_dashboard_1860
- grafana_dashboard_315
- grafana_dashboard_405
- grafana_dashboard_4279
- grafana_dashboard_455
- grafana_dashboard_6663
- grafana_dashboard_7249
- grafana_dashboard_7589
- grafana_dashboard_789
- grafana_dashboard_9628
--------------------------------------------------
"""


EXPECTED_VERBOSE_FILE_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components requested:
- kafka
- repository

Features requested:
- filebeat
- firewall
- jmx-exporter
- kafka
- kafka-exporter
- node-exporter
- repository
- zookeeper

Files to download:
- apache-zookeeper
- jmx-prometheus-javaagent
- kafka
- kafka-exporter
- node-exporter
--------------------------------------------------
"""


EXPECTED_VERBOSE_IMAGE_NO_DOCUMENT_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components requested:
- kafka
- repository

Features requested:
- filebeat
- firewall
- jmx-exporter
- kafka
- kafka-exporter
- node-exporter
- repository
- zookeeper
--------------------------------------------------
"""


EXPECTED_VERBOSE_K8S_AS_CLOUD_SERVICE_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components requested:
- repository

Features requested:
- filebeat
- firewall
- k8s-as-cloud-service
- node-exporter
- repository

Files to download:
- filebeat-chart
- node-exporter
- node-exporter-chart
--------------------------------------------------
"""


EXPECTED_FULL_DOWNLOAD_OUTPUT = """

Files to download:
- https://github.com/danielqsj/kafka_exporter/releases/download/v1.4.0/kafka_exporter-1.4.0.linux-amd64.tar.gz
- https://github.com/prometheus-community/postgres_exporter/releases/download/v0.10.0/postgres_exporter-0.10.0.linux-amd64.tar.gz
- https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
- https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar

Dashboards to download:
- grafana_dashboard_11074
- grafana_dashboard_315
- grafana_dashboard_7249

"""
