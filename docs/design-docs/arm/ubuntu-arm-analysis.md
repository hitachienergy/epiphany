# Ubuntu requirements.txt ARM analysis

## Packages

| Name        | ARM Supported           | Info  | Required |
| ------------- |:-------------:|:-----:|-----:|
| adduser | + |  | + |
| apt-transport-https | + |  | + |
| auditd | + |  | + |
| bash-completion | + |  | + |
| build-essential | + |  | + |
| ca-certificates | + |  | + |
| cifs-utils | + |  | + |
| containerd.io | + |  | + |
| cri-tools | + |  | + |
| curl | + |  | + |
| docker-ce | + |  | + |
| docker-ce-cli | + |  | + |
| ebtables | + |  | + |
| elasticsearch-curator | + |  | + |
| elasticsearch-oss | + |  | + |
| erlang-asn1 | + |  | + |
| erlang-base | + |  | + |
| erlang-crypto | + |  | + |
| erlang-eldap | + |  | + |
| erlang-ftp | + |  | + |
| erlang-inets | + |  | + |
| erlang-mnesia | + |  | + |
| erlang-os-mon | + |  | + |
| erlang-parsetools | + |  | + |
| erlang-public-key | + |  | + |
| erlang-runtime-tools | + |  | + |
| erlang-snmp | + |  | + |
| erlang-ssl | + |  | + |
| erlang-syntax-tools | + |  | + |
| erlang-tftp | + |  | + |
| erlang-tools | + |  | + |
| erlang-xmerl | + |  | + |
| ethtool | + |  | + |
| filebeat | + |  | + |
| firewalld | + |  | + |
| fping | + |  | + |
| gnupg2 | + |  | + |
| grafana | + |  | + |
| haproxy | + |  | + |
| htop | + |  | + |
| iftop | + |  | + |
| jq | + |  | + |
| libfontconfig1 | + |  | + |
| logrotate | + |  | + |
| logstash-oss | + |  | + |
| netcat | + |  | + |
| net-tools | + |  | + |
| nfs-common | + |  | + |
| opendistro-alerting | + |  | + |
| opendistro-index-management | + |  | + |
| opendistro-job-scheduler | + |  | + |
| opendistro-performance-analyzer | + |  | + |
| opendistro-security | + |  | + |
| opendistro-sql | + |  | + |
| opendistroforelasticsearch-kibana | + |  | + |
| openjdk-8-jre-headless | + |  | + |
| openssl | + |  | + |
| postgresql-10 | + |  | + |
| python-pip | + |  | + |
| python-psycopg2 | + |  | + |
| python-selinux | + |  | + |
| python-setuptools | + |  | + |
| rabbitmq-server | + |  | + |
| smbclient | + |  | + |
| samba-common | + |  | + |
| smbclient | + |  | + |
| software-properties-common | + |  | + |
| sshpass | + |  | + |
| sysstat | + |  | + |
| tar | + |  | + |
| telnet | + |  | + |
| tmux | + |  | + |
| unzip | + |  | + |
| vim | + |  | + |
| rsync | + |  | + |
| libcurl4 | + |  | + |
| libnss3 | + |  | + |
| libcups2 | + |  | + |
| libavahi-client3 | + |  | + |
| libavahi-common3 | + |  | + |
| libjpeg8 | + |  | + |
| libfontconfig1 | + |  | + |
| libxtst6 | + |  | + |
| fontconfig-config | + |  | + |
| python-apt | + |  | + |
| python | + |  | + |
| python2.7 | + |  | + |
| python-minimal | + |  | + |
| python2.7-minimal | + |  | + |
| gcc | + |  | + |
| gcc-7 | + |  | + |
| g++ | + |  | + |
| g++-7 | + |  | + |
| dpkg-dev | + |  | + |
| libc6-dev | + |  | + |
| cpp | + |  | + |
| cpp-7 | + |  | + |
| libgcc-7-dev | + |  | + |
| binutils | + |  | + |
| gcc-8-base | + |  | + |
| libodbc1 | + |  | + |
| apache2 | + |  | + |
| apache2-bin | + |  | + |
| apache2-utils | + |  | + |
| libjq1 | + |  | + |
| gnupg | + |  | + |
| gpg | + |  | + |
| gpg-agent | + |  | + |
| smbclient | + |  | + |
| samba-libs | + |  | + |
| libsmbclient | + |  | + |
| postgresql-client-10 | + |  | + |
| postgresql-10-pgaudit | + |  | + |
| postgresql-10-repmgr | + |  | + |
| postgresql-common | + |  | + |
| pgbouncer | + |  | + |
| ipset | + |  | + |
| libipset3 | + |  | + |
| python3-decorator | + |  | + |
| python3-selinux | + |  | + |
| python3-slip | + |  | + |
| python3-slip-dbus | + |  | + |
| libpq5 | + |  | + |
| python3-psycopg2 | + |  | + |
| python3-jmespath | + |  | + |
| libpython3.6 | + |  | + |
| python-cryptography | + |  | + |
| python-asn1crypto | + |  | + |
| python-cffi-backend | + |  | + |
| python-enum34 | + |  | + |
| python-idna | + |  | + |
| python-ipaddress | + |  | + |
| python-six | + |  | + |
| kubeadm | + |  | + |
| kubectl | + |  | + |
| kubelet | + |  | + |
| kubernetes-cni | + |  | + |
|  |  |  |  |


