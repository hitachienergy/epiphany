# CentOS requirements.txt ARM analysis

## Packages

| Name        | ARM Supported           | Additional Info  |
| ------------- |:-------------:| -----:|
| apr | <span style="color:green">+</span> |  |
| apr-util | <span style="color:green">+</span> |  |
| centos-logos | <span style="color:green">+</span> | |
| createrepo | <span style="color:green">+</span> | |
| deltarpm | <span style="color:green">+</span> | |
| httpd | <span style="color:green">+</span> | |
| httpd-tools | <span style="color:green">+</span> | |
| libxml2-python | <span style="color:green">+</span> | |
| mailcap | <span style="color:green">+</span> | |
| mod_ssl | <span style="color:green">+</span> | |
| python-chardet | <span style="color:green">+</span> | |
| python-deltarpm | <span style="color:green">+</span> | |
| python-kitchen | <span style="color:green">+</span> | |
| yum-utils | <span style="color:green">+</span> | |
| audit | <span style="color:green">+</span> | |
| bash-completion | <span style="color:green">+</span> | |
| c-ares | <span style="color:green">+</span> | |
| ca-certificates | <span style="color:green">+</span> | |
| cifs-utils | <span style="color:green">+</span> | |
| conntrack-tools | <span style="color:green">+</span> | |
| containerd.io | <span style="color:green">+</span> | |
| container-selinux | <span style="color:green">+</span> | |
| cri-tools-1.13.0 | <span style="color:green">+</span> | |
| curl | <span style="color:green">+</span> | |
| dejavu-sans-fonts | <span style="color:green">+</span> | |
| docker-ce-19.03.14 | <span style="color:green">+</span> | |
| docker-ce-cli-19.03.14 | <span style="color:green">+</span> | |
| ebtables | <span style="color:green">+</span> | |
| elasticsearch-curator-5.8.3 | <span style="color:red">---</span> | |
| elasticsearch-oss-6.8.5 | <span style="color:green">+</span> | |
| elasticsearch-oss-7.9.1 | <span style="color:green">+</span> | |
| erlang-23.1.4 | <span style="color:green">+</span> | |
| ethtool | <span style="color:green">+</span> | |
| filebeat-7.9.2 | <span style="color:green">+</span> | |
| firewalld | <span style="color:green">+</span> | |
| fontconfig | <span style="color:green">+</span> | |
| fping | <span style="color:green">+</span> | |
| gnutls | <span style="color:green">+</span> | |
| grafana-7.3.5 | <span style="color:green">+</span> | |
| gssproxy | <span style="color:green">+</span> | |
| htop | <span style="color:green">+</span> | |
| iftop | <span style="color:green">+</span> | |
| ipset | <span style="color:green">+</span> | |
| java-1.8.0-openjdk-headless | <span style="color:green">+</span> | |
| javapackages-tools | <span style="color:green">+</span> | |
| jq | <span style="color:green">+</span> | |
| libini_config | <span style="color:green">+</span> | |
| libselinux-python | <span style="color:green">+</span> | |
| libsemanage-python | <span style="color:green">+</span> | |
| libX11 | <span style="color:green">+</span> | |
| libxcb | <span style="color:green">+</span> | |
| libXcursor | <span style="color:green">+</span> | |
| libXt | <span style="color:green">+</span> | |
| logrotate | <span style="color:green">+</span> | |
| logstash-oss-7.8.1 | <span style="color:green">+</span> | |
| net-tools | <span style="color:green">+</span> | |
| nfs-utils | <span style="color:green">+</span> | |
| nmap-ncat | <span style="color:green">+</span> | |
| opendistro-alerting-1.10.1* | <span style="color:green">+</span> | |
| opendistro-index-management-1.10.1* | <span style="color:green">+</span> | |
| opendistro-job-scheduler-1.10.1* | <span style="color:green">+</span> | |
| opendistro-performance-analyzer-1.10.1* | <span style="color:green">+</span> | |
| opendistro-security-1.10.1* | <span style="color:green">+</span> | |
| opendistro-sql-1.10.1* | <span style="color:green">+</span> | |
| opendistroforelasticsearch-kibana-1.10.1* | <span style="color:red">---</span> | |
| openssl | <span style="color:green">+</span> | |
| perl | <span style="color:green">+</span> | |
| perl-Getopt-Long | <span style="color:green">+</span> | |
| perl-libs | <span style="color:green">+</span> | |
| perl-Pod-Perldoc | <span style="color:green">+</span> | |
| perl-Pod-Simple | <span style="color:green">+</span> | |
| perl-Pod-Usage | <span style="color:green">+</span> | |
| pgaudit12_10 | <span style="color:green">+</span> | |
| pgbouncer-1.10.* | <span style="color:red">---</span> | |
| pyldb | <span style="color:green">+</span> | |
| python-firewall | <span style="color:green">+</span> | |
| python-kitchen | <span style="color:green">+</span> | |
| python-lxml | <span style="color:green">+</span> | |
| python-psycopg2 | <span style="color:green">+</span> | |
| python-setuptools | <span style="color:green">+</span> | |
| python-slip-dbus | <span style="color:green">+</span> | |
| python-ipaddress | <span style="color:green">+</span> | |
| python-backports | <span style="color:green">+</span> | |
| quota | <span style="color:green">+</span> | |
| rabbitmq-server-3.8.9 | <span style="color:green">+</span> | |
| rh-haproxy18 | <span style="color:red">---</span> | |
| rh-haproxy18-haproxy-syspaths | <span style="color:red">---</span> | |
| postgresql10-server | <span style="color:green">+</span> | |
| repmgr10-4.0.6 | <span style="color:red">---</span> |  |
| samba-client | <span style="color:green">+</span> | |
| samba-client-libs | <span style="color:green">+</span> | |
| samba-common | <span style="color:green">+</span> | |
| samba-libs | <span style="color:green">+</span> | |
| sysstat | <span style="color:green">+</span> | |
| tar | <span style="color:green">+</span> | |
| telnet | <span style="color:green">+</span> | |
| tmux | <span style="color:green">+</span> | |
| urw-base35-fonts | <span style="color:green">+</span> | |
| unzip | <span style="color:green">+</span> | |
| vim-common | <span style="color:green">+</span> | |
| vim-enhanced | <span style="color:green">+</span> | |
| wget | <span style="color:green">+</span> | |
| xorg-x11-font-utils | <span style="color:green">+</span> | |
| xorg-x11-server-utils | <span style="color:green">+</span> | |
| yum-plugin-versionlock | <span style="color:green">+</span> | |
| yum-utils | <span style="color:green">+</span> | |
| rsync | <span style="color:green">+</span> | |
| kubeadm-1.17.4 | <span style="color:green">+</span> | |
| kubectl-1.17.4 | <span style="color:green">+</span> | |
| kubelet-1.17.4 | <span style="color:green">+</span> | |
| kubernetes-cni-0.8.6-0 | <span style="color:green">+</span> | |
|  |  |  |

