# Changelog 0.9

## [0.9.2] 2021-0x-xx

### Fixed

- [#2262](https://github.com/epiphany-platform/epiphany/issues/2262) - [Ubuntu] elasticsearch-curator in version 5.8.3 is not available from APT repo

## [0.9.1] 2021-04-22

### Added

- [#2192](https://github.com/epiphany-platform/epiphany/issues/2192) - Support for RHEL 7.9 images

### Fixed

- [#2049](https://github.com/epiphany-platform/epiphany/issues/2049) - Elasticsearch-curator installation fails on RedHat
- [#2131](https://github.com/epiphany-platform/epiphany/issues/2131) - [RedHat/CentOS] Erlang package versions specified in requirements are missing in external repository
- [#2166](https://github.com/epiphany-platform/epiphany/issues/2166) - Replace Bintray repository
- [#1824](https://github.com/epiphany-platform/epiphany/issues/1824) - offline installation fails with error 'yum lockfile is held by another process' (Azure/RHEL)
- [#2067](https://github.com/epiphany-platform/epiphany/issues/2067) - [CentOS] epicli fails on task "repository : Wait for yum lock to be released" on CentOS Minimal
- [#2012](https://github.com/epiphany-platform/epiphany/issues/2012) - Patch cgroup drivers (switch to systemd)

## [0.9.0] 2021-01-19

### Added

- [#921](https://github.com/epiphany-platform/epiphany/issues/921) - Implement log rotation for PgBouncer
- [#1911](https://github.com/epiphany-platform/epiphany/issues/1911) - Ability to deploy Istio
- [#1756](https://github.com/epiphany-platform/epiphany/issues/1756) - Separate role vars and manifest vars generation during upgrades

### Fixed

- [#1273](https://github.com/epiphany-platform/epiphany/issues/1273) - PostgreSQL replication with repmgr: hot_standby not set in config file
- [#1792](https://github.com/epiphany-platform/epiphany/issues/1792) - Not possible to debug failures in applications role
- [#1835](https://github.com/epiphany-platform/epiphany/issues/1835) - Automated tests may give false negative result for PGAudit
- [#1409](https://github.com/epiphany-platform/epiphany/issues/1409) - custom_image_registry_address setting is not implemented
- [#1280](https://github.com/epiphany-platform/epiphany/issues/1280) - [RHEL] Pgpool not showing Replication State
- [#1833](https://github.com/epiphany-platform/epiphany/issues/1833) - DaemonSets of Node Exporter and Filebeat deploy in default namespace
- [#1872](https://github.com/epiphany-platform/epiphany/issues/1872) - pythonPath in launch.json is not supported
- [#1868](https://github.com/epiphany-platform/epiphany/issues/1868) - Repository host runs Ubuntu on Azure/RHEL cluster
- [#1875](https://github.com/epiphany-platform/epiphany/issues/1875) - epicli upgrade fails when there is no kubernetes_master group in inventory
- [#1834](https://github.com/epiphany-platform/epiphany/issues/1834) - Kafka - Disable debug logging and make this option configurable
- [#1888](https://github.com/epiphany-platform/epiphany/issues/1888) - epicli upgrade of cluster created by Epiphany v0.5 may fail
- [#1884](https://github.com/epiphany-platform/epiphany/issues/1884) - Prometheus is not able to scrape metrics from AKS/EKS nodes
- [#1887](https://github.com/epiphany-platform/epiphany/issues/1887) - epicli upgrade of cluster created by Epiphany v0.6 fails on "Store preflight facts" task
- [#1866](https://github.com/epiphany-platform/epiphany/issues/1866) - No logs from K8s apps in Elasticsearch

### Updated

- [#1770](https://github.com/epiphany-platform/epiphany/issues/1770) - Upgrade Filebeat to the latest version (7.9.2)
- [#1848](https://github.com/epiphany-platform/epiphany/issues/1848) - Update Ansible to v2.8.17
- [#1854](https://github.com/epiphany-platform/epiphany/issues/1854) - Upgrade RabbitMQ to the latest version (3.8.9)
- [#1137](https://github.com/epiphany-platform/epiphany/issues/1137) - Upgrade Kafka to v2.6.0
- [#1855](https://github.com/epiphany-platform/epiphany/issues/1855) - Upgrade Docker to v19.03.14
- [#1853](https://github.com/epiphany-platform/epiphany/issues/1853) - Upgrade Zookeeper to v3.5.8
- [#1860](https://github.com/epiphany-platform/epiphany/issues/1860) - Upgrade Grafana to v7.3.5
- [#1955](https://github.com/epiphany-platform/epiphany/issues/1955) - Upgrade Elasticsearch Curator to v5.8.3

### Deprecated

- Elasticsearch OSS v6 (feature name: `elasticsearch`), succesor: Elasticsearch OSS v7 (feature name: `opendistro-for-elasticsearch`). It may be removed in the next major release.

### Breaking changes

### Known issues

- [#1979](https://github.com/epiphany-platform/epiphany/issues/1979) - RabbitMQ fails on upgrade when there are multiple non-clustered nodes
- [#1984](https://github.com/epiphany-platform/epiphany/issues/1984) - RabbitMQ 3.7.10 fails on upgrade to 3.8.9: 'rabbitmqctl version' command not found
