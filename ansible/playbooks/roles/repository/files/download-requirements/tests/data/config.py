FILE_REQUIREMENTS = """
files:
  # --- Exporters ---
  'https://github.com/danielqsj/kafka_exporter/releases/download/v1.4.0/kafka_exporter-1.4.0.linux-amd64.tar.gz':
    sha256: ffda682e82daede726da8719257a088f8e23dcaa4e2ac8b2b2748a129aea85f0
    deps: kafka-exporter

  'https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar':
    sha256: 0ddc6834f854c03d5795305193c1d33132a24fbd406b4b52828602f5bc30777e
    deps: prometheus

  'https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz':
    sha256: 68f3802c2dd3980667e4ba65ea2e1fb03f4a4ba026cca375f15a0390ff850949
    deps: node-exporter

  'https://github.com/prometheus-community/postgres_exporter/releases/download/v0.10.0/postgres_exporter-0.10.0.linux-amd64.tar.gz':
    sha256: 1d1a008c5e29673b404a9ce119b7516fa59974aeda2f47d4a0446d102abce8a1
    deps: postgres-exporter

  # --- Misc ---
  'https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz':
    sha256: 175a4134efc569a586d58916cd16ce70f868b13dea2b5a3d12a67b1395d59f98
    deps: kafka

  'https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz':
    sha256: c35ed6786d59b73920243f1a324d24c2ddfafb379041d7a350cc9a341c52caf3
    deps: zookeeper

  'https://github.com/prometheus/alertmanager/releases/download/v0.23.0/alertmanager-0.23.0.linux-amd64.tar.gz':
    sha256: 77793c4d9bb92be98f7525f8bc50cb8adb8c5de2e944d5500e90ab13918771fc
    deps: alertmanager

  'https://github.com/prometheus/prometheus/releases/download/v2.31.1/prometheus-2.31.1.linux-amd64.tar.gz':
    sha256: 7852dc11cfaa039577c1804fe6f082a07c5eb06be50babcffe29214aedf318b3
    deps: prometheus

  'https://get.helm.sh/helm-v3.2.0-linux-amd64.tar.gz':
    sha256: 4c3fd562e64005786ac8f18e7334054a24da34ec04bbd769c206b03b8ed6e457
    deps: helm

  'https://archive.apache.org/dist/logging/log4j/2.17.1/apache-log4j-2.17.1-bin.tar.gz':
    sha256: b876c20c9d318d77a39c0c2e095897b2bb1cd100c7859643f8c7c8b0fc6d5961
    deps: default

  # --- Helm charts ---
  'https://charts.bitnami.com/bitnami/node-exporter-2.3.17.tgz':
    sha256: ec586fabb775a4f05510386899cf348391523c89ff5a1d4097b0592e675ade7f
    deps: node-exporter

  'https://helm.elastic.co/helm/filebeat/filebeat-7.12.1.tgz':
    sha256: 5838058fe06372390dc335900a7707109cc7287a84164ca245d395af1f9c0a79
    deps: filebeat

  'https://charts.rook.io/release/rook-ceph-v1.8.8.tgz':
    sha256: f67e474dedffd4004f3a0b7b40112694a7f1c2b1a0048b03b3083d0a01e86b14
    deps: rook

  'https://charts.rook.io/release/rook-ceph-cluster-v1.8.8.tgz':
    sha256: df4e1f2125af41fb84c72e4d12aa0cb859dddd4f37b3d5979981bd092040bd16
    deps: rook
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
    sha256: 151b23305da46eab84930e99175e1c07e375af73dbbb4b8f501ca25f5ac62785
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


EXPECTED_VERBOSE_OUTPUT = """
Manifest summary:
--------------------------------------------------
Components detected:
- kafka
- repository

Features detected:
- filebeat
- firewall
- image-registry
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
Components detected:
- monitoring
- repository

Features detected:
- filebeat
- firewall
- grafana
- image-registry
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
Components detected:
- kafka
- repository

Features detected:
- filebeat
- firewall
- image-registry
- jmx-exporter
- kafka
- kafka-exporter
- node-exporter
- repository
- zookeeper

Files to download:
- https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
- https://archive.apache.org/dist/logging/log4j/2.17.1/apache-log4j-2.17.1-bin.tar.gz
- https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz
- https://charts.bitnami.com/bitnami/node-exporter-2.3.17.tgz
- https://github.com/danielqsj/kafka_exporter/releases/download/v1.4.0/kafka_exporter-1.4.0.linux-amd64.tar.gz
- https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
- https://helm.elastic.co/helm/filebeat/filebeat-7.12.1.tgz
--------------------------------------------------
"""
