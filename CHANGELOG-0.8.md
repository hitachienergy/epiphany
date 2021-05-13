# Changelog 0.8

## [0.8.3] 2021-xx-xx

### Fixed

- [#1824](https://github.com/epiphany-platform/epiphany/issues/1824) - offline installation fails with error 'yum lockfile is held by another process' (Azure/RHEL)
- [#2067](https://github.com/epiphany-platform/epiphany/issues/2067) - [CentOS] epicli fails on task "repository : Wait for yum lock to be released" on CentOS Minimal
- [#2262](https://github.com/epiphany-platform/epiphany/issues/2262) - [Ubuntu] elasticsearch-curator in version 5.8.3 is not available from APT repo
- [#2313](https://github.com/epiphany-platform/epiphany/issues/2313) - [RHEL/Azure] RHUI client certificate expired for RHEL 7-RAW images

## [0.8.2] 2021-04-13

### Added

- [#2191](https://github.com/epiphany-platform/epiphany/issues/2191) - Support for RHEL 7.9 images

### Fixed

- [#2049](https://github.com/epiphany-platform/epiphany/issues/2049) - Elasticsearch-curator installation fails on RedHat
- [#2165](https://github.com/epiphany-platform/epiphany/issues/2165) - Replace Bintray repository

## [0.8.1] 2021-02-10

### Fixed

- [#1875](https://github.com/epiphany-platform/epiphany/issues/1875) - epicli upgrade fails when there is no kubernetes_master group in inventory
- [#1884](https://github.com/epiphany-platform/epiphany/issues/1884) - Prometheus is not able to scrape metrics from AKS/EKS nodes
- [#1908](https://github.com/epiphany-platform/epiphany/issues/1908) - Research why Epiphany nodes hang when memory is overcommited
- [#1888](https://github.com/epiphany-platform/epiphany/issues/1888) - epicli upgrade of cluster created by Epiphany v0.5 may fail
- [#2002](https://github.com/epiphany-platform/epiphany/issues/2002) - Do not install Filebeat when there is no Elasticsearch
- [#2042](https://github.com/epiphany-platform/epiphany/issues/2042) - PostgreSQL replication with repmgr: hot_standby not set in config file
- [#2041](https://github.com/epiphany-platform/epiphany/issues/2042) - Pgpool not showing Replication State on RedHat

### Updated

- [#1964](https://github.com/epiphany-platform/epiphany/issues/1964) - Upgrade Elasticsearch Curator to v5.8.3
- [#1919](https://github.com/epiphany-platform/epiphany/issues/1919) - Upgrade Kafka to v2.6.0
- [#1926](https://github.com/epiphany-platform/epiphany/issues/1926) - Upgrade Zookeeper to v3.5.8
- [#1854](https://github.com/epiphany-platform/epiphany/issues/1854) - Upgrade RabbitMQ to v3.8.9
- [#1949](https://github.com/epiphany-platform/epiphany/issues/1949) - Upgrade Grafana to v7.3.5
- [#1855](https://github.com/epiphany-platform/epiphany/issues/1855) - Upgrade Docker to v19.03.14

## [0.8.0] 2020-10-22

### Added

- [#1322](https://github.com/epiphany-platform/epiphany/issues/1322) - Add proper documentation how to define additional security rules for AWS/Azure
- [#1773](https://github.com/epiphany-platform/epiphany/issues/1773) - Document Azure supported images

### Fixed

- [#1754](https://github.com/epiphany-platform/epiphany/issues/1754) - Fix Vault installation for setup without K8s
- [#1640](https://github.com/epiphany-platform/epiphany/issues/1640) - Default disk size for repository machine increased to 64 GB (AWS and Azure)
- [#1774](https://github.com/epiphany-platform/epiphany/issues/1774) - [epicli upgrade] Filebeat stops working when legacy Elasticsearch (v6) is used for storing logs
- [#1775](https://github.com/epiphany-platform/epiphany/issues/1775) - [epicli upgrade] Cannot upgrade Epiphany cluster in version 0.6.x when using "--wait-for-pods" flag.

### Updated

- [#1719](https://github.com/epiphany-platform/epiphany/issues/1719) - Upgrade Open Distro for Elasticsearch to v1.10.1 and elasticsearch-oss to v7.9.1

## [0.8.0rc1] 2020-10-08

### Added

- [#1542](https://github.com/epiphany-platform/epiphany/issues/1542) - Implement Ansible role postgres-exporter
- [#1302](https://github.com/epiphany-platform/epiphany/issues/1302) - Ability to update control plane certificates expiration date
- [#1324](https://github.com/epiphany-platform/epiphany/issues/1324) - Added Logstash to export data from Elasticsearch to csv format
- [#1300](https://github.com/epiphany-platform/epiphany/issues/1300) - Configure OpenSSH according to Mozilla Infosec guidance
- [#1543](https://github.com/epiphany-platform/epiphany/issues/1543) - Add support for Azure availability sets
- [#1609](https://github.com/epiphany-platform/epiphany/issues/1609) - Build epicli image using Dockerfile only (without shell script)
- [#765](https://github.com/epiphany-platform/epiphany/issues/765) - Added multiline support for logs statements in Filebeat
- [#1618](https://github.com/epiphany-platform/epiphany/issues/1618) - Add kubectl and Helm to epicli and devcontainer images
- [#1225](https://github.com/epiphany-platform/epiphany/issues/1225) - Add OS_PATCHING.md with information about patching RHEL OS
- [#1656](https://github.com/epiphany-platform/epiphany/issues/1656) - Run Helm tasks from Epiphany container
- [#1640](https://github.com/epiphany-platform/epiphany/issues/1640) - Added separate machine for repository and changed helm to use localhost address
- [#1673](https://github.com/epiphany-platform/epiphany/issues/1673) - Added Node Exporter as DaemonSet for "Kubernetes as Cloud Service"
- [#1670](https://github.com/epiphany-platform/epiphany/issues/1670) - Added Filebeat as DaemonSet for "Kubernetes as Cloud Service"
- [#1696](https://github.com/epiphany-platform/epiphany/issues/1696) - Document installation of Epiphany using AzBI and AzKS modules

### Updated

- [#846](https://github.com/epiphany-platform/epiphany/issues/846) - Update Filebeat to v7.8.1
- [#1140](https://github.com/epiphany-platform/epiphany/issues/1140) - Upgrade Open Distro for Elasticsearch to v7.8.0
- [#1316](https://github.com/epiphany-platform/epiphany/issues/1316) - Upgrade HAProxy to v2.2
- [#1115](https://github.com/epiphany-platform/epiphany/issues/1115) - Upgrade Node exporter to v1.0.1
- [#1589](https://github.com/epiphany-platform/epiphany/issues/1589) - Update OS_PATCHING.md with information about patching Ubuntu OS
- [#1639](https://github.com/epiphany-platform/epiphany/issues/1639) - Use local kubectl in 'prometheus' role
- [#1654](https://github.com/epiphany-platform/epiphany/issues/1654) - Use local kubectl for 'applications' part

### Fixed

- Fix for changing Terraform templates between Epicli apply runs on Azure.
- [#1520](https://github.com/epiphany-platform/epiphany/issues/1520) - Added additional SANs to k8s-apiserver certificates to run kubectl outside the cluster
- [#1491](https://github.com/epiphany-platform/epiphany/issues/1491) - Error running upgrade on a 0.3 cluster: missing shared-config
- [#1659](https://github.com/epiphany-platform/epiphany/issues/1659) - epicli upgrade fails on Ubuntu on downgrading kubernetes-cni package
- [#1681](https://github.com/epiphany-platform/epiphany/issues/1681) - Node exporter does not work after the upgrade
- [#1705](https://github.com/epiphany-platform/epiphany/issues/1705) - [RHEL/CentOS] epicli fails on downloading requirements - Docker CE repo not available
- [#922](https://github.com/epiphany-platform/epiphany/issues/922) - [RHEL/CentOS] Elasticsearch v6 stops working after epicli upgrade
- [#1741](https://github.com/epiphany-platform/epiphany/issues/1741) - Upgrade doesn't work with ERROR epicli - No such attribute: cloud

### Breaking changes

- Repository machine was introduced (ref #1640)
- Change cluster configuration manifest in order to be compatible with changes in #1640 [example] (https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/common/defaults/epiphany-cluster.yml)
- Filebeat renamed fields in 7.0, see [here](https://www.elastic.co/guide/en/beats/libbeat/current/breaking-changes-7.0.html#_field_name_changes). The `source` field was removed and replaced with `log.file.path`.

### Known issues

- [1647](https://github.com/epiphany-platform/epiphany/issues/1647) - `epicli upgrade` fails on `[opendistro_for_elasticsearch : Provide jvm configuration file]` task