## Files

| Name        | ARM Supported           |  Info  | Required |
| ------------- |:-------------:|:-----:|-----:|
| https://github.com/prometheus/haproxy_exporter/releases/download/v0.10.0/haproxy_exporter-0.10.0.linux-arm64.tar.gz | + | dedicated package | + |
| https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.14.0/jmx_prometheus_javaagent-0.14.0.jar | + | jar | + |
| https://archive.apache.org/dist/kafka/2.6.0/kafka_2.12-2.6.0.tgz | + | shell scripts + jar libraries | + |
| https://github.com/danielqsj/kafka_exporter/releases/download/v1.2.0/kafka_exporter-1.2.0.linux-arm64.tar.gz | + | dedicated package | + |
| https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-arm64.tar.gz | + | dedicated package | + |
| https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-arm64.tar.gz | + | dedicated package | + |
| https://github.com/prometheus/alertmanager/releases/download/v0.17.0/alertmanager-0.17.0.linux-arm64.tar.gz | + | dedicated package | + |
| https://archive.apache.org/dist/zookeeper/zookeeper-3.5.8/apache-zookeeper-3.5.8-bin.tar.gz | + | shell scripts + jar libraries | --- |
| https://archive.apache.org/dist/ignite/2.9.1/apache-ignite-2.9.1-bin.zip | + | shell scripts + jar libraries | --- |
| https://releases.hashicorp.com/vault/1.7.0/vault_1.7.0_linux_arm64.zip | + | dedicated package | --- |
| https://get.helm.sh/helm-v3.2.0-linux-arm64.tar.gz | + | dedicated package | --- |
| https://github.com/hashicorp/vault-helm/archive/v0.9.0.tar.gz | + | yaml files | --- |
| https://github.com/wrouesnel/postgres_exporter/releases/download/v0.8.0/postgres_exporter_v0.8.0_linux-amd64.tar.gz | --- |  | + |
| https://charts.bitnami.com/bitnami/node-exporter-1.1.2.tgz | + | yaml files | + |
| https://helm.elastic.co/helm/filebeat/filebeat-7.9.2.tgz | + | yaml files | + |
|  |  |  |  |


## Images

