# Changelog 1.3

## [1.3.1] 2022-xx-xx

### Fixed

- [#2997](https://github.com/epiphany-platform/epiphany/issues/2997) - Doubled HAProxy entries in prometheus.yml after upgrade
- [#2996](https://github.com/epiphany-platform/epiphany/issues/2996) - Introduce the new configuration field to change a component name
- [#3065](https://github.com/epiphany-platform/epiphany/issues/3065) - Flag `delete_os_disk_on_termination` has no effect when removing cluster
- [#3006](https://github.com/epiphany-platform/epiphany/issues/3006) - install 'containerd.io=1.4.12-*' failed, when upgrade from v1.3.0 to 2.0.0dev

## [1.3.0] 2022-01-19

### Added

- [#1331](https://github.com/epiphany-platform/epiphany/issues/1331) - Support for Ubuntu 20.04 LTS
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
- [#2840](https://github.com/epiphany-platform/epiphany/issues/2840) - Create deprecation notes documentation
- [#2860](https://github.com/epiphany-platform/epiphany/issues/2860) - Increase the number of forks in Ansible from default (5) to configure more hosts in parallel

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
- [#2420](https://github.com/epiphany-platform/epiphany/issues/2420) - Changing Grafana admin password in the apply mode
- [#2873](https://github.com/epiphany-platform/epiphany/issues/2873) - Epicli backup fails on schema validation
- [#2886](https://github.com/epiphany-platform/epiphany/issues/2886) - [Ubuntu] [PostgreSQL] Apply command fails after upgrading from v1.0.x LTS to v1.3.0
- [#2894](https://github.com/epiphany-platform/epiphany/issues/2894) - System repositories are not restored on epicli re-run
- [#2904](https://github.com/epiphany-platform/epiphany/issues/2904) - Not possible to add PostgreSQL component to existing environment

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
- [#2856](https://github.com/epiphany-platform/epiphany/issues/2856) - Update cloud OS images to the latest

### Removed

- Support for Ubuntu 18.04
- [#2680](https://github.com/epiphany-platform/epiphany/issues/2680) - Remove PgBouncer standalone installation
- [#1739](https://github.com/epiphany-platform/epiphany/issues/1739) - Replace standalone HAproxy-exporter by embedded one

### Deprecated

### Breaking changes

- **Ubuntu 18.04 is not supported**. For Ubuntu, only release 20.04 is supported and upgrade from 18.04 is not handled by Epiphany.
For more information, see [How to upgrade from Ubuntu 18.04 to 20.04](../home/howto/OS_UPGRADE.md#how-to-upgrade-from-ubuntu-1804-to-2004).
- PgBouncer available only as Kubernetes service

### Known issues

- Upgrading Kubernetes to the latest available version 1.22 breaks the Vault and Istio components as versions are not compatible. The issues are not being addressed as these components are being considered for deprecation and removal in subsequent releases.
- Kafka exporter for Prometheus: Performance issue on large clusters. We use version 1.4.0 since 1.4.1 and 1.4.2 contain critical bug (see https://github.com/danielqsj/kafka_exporter/issues/273). For release notes, see https://github.com/danielqsj/kafka_exporter/releases.
