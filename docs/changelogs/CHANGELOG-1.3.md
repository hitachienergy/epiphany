# Changelog 1.3

## [1.3.0] YYYY-MM-DD

### Added

- [#2782](https://github.com/epiphany-platform/epiphany/issues/2782) - Assure Node-Exporter is upgraded in its relevant namespace
- [#1306](https://github.com/epiphany-platform/epiphany/issues/1306) - Allow to check on VMs which epicli version was used to deploy/upgrade components
- [#1487](https://github.com/epiphany-platform/epiphany/issues/1487) - Add RabbitMQ monitoring
- [#2600](https://github.com/epiphany-platform/epiphany/issues/2600) - Change epicli output structure
- [#2655](https://github.com/epiphany-platform/epiphany/issues/2655) - Add 'repmgr node check' to upgrade preflight checks and auto-tests
- [#2643](https://github.com/epiphany-platform/epiphany/issues/2643) - Restructure Epicli project folder
- [#2666](https://github.com/epiphany-platform/epiphany/issues/2666) - Project re-structure part 2
- [#2547](https://github.com/epiphany-platform/epiphany/issues/2547) - Refactoring and removal of old code from Ansible inventory creator and upgrade
- [#2597](https://github.com/epiphany-platform/epiphany/issues/2597) - Ensure automatic PostgreSQL clusterization
- [#2644](https://github.com/epiphany-platform/epiphany/issues/2644) - Add validation to check hostnames for on-prem deployment
- [#2703](https://github.com/epiphany-platform/epiphany/issues/2703) - Add tests for docker and kubelet cgroup driver
- [#1076](https://github.com/epiphany-platform/epiphany/issues/1076) - Add sorting entries in the inventory file
- [#2768](https://github.com/epiphany-platform/epiphany/issues/2768) - Add posibility to provide custom hostnames
- [#2785](https://github.com/epiphany-platform/epiphany/issues/2785) - Add configuration option to Keycloak for PROXY_ADDRESS_FORWARDING env. variable
- [#2814](https://github.com/epiphany-platform/epiphany/issues/2814) - Add description how to enable TLS in Kibana
- [#1076](https://github.com/epiphany-platform/epiphany/issues/2595) - Document connection protocols and ciphers
- [#2665](https://github.com/epiphany-platform/epiphany/issues/2665) - Add Kubernetes prereqs to epicli preflight checks
- [#633](https://github.com/epiphany-platform/epiphany/issues/633) - DOC: How to use TLS/SSL certificate with HA Proxy
- [#2702](https://github.com/epiphany-platform/epiphany/issues/2702) - Use state flag file in K8s upgrades

### Fixed

- [#2657](https://github.com/epiphany-platform/epiphany/issues/2657) - Add preflight check which stop upgrade is such pods exists
- [#2497](https://github.com/epiphany-platform/epiphany/issues/2497) - Fix epicli apply --full region values
- [#1743](https://github.com/epiphany-platform/epiphany/issues/1743) - Virtual machine "kind" mismatch
- [#2656](https://github.com/epiphany-platform/epiphany/issues/2656) - WAL files are not removed from $PGDATA/pg_wal directory
- [#1587](https://github.com/epiphany-platform/epiphany/issues/1587) - Duplicated SANs for K8s apiserver certificate
- [#1661](https://github.com/epiphany-platform/epiphany/issues/1661) - Changing the default Kubernetes certificate location results in a cluster deployment error
- [#2707](https://github.com/epiphany-platform/epiphany/issues/2707) - Fix logging component backup
- [#2753](https://github.com/epiphany-platform/epiphany/issues/2753) - Failing offline upgrade: 'download_script_subdir' is undefined
- [#2718](https://github.com/epiphany-platform/epiphany/issues/2718) - Failed epicli upgrade may lead to broken repository machine (disabled system repos)
- [#1221](https://github.com/epiphany-platform/epiphany/issues/1221) - Kafka-exporter service doesn't start after restarting kafka VMs
- [#2774](https://github.com/epiphany-platform/epiphany/issues/2774) - Issue creating service principle on Azure
- [#2737](https://github.com/epiphany-platform/epiphany/issues/2737) - Fix asserting number of postgres nodes
- [#1175](https://github.com/epiphany-platform/epiphany/issues/1175) - Task 'Join to Kubernetes cluster' may fail when Ansible vault already exists

### Updated

- [#2660](https://github.com/epiphany-platform/epiphany/issues/2660) - Upgrade K8s to v1.22.4
  - Upgrade Calico and Canal to v3.20.3
  - Upgrade Coredns to v1.8.4
  - Upgrade Flannel to v0.14.0
  - Upgrade Kubernetes dashboard to v2.3.1
  - Upgrade Kubernetes metrics-scraper to v1.0.7
- [#2747](https://github.com/epiphany-platform/epiphany/issues/2747) - Upgrade Node-Exporter to v1.3.1
- [#2494](https://github.com/epiphany-platform/epiphany/issues/2494) - Duplicated MOTD after ssh to servers
- [#2715](https://github.com/epiphany-platform/epiphany/issues/2715) - Change user login message to show current epicli version
- [#1974](https://github.com/epiphany-platform/epiphany/issues/1974) - [documentation] Azure Files Persistent Volume Support
- [#2454](https://github.com/epiphany-platform/epiphany/issues/2454) - Remove dependencies for K8s v1.17
- [#2537](https://github.com/epiphany-platform/epiphany/issues/2537) - [PostgreSQL] [upgrade] Do not remove new packages automatically in rollback
- [#2180](https://github.com/epiphany-platform/epiphany/issues/2180) - [documentation] Missing clear information about supported CNI plugins
- [#2755](https://github.com/epiphany-platform/epiphany/issues/2755) - Upgrade Python dependencies to the latest
- [#2700](https://github.com/epiphany-platform/epiphany/issues/2700) - Upgrade Prometheus to 2.31.1 and AlertManager to 0.23.0
- [#2748](https://github.com/epiphany-platform/epiphany/issues/2748) - Upgrade Kafka exporter to the version 1.4.0
- [#2750](https://github.com/epiphany-platform/epiphany/issues/2750) - Upgrade JMX exporter to the newest version
- [#2699](https://github.com/epiphany-platform/epiphany/issues/2699) - Upgrade Grafana to 8.3.2
- [#2788](https://github.com/epiphany-platform/epiphany/issues/2788) - Upgrade Log4j in Open Distro for Elasticsearch
- [#2661](https://github.com/epiphany-platform/epiphany/issues/2661) - Update K8s documentation according to the latest version Epiphany supports
- [#2752](https://github.com/epiphany-platform/epiphany/issues/2752) - Upgrade postgresql exporter to the version 0.10.0

### Removed

- [#2680](https://github.com/epiphany-platform/epiphany/issues/2680) - Remove PgBouncer standalone installation
- [#1739](https://github.com/epiphany-platform/epiphany/issues/1739) - Replace standalone HAproxy-exporter by embedded one

### Deprecated

### Breaking changes

- PgBouncer available only as Kubernetes service

### Known issues

- Upgrading Kubernetes to the latest available version 1.22 breaks the Vault and Istio components as versions are not compatible. The issues are not being addressed as these components are being considered for deprecation and removal in subsequent releases.
- Kafka exporter for Prometheus: Performance issue on large clusters. We use version 1.4.0 since 1.4.1 and 1.4.2 contain critical bug (see https://github.com/danielqsj/kafka_exporter/issues/273). For release notes, see https://github.com/danielqsj/kafka_exporter/releases.