## Files

| Name        | ARM Supported           | Additional Info  |
| ------------- |:-------------:| -----:|
| https://github.com/prometheus/haproxy_exporter/releases/download/v0.10.0/haproxy_exporter-0.10.0.linux-armv7.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.14.0/jmx_prometheus_javaagent-0.14.0.jar | <span style="color:green">+</span> | jar |
| https://archive.apache.org/dist/kafka/2.6.0/kafka_2.12-2.6.0.tgz | <span style="color:green">+</span> | shell scripts + jar libraries |
| https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-armv7.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-armv7.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-armv7.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://github.com/prometheus/alertmanager/releases/download/v0.17.0/alertmanager-0.17.0.linux-armv7.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz | <span style="color:green">+</span> | shell scripts + jar libraries |
| https://archive.apache.org/dist/ignite/2.9.1/apache-ignite-2.9.1-bin.zip | <span style="color:green">+</span> | shell scripts + jar libraries |
| https://releases.hashicorp.com/vault/1.6.1/vault_1.6.1_linux_arm.zip | <span style="color:green">+</span> | dedicated package |
| https://get.helm.sh/helm-v3.2.0-linux-arm.tar.gz | <span style="color:green">+</span> | dedicated package |
| https://github.com/hashicorp/vault-helm/archive/v0.9.0.tar.gz | <span style="color:green">+</span> | yaml files |
| https://github.com/wrouesnel/postgres_exporter/releases/download/v0.8.0/postgres_exporter_v0.8.0_linux-amd64.tar.gz | <span style="color:red">---</span> |  |
| https://charts.bitnami.com/bitnami/node-exporter-1.1.2.tgz | <span style="color:green">+</span> | yaml files |
| https://helm.elastic.co/helm/filebeat/filebeat-7.9.2.tgz | <span style="color:green">+</span> | yaml files |
|  |  |  |


