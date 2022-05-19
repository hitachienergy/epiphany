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
- grafana_dashboard_7249
- grafana_dashboard_315
- grafana_dashboard_11074
- grafana_dashboard_405
- grafana_dashboard_455
- grafana_dashboard_9628
- grafana_dashboard_4279
- grafana_dashboard_1860
- grafana_dashboard_7589
- grafana_dashboard_789
- grafana_dashboard_179
- grafana_dashboard_6663
- grafana_dashboard_10991
--------------------------------------------------
"""
