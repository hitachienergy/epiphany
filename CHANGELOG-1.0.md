# Changelog 1.0

## [1.0.3] 2022-xx-xx

### Added

- [#2976](https://github.com/epiphany-platform/epiphany/issues/2976) - Allow for custom Terraform scripts
- [#1076](https://github.com/epiphany-platform/epiphany/issues/1076) - Add sorting entries in the inventory file

### Fixed

- [#2989](https://github.com/epiphany-platform/epiphany/issues/2989) - Task `Remove swap from /etc/fstab` does not remove swap entry from file
- [#2653](https://github.com/epiphany-platform/epiphany/issues/2653) - Epicli is failing in air-gapped infra mode
- [#3004](https://github.com/epiphany-platform/epiphany/issues/3004) - `disk_size_gb` hardcoded in `/usr/local/epicli/data/azure/defaults/infrastructure/virtual-machine.yml`
- [#2934](https://github.com/epiphany-platform/epiphany/issues/2934) - Duplicated entries in image-registry defaults (LTS)
- [#3065](https://github.com/epiphany-platform/epiphany/issues/3065) - Flag `delete_os_disk_on_termination` has no effect when removing cluster
- [#2996](https://github.com/epiphany-platform/epiphany/issues/2996) - Introduce the new configuration field to change a component name
- [#3060](https://github.com/epiphany-platform/epiphany/issues/3060) - Allow to disable Open Distro audit logs

### Fixed

- [#3034](https://github.com/epiphany-platform/epiphany/issues/3034) - [RHEL/CentOS] GPG signature could not be verified for Kubernetes repository
- [#3102](https://github.com/epiphany-platform/epiphany/issues/3102) - Errors in system logs: /var/lib/prometheus/node-exporter: no such file or directory

## [1.0.2] 2022-01-26

### NOTE ###

Before running `epicli backup` for RHEL/CentOS based cluster with standalone (non-K8s) RabbitMQ component,
read note in [this doc](docs/home/howto/BACKUP.md#1-how-to-perform-backup).

### Added

- [#2124](https://github.com/epiphany-platform/epiphany/issues/2124) - Added Internet connection test to download-requirements.sh
- [#195](https://github.com/epiphany-platform/epiphany/issues/195) - Basic configuration type and schema validation
- [#2768](https://github.com/epiphany-platform/epiphany/issues/2768) - Add posibility to provide custom hostnames

### Fixed

- [#2920](https://github.com/epiphany-platform/epiphany/issues/2920) - [RHEL/CentOS] RabbitMQ backup fails: /usr/bin/env: python3: No such file or directory
- [#2425](https://github.com/epiphany-platform/epiphany/issues/2425) - Feature-mapping - 'enabled: no' do nothing
- [#1294](https://github.com/epiphany-platform/epiphany/issues/1294) - Implement proper merging of lists of dictionaries for epicli yaml docs
- [#1370](https://github.com/epiphany-platform/epiphany/issues/1370) - Epicli does not correctly generate vars for Postgres
- [#1296](https://github.com/epiphany-platform/epiphany/issues/1296) - Epicli does not interpret alternative yaml boolean values as true booleans
- [#2774](https://github.com/epiphany-platform/epiphany/issues/2774) - Issue creating service principal on Azure
- [#2788](https://github.com/epiphany-platform/epiphany/issues/2788) - Upgrade Log4j in Open Distro for Elasticsearch
- [#1221](https://github.com/epiphany-platform/epiphany/issues/1221) - kafka-exporter service doesn't start after restarting kafka VMs
- [#2332](https://github.com/epiphany-platform/epiphany/issues/2332) - [Elasticsearch] Error when having multiple VMs and non-clustered mode
- [#2707](https://github.com/epiphany-platform/epiphany/issues/2707) - Fix logging component backup
- [#2831](https://github.com/epiphany-platform/epiphany/issues/2831) - Fix postgres-exporter service errror: Error opening connection to database
- [#2894](https://github.com/epiphany-platform/epiphany/issues/2894) - System repositories are not restored on epicli re-run

## [1.0.1] 2021-07-16

### Fixed

- [#2319](https://github.com/epiphany-platform/epiphany/issues/2319) - [RHEL/Azure] RHUI client certificate expired for RHEL 7-LVM images
- [#2098](https://github.com/epiphany-platform/epiphany/issues/2098) - The default values can't be changed in cluster config file for virtual machine
- [#2233](https://github.com/epiphany-platform/epiphany/issues/2233) - Filebeat communication error in AKS
- [#2406](https://github.com/epiphany-platform/epiphany/issues/2406) - [Upgrade] [Filebeat] All settings for multiline feature are lost after upgrade
- [#1576](https://github.com/epiphany-platform/epiphany/issues/1576) - [Kafka] Incorrect number of brokers/queues available after scaling up/down
- [#2345](https://github.com/epiphany-platform/epiphany/issues/2345) - CoreDNS requires restart after scaling up nodes to be able to resolve new hostnames
- [#2360](https://github.com/epiphany-platform/epiphany/issues/2360) - [Upgrade] epicli may fail after re-running
- [#2381](https://github.com/epiphany-platform/epiphany/issues/2381) - Kibana fails to upgrade from epicli v1.0 to v1.1 (version comparison issue)

### Added

- [#2288](https://github.com/epiphany-platform/epiphany/issues/2288) - Allow to preserve OS images when run 'epicli apply' for existing cluster
- [#2127](https://github.com/epiphany-platform/epiphany/issues/2127) - Allow to specify configuration to be used in upgrade mode
- [#2129](https://github.com/epiphany-platform/epiphany/issues/2129) - [Upgrade] Add migration from ODFE demo certificates to generated ones

## [1.0.0] 2021-05-07

### Fixed

- [#2262](https://github.com/epiphany-platform/epiphany/issues/2262) - [Ubuntu] elasticsearch-curator in version 5.8.3 is not available from APT repo
- [#2259](https://github.com/epiphany-platform/epiphany/issues/2259) - [Upgrade] Automated tests fail when run after upgrade
- [#2292](https://github.com/epiphany-platform/epiphany/issues/2292) - PostgreSQL automated tests fail when run on a single machine
