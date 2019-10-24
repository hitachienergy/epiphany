# How-To Guides

- [Prerequisites for Epiphany](./howto/PREREQUISITES.md)
  - [Run Epicli from Docker image](./howto/PREREQUISITES.md#run-epicli-from-docker-image)
  - [Run Epicli directly from OS](./howto/PREREQUISITES.md#run-epicli-directly-from-os)
  - [Epicli development](./howto/PREREQUISITES.md#epicli-development)
  - [Note for Windows users](./howto/PREREQUISITES.md#note-for-windows-users)
  - [Note about proxies](./howto/PREREQUISITES.md#note-about-proxies)

- [Epiphany cluster](./howto/CLUSTER.md)
  - [How to create an Epiphany cluster on existing infrastructure](./howto/CLUSTER.md#how-to-create-an-epiphany-cluster-on-existing-infrastructure)
  - [How to create an Epiphany cluster on existing airgapped infrastructure](./howto/CLUSTER.md#how-to-create-an-epiphany-cluster-on-existing-airgapped-infrastructure)
  - [How to create an Epiphany cluster on a cloud provider](./howto/CLUSTER.md#how-to-create-an-epiphany-cluster-on-a-cloud-provider)
  - [How to delete an Epiphany cluster on a cloud provider](./howto/CLUSTER.md#how-to-delete-an-epiphany-cluster-on-a-cloud-provider)
  - [Single machine cluster](./howto/CLUSTER.md#single-machine-cluster)
  - [How to scale  or cluster components](./howto/CLUSTER.md#how-to-scale-or-cluster-components)
  - [Build artifacts](./howto/CLUSTER.md#build-artifacts)
  - [Kafka replication and partition setting](./howto/CLUSTER.md#kafka-replication-and-partition-setting)
  - [RabbitMQ installation and setting](./howto/CLUSTER.md#rabbitmq-installation-and-setting)

- [Monitoring](./howto/MONITORING.md)
  - [How to configure Prometheus alerts](./howto/MONITORING.md#how-to-configure-prometheus-alerts)
  - [Import and create of Grafana dashboards](./howto/MONITORING.md#import-and-create-of-grafana-dashboards)
  - [How to configure Kibana](./howto/MONITORING.md#how-to-configure-kibana)
  - [How to configure scalable Prometheus setup](./howto/MONITORING.md#how-to-configure-scalable-prometheus-setup)
  - [How to configure Azure additional monitoring and alerting](./howto/MONITORING.md#how-to-configure-azure-additional-monitoring-and-alerting)
  - [How to configure AWS additional monitoring and alerting](./howto/MONITORING.md#how-to-configure-aws-additional-monitoring-and-alerting)

- [Kubernetes](./howto/KUBERNETES.md)
  - [How to expose service through HA Proxy load balancer](./howto/KUBERNETES.md#how-to-expose-service-through-ha-proxy-load-balancer)
  - [How to do Kubernetes RBAC](./howto/KUBERNETES.md#how-to-do-kubernetes-rbac)
  - [How to run an example app](./howto/KUBERNETES.md#how-to-run-an-example-app)
  - [How to set resource requests and limits for Containers](./howto/KUBERNETES.md#how-to-set-resource-requests-and-limits-for-containers)
  - [How to run CronJobs](./howto/KUBERNETES.md#how-to-run-cronjobs)
  - [How to test the monitoring features](./howto/KUBERNETES.md#how-to-test-the-monitoring-features)
  - [How to run chaos on Epiphany Kubernetes cluster and monitor it with Grafana](./howto/KUBERNETES.md#how-to-run-chaos-on-epiphany-kubernetes-cluster-and-monitor-it-with-grafana)
  - [How to test the central logging features](./howto/KUBERNETES.md#how-to-test-the-central-logging-features)
  - [How to tunnel Kubernetes dashboard from remote kubectl to your PC](./howto/KUBERNETES.md#how-to-tunnel-kubernetes-dashboard-from-remote-kubectl-to-your-pc)

- [Upgrade](./howto/UPGRADE.md)
  - [How to upgrade Kubernetes cluster](./howto/UPGRADE.md#how-to-upgrade-kubernetes-cluster)
  - [How to upgrade Kubernetes cluster from 1.13.0 to 1.13.1](./howto/UPGRADE.md#how-to-upgrade-kubernetes-cluster-from-1130-to-1131)
  - [How to upgrade Kubernetes cluster from 1.13.1 to 1.13.10 / latest patch](./howto/UPGRADE.md#how-to-upgrade-kubernetes-cluster-from-1131-to-11310--latest-patch)
  - [How to upgrade Kafka cluster](./howto/UPGRADE.md#how-to-upgrade-Kafka-cluster)

- [Security](./howto/SECURITY.md)
  - Epicli
    - [How to use TLS/SSL certificate with HA Proxy](./howto/SECURITY.md#how-to-use-tls/ssl-certificate-with-ha-proxy)
    - [How to enable AWS disk encryption](./howto/SECURITY.md#how-to-enable-AWS-disk-encryption)
  - Legacy
    - [How to use TLS/SSL certificate with HA Proxy in a legacy cluster](./howto/SECURITY.md#how-to-use-tls/ssl-certificate-with-ha-proxy-in-a-legacy-cluster)
    - [How to enable or disable network traffic - firewall](./howto/SECURITY.md#how-to-enable-or-disable-network-traffic)
    - [Client certificate for Azure VPN connection](./howto/SECURITY.md#client-certificate-for-azure-vpn-connection)
    - [How to set HA Proxy load balancer to minimize risk of Slowloris like attacks](./howto/SECURITY.md#how-to-set-HA-Proxy-load-balancer-to-minimize-risk-of-Slowloris-like-attacks)
  - [How to use Kubernetes Secrets](./howto/SECURITY.md#how-to-use-kubernetes-secrets)
  - [How to authenticate to Azure AD app](./howto/SECURITY.md#how-to-authenticate-to-azure-ad-app)

- [Databases](./howto/DATABASES.md)
  - [How to configure PostgreSQL](./howto/DATABASES.md#how-to-configure-postgresql)
  - [How to configure PostgreSQL replication](./howto/DATABASES.md#how-to-configure-postgresql-replication)

- [Data and log retention](./howto/RETENTION.md)
  - Epicli
    - TODO
  - Legacy
    - [Elasticsearch](./howto/RETENTION.md#elasticsearch)
    - [Grafana](./howto/RETENTION.md#grafana)
    - [Kafka](./howto/RETENTION.md#kafka)
    - [Kibana](./howto/RETENTION.md#kibana)
    - [Kubernetes](./howto/RETENTION.md#kubernetes)
    - [Prometheus](./howto/RETENTION.md#prometheus)
    - [Zookeeper](./howto/RETENTION.md#zookeeper)
