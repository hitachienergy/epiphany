# Changelog 1.3

## [1.3.0] YYYY-MM-DD

### Added

- [#1306](https://github.com/epiphany-platform/epiphany/issues/1306) - Allow to check on VMs which epicli version was used to deploy/upgrade components
- [#1487](https://github.com//epiphany-platform/epiphany/issues/1487) - Add RabbitMQ monitoring
- [#2600](https://github.com/epiphany-platform/epiphany/issues/2600) - Change epicli output structure
- [#2655](https://github.com/epiphany-platform/epiphany/issues/2655) - Add 'repmgr node check' to upgrade preflight checks and auto-tests
- [#2643](https://github.com/epiphany-platform/epiphany/issues/2643) - Restructure Epicli project folder
- [#2666](https://github.com/epiphany-platform/epiphany/issues/2666) - Project re-structure part 2
- [#2547](https://github.com/epiphany-platform/epiphany/issues/2547) - Refactoring and removal of old code from Ansible inventory creator and upgrade
- [#2597](https://github.com/epiphany-platform/epiphany/issues/2597) - Ensure automatic PostgreSQL clusterization
- [#2644](https://github.com/epiphany-platform/epiphany/issues/2644) - Add validation to check hostnames for on-prem deployment
- [#2703](https://github.com/epiphany-platform/epiphany/issues/2703) - Add tests for docker and kubelet cgroup driver
- [#1076](https://github.com/epiphany-platform/epiphany/issues/1076) - Add sorting entries in the inventory file

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

### Updated

- Upgrade Flannel to v0.14.0
- Upgrade Calico and Canal to v3.20.3
- Upgrade Coredns to v1.8.0
- Upgrade Kubernetes dashboard to v2.3.1
- Upgrade Kubernetes metrics-scraper to v1.0.7
- [#2659](https://github.com/epiphany-platform/epiphany/issues/2659) - Upgrade K8s to v1.21.7
- [#2494](https://github.com/epiphany-platform/epiphany/issues/2494) - Duplicated MOTD after ssh to servers
- [#1974](https://github.com/epiphany-platform/epiphany/issues/1974) - [documentation] Azure Files Persistent Volume Support
- [#2454](https://github.com/epiphany-platform/epiphany/issues/2454) - Remove dependencies for K8s v1.17
- [#2537](https://github.com/epiphany-platform/epiphany/issues/2537) - [PostgreSQL] [upgrade] Do not remove new packages automatically in rollback
- [#2180](https://github.com/epiphany-platform/epiphany/issues/2180) - [documentation] Missing clear information about supported CNI plugins
- [#2755](https://github.com/epiphany-platform/epiphany/issues/2755) - Upgrade Python dependencies to the latest
- [#2700](https://github.com/epiphany-platform/epiphany/issues/2700) - Upgrade Prometheus to 2.31.1 and AlertManager to 0.23.0
- [#2748](https://github.com/epiphany-platform/epiphany/issues/2748) - Upgrade Kafka exporter to the version 1.4.0
- [#2750](https://github.com/epiphany-platform/epiphany/issues/2750) - Upgrade JMX exporter to the newest version

### Removed

- [#2680](https://github.com/epiphany-platform/epiphany/issues/2680) - Remove PgBouncer standalone installation

### Deprecated

### Breaking changes

- PgBouncer available only as Kubernetes service

### Known issues