## Images

| Name        | ARM Supported           | Additional Info  |
| ------------- |:-------------:| -----:|
| haproxy:2.2.2-alpine | <span style="color:green">+</span> | arm32v7/haproxy |
| kubernetesui/dashboard:v2.0.3 | <span style="color:green">+</span> |  |
| kubernetesui/metrics-scraper:v1.0.4 | <span style="color:green">+</span> |  |
| registry:2 | <span style="color:green">+</span> |  |
| hashicorp/vault-k8s:0.7.0 | <span style="color:red">---</span> |  |
| vault:1.6.1 | <span style="color:green">+</span> |  |
| apacheignite/ignite:2.9.1 | <span style="color:red">---</span> |  |
| bitnami/pgpool:4.1.1-debian-10-r29 | <span style="color:red">---</span> |  |
| brainsam/pgbouncer:1.12 | <span style="color:red">---</span> |  |
| istio/pilot:1.8.1 | <span style="color:red">---</span> |  |
| istio/proxyv2:1.8.1 | <span style="color:red">---</span> |  |
| istio/operator:1.8.1 | <span style="color:red">---</span> |  |
| jboss/keycloak:4.8.3.Final | <span style="color:red">---</span> |  |
| jboss/keycloak:9.0.0 | <span style="color:red">---</span> |  |
| rabbitmq:3.8.9 | <span style="color:green">+</span> |  |
| coredns/coredns:1.5.0 | <span style="color:green">+</span> |  |
| quay.io/coreos/flannel:v0.11.0 | <span style="color:green">+</span> |  |
| calico/cni:v3.8.1 | <span style="color:green">+</span> |  |
| calico/kube-controllers:v3.8.1 | <span style="color:green">+</span> |  |
| calico/node:v3.8.1 | <span style="color:green">+</span> |  |
| calico/pod2daemon-flexvol:v3.8.1 | <span style="color:green">+</span> |  |
| k8s.gcr.io/kube-apiserver:v1.18.6 | <span style="color:green">+</span> | k8s.gcr.io/kube-apiserver-arm64:v1.18.6 |
| k8s.gcr.io/kube-controller-manager:v1.18.6 | <span style="color:green">+</span> | k8s.gcr.io/kube-controller-manager-arm64:v1.18.6 |
| k8s.gcr.io/kube-scheduler:v1.18.6 | <span style="color:green">+</span> | k8s.gcr.io/kube-scheduler-arm64:v1.18.6 |
| k8s.gcr.io/kube-proxy:v1.18.6 | <span style="color:green">+</span> | k8s.gcr.io/kube-proxy-arm64:v1.18.6 |
| k8s.gcr.io/coredns:1.6.7 | <span style="color:red">---</span> |  |
| k8s.gcr.io/etcd:3.4.3-0 | <span style="color:green">+</span> | k8s.gcr.io/etcd-arm64:3.4.3-0 |
| k8s.gcr.io/pause:3.2 | <span style="color:green">+</span> | k8s.gcr.io/pause-arm64:3.2 |
|  |  |  |