| Name        | ARM Supported           |  Info  | Required |
| ------------- |:-------------:|:-----:|-----:|
| haproxy:2.2.2-alpine | + | arm64v8/haproxy | + |
| kubernetesui/dashboard:v2.0.3 | + |  | + |
| kubernetesui/metrics-scraper:v1.0.4 | + |  | + |
| registry:2 | + |  |  |
| hashicorp/vault-k8s:0.7.0 | --- | https://hub.docker.com/r/moikot/vault-k8s / custom build | --- |
| vault:1.7.0 | + |  | --- |
| apacheignite/ignite:2.9.1 | --- | https://github.com/apache/ignite/tree/master/docker/apache-ignite / custom build | --- |
| bitnami/pgpool:4.1.1-debian-10-r29 | --- |  | --- |
| brainsam/pgbouncer:1.12 | --- |  | --- |
| istio/pilot:1.8.1 | --- | https://github.com/istio/istio/issues/21094 / custom build | --- |
| istio/proxyv2:1.8.1 | --- | https://github.com/istio/istio/issues/21094 / custom build | --- |
| istio/operator:1.8.1 | --- | https://github.com/istio/istio/issues/21094 / custom build | --- |
| jboss/keycloak:4.8.3.Final | --- |  | + |
| jboss/keycloak:9.0.0 | --- |  | + |
| rabbitmq:3.8.9 | + |  | + |
| coredns/coredns:1.5.0 | + |  | + |
| quay.io/coreos/flannel:v0.11.0 | + |  | + |
| calico/cni:v3.8.1 | + |  | + |
| calico/kube-controllers:v3.8.1 | + |  | + |
| calico/node:v3.8.1 | + |  | + |
| calico/pod2daemon-flexvol:v3.8.1 | + |  | + |
| k8s.gcr.io/kube-apiserver:v1.18.6 | + | k8s.gcr.io/kube-apiserver-arm64:v1.18.6 | + |
| k8s.gcr.io/kube-controller-manager:v1.18.6 | + | k8s.gcr.io/kube-controller-manager-arm64:v1.18.6 | + |
| k8s.gcr.io/kube-scheduler:v1.18.6 | + | k8s.gcr.io/kube-scheduler-arm64:v1.18.6 | + |
| k8s.gcr.io/kube-proxy:v1.18.6 | + | k8s.gcr.io/kube-proxy-arm64:v1.18.6 | + |
| k8s.gcr.io/coredns:1.6.7 | --- | coredns/coredns:1.6.7 | + |
| k8s.gcr.io/etcd:3.4.3-0 | + | k8s.gcr.io/etcd-arm64:3.4.3-0 | + |
| k8s.gcr.io/pause:3.2 | + | k8s.gcr.io/pause-arm64:3.2 | + |
|  |  |  |  |


# Custom builds

Build multi arch image for Keycloak 9:

Clone repo: https://github.com/keycloak/keycloak-containers/

Checkout tag: 9.0.0

Change dir to: keycloak-containers/server

Create new builder: docker buildx create --name mybuilder

Switch to builder: docker buildx use mybuilder

Inspect builder and make sure it supports linux/amd64, linux/arm64: docker buildx inspect --bootstrap

Build and push container: docker buildx build --platform linux/amd64,linux/arm64 -t repo/keycloak:9.0.0 --push .

---

Additional info:

https://hub.docker.com/r/jboss/keycloak/dockerfile

https://github.com/keycloak/keycloak-containers/

https://catalog.redhat.com/software/containers/ubi8/ubi-minimal/5c359a62bed8bd75a2c3fba8?architecture=arm64&container-tabs=overview

https://docs.docker.com/docker-for-mac/multi-arch/


# Components to roles mapping

| Component name | Roles |
| ------------- |-------------:|
| Repository | repository <br> image-registry <br> node-exporter <br> firewall <br> filebeat <br> docker |
| Kubernetes | kubernetes-master <br> kubernetes-node <br> applications <br> node-exporter <br> haproxy_runc <br> kubernetes_common |
| Kafka | zookeeper <br> jmx-exporter <br> kafka <br> kafka-exporter <br> node-exporter |
| ELK (Logging) | logging <br> elasticsearch <br> elasticsearch_curator <br> logstash <br> kibana  <br> node-exporter |
| Exporters | node-exporter <br> kafka-exporter <br> jmx-exporter <br> haproxy-exporter <br> postgres-exporter |
| PostgreSQL | postgresql <br> postgres-exporter <br> node-exporter |
| Keycloak | applications |
| RabbitMQ | rabbitmq <br> node-exporter |
| HAProxy | haproxy <br> haproxy-exporter <br> node-exporter <br> haproxy_runc <br> |
| Monitoring | prometheus <br> grafana <br> node-exporter |
|  |  |

Except above table, components require following roles to be checked:

 - upgrade
 - backup
 - download
 - firewall
 - filebeat
 - recovery (n/a kubernetes)
