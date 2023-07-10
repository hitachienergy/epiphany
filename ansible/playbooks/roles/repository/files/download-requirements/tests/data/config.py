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

  helm:
    options:
      - url: 'https://get.helm.sh/helm-v3.2.0-linux-amd64.tar.gz'
        sha256: 4c3fd562e64005786ac8f18e7334054a24da34ec04bbd769c206b03b8ed6e457
    deps: [helm]

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
images:
  haproxy:
    'haproxy:2.2.2-alpine':
      sha1: dff8993b065b7f7846adb553548bcdcfcd1b6e8e

  image-registry:
    'registry:2.8.0':
      sha1: 89795c17099199c752d02ad8797c1d4565a08aff
      allow_mismatch: true

  applications:
    'bitnami/pgpool:4.2.4':
      sha1: 66741f3cf4a508bd1f80e2965b0086a4c0fc3580

    'bitnami/pgbouncer:1.16.0':
      sha1: f2e37eecbf9aed44d5566f06dcc101c1ba9edff9

  kubernetes-master:
    'haproxy:2.2.2-alpine':
      sha1: dff8993b065b7f7846adb553548bcdcfcd1b6e8e

    'kubernetesui/dashboard:v2.3.1':
      sha1: 8c8a4ac7a643f9c5dd9e5d22876c434187312db8

    'kubernetesui/metrics-scraper:v1.0.7':
      sha1: 5a0052e2afd3eef3ae638be21938b29b1d608ebe

    # K8s
    # v1.18.6
    'registry.k8s.io/kube-apiserver:v1.18.6':
      sha1: 7376c22211a4e854efb9c7d486d125cd6b9ad937

    'registry.k8s.io/kube-controller-manager:v1.18.6':
      sha1: cd96d2d94dc62a93e8603f362d981dfba8a5917a

    'registry.k8s.io/kube-scheduler:v1.18.6':
      sha1: c40ae182f4af1ddbd7b57fff832979c42847655a

    'registry.k8s.io/kube-proxy:v1.18.6':
      sha1: 75418f30f6e3e6d502ee71d3c7b1253e42cfa6b2

    'registry.k8s.io/coredns:1.6.7':
      sha1: ff4a87c424b1997544d61542c0f0152625466985

    'registry.k8s.io/etcd:3.4.3-0':
      sha1: 6afca8c0f0be353a7262c9a4f75cc51e7f77e019

    'quay.io/coreos/flannel:v0.12.0-amd64':
      sha1: 3516522e779373983992095e61eb6615edd50d1f

    'quay.io/coreos/flannel:v0.12.0':
      sha1: 2cb6ce8f1361886225526767c4a0422c039453c8

    'calico/cni:v3.15.0':
      sha1: aa59f624c223bc398a42c7ba9e628e8143718e58

    'calico/kube-controllers:v3.15.0':
      sha1: f8921f5d67ee7db1c619aa9fdb74114569684ceb

    'calico/node:v3.15.0':
      sha1: b15308e1aa8b9c56253c142e4361e47125bb4ac5

    'calico/pod2daemon-flexvol:v3.15.0':
      sha1: dd1a6525bde05937a28e3d9176b826162ae489af

    # v1.19.15
    'registry.k8s.io/kube-apiserver:v1.19.15':
      sha1: 8ba2f1966563a1cee14c308fb35269a468529fc7

    'registry.k8s.io/kube-controller-manager:v1.19.15':
      sha1: 36a0dde7704d782291158ed3fc4170f887fa7aca

    'registry.k8s.io/kube-scheduler:v1.19.15':
      sha1: 3ba7a05cc19f1accec94557e81c36d146993f76b

    'registry.k8s.io/kube-proxy:v1.19.15':
      sha1: de785d5892a9394a7cd8c432f40dc1e2874c565f

    # v1.20.12
    'registry.k8s.io/kube-apiserver:v1.20.12':
      sha1: b8c79267b9cbe1310f407f787e7d1643841a4b30

    'registry.k8s.io/kube-controller-manager:v1.20.12':
      sha1: 88e0b52ce2abe3fbe3bcaf2043fd6a2e8ff4d428

    'registry.k8s.io/kube-scheduler:v1.20.12':
      sha1: 47934c2c8fbb8e7051ecf3481c466f5021201710

    'registry.k8s.io/kube-proxy:v1.20.12':
      sha1: 0e562fedb15086e613bf6c6fbc2e4193bc49cc76

    'registry.k8s.io/coredns:1.7.0':
      sha1: 521d9f2b461ce4b8a1407715596fec93bfb27e64

    'registry.k8s.io/pause:3.2':
      sha1: a107a151b90d28890f247d4fe951b7b8cf1c7ee7

    # v1.21.7
    'registry.k8s.io/kube-apiserver:v1.21.7':
      sha1: 8aa1733cdf257a58f02df6ad6e23176d97e81b79

    'registry.k8s.io/kube-controller-manager:v1.21.7':
      sha1: cf43f4a88e3b6c79014e5b1e31dd2c0de0da3300

    'registry.k8s.io/kube-scheduler:v1.21.7':
      sha1: f2e62ec380344ea246b40b90cadb3171d211cdab

    'registry.k8s.io/kube-proxy:v1.21.7':
      sha1: a121226c3a55b10fd607d280fc9c471f60b86632

    'registry.k8s.io/coredns/coredns:v1.8.0':
      sha1: 43da34af984b00bd2fcdf5364ff9526433e499c8

    'registry.k8s.io/etcd:3.4.13-0':
      sha1: ee125946a39ce208cb7e38d0fc9a985150f1c3fe

    'registry.k8s.io/pause:3.4.1':
      sha1: c4a3022683dee873dc861328dca2d5524910bbc5

    # v1.22.4
    'registry.k8s.io/kube-apiserver:v1.22.4':
      sha1: 753ff29805d9ac873f409f0cd8dec0818dba4b2d

    'registry.k8s.io/kube-controller-manager:v1.22.4':
      sha1: 3e6936ed6984505bcd194da11b8fcd3e77b52ac4

    'registry.k8s.io/kube-scheduler:v1.22.4':
      sha1: d1fa695dbae08408cf22c8e14b6a70058d5873e1

    'registry.k8s.io/kube-proxy:v1.22.4':
      sha1: b0e3b50e84060be942e48ea67a5c4a95b7355973

    'registry.k8s.io/coredns/coredns:v1.8.4':
      sha1: 447ce8fb5c1ef69298658d976e8aa3a55da28675

    'registry.k8s.io/etcd:3.5.0-0':
      sha1: 78f42080da842ff9454ba9420ad48d90e84de045

    'registry.k8s.io/pause:3.5':
      sha1: 98f71abc4bdab5a3d5eb779b18483caed2544c5d

    'quay.io/coreos/flannel:v0.14.0-amd64':
      sha1: cff47465996a51de4632b53abf1fca873f147027

    'quay.io/coreos/flannel:v0.14.0':
      sha1: a487a36f7b31677e50e74b96b944f27fbce5ac13

    'calico/cni:v3.20.3':
      sha1: 95e4cf79e92715b13e500a0efcfdb65590de1e04

    'calico/kube-controllers:v3.20.3':
      sha1: 5769bae60830abcb3c5d97eb86b8f9938a587b2d

    'calico/node:v3.20.3':
      sha1: cc3c8727ad30b4850e8d0042681342a4f2351eff

    'calico/pod2daemon-flexvol:v3.20.3':
      sha1: 97c1b7ac90aa5a0f5c52e7f137549e598ff80f3e

    'registry.k8s.io/sig-storage/csi-attacher:v3.4.0':
      sha1: a65c9b964b98b0a908a577350a03a5166ab467b3

    'registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.5.0':
      sha1: 49304df65bfbb463bb4be7db688a95c2b1c1a1a5

    'registry.k8s.io/sig-storage/csi-provisioner:v3.1.0':
      sha1: 0d909f211b06853aaaea6e2533f91e7b7ecfd210

    'registry.k8s.io/sig-storage/csi-resizer:v1.4.0':
      sha1: 8acc84db171b9b8efc17290e17ea7e12e9a09219

    'registry.k8s.io/sig-storage/csi-snapshotter:v5.0.1':
      sha1: d5d1b7d2b3eee884dda7d5cd9a6b553d4d997d50

    'quay.io/ceph/ceph:v16.2.7':
      sha1: fe9b7802c67e19111f83ffe4754ab62df66fd417
      allow_mismatch: true

    'quay.io/cephcsi/cephcsi:v3.5.1':
      sha1: 51dee9ea8ad76fb95ebd16f951e8ffaaaba95eb6

    'quay.io/csiaddons/k8s-sidecar:v0.2.1':
      sha1: f0fd757436ac5075910c460c1991ff67c4774d09

    'quay.io/csiaddons/volumereplication-operator:v0.3.0':
      sha1: d3cd17f14fcbf09fc6c8c2c5c0419f098f87a70f
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
    'images': {
        'haproxy': {
            'haproxy:2.2.2-alpine': {
                'sha1': 'dff8993b065b7f7846adb553548bcdcfcd1b6e8e'
            }
        },
        'image-registry': {
            'registry:2.8.0': {
                'sha1': '89795c17099199c752d02ad8797c1d4565a08aff',
                'allow_mismatch': True
            }
        },
        'applications': {
            'bitnami/pgpool:4.2.4': {
                'sha1': '66741f3cf4a508bd1f80e2965b0086a4c0fc3580'
            }
        }
    },
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
Components requested:
- monitoring
- repository

Features requested:
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
Components requested:
- kafka
- repository

Features requested:
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
- image-registry
- jmx-exporter
- kafka
- kafka-exporter
- node-exporter
- repository
- zookeeper

Images to download:
- registry:2.8.0
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
- image-registry
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

Images to download:
- bitnami/pgpool:4.2.4
- haproxy:2.2.2-alpine
- registry:2.8.0

"""
