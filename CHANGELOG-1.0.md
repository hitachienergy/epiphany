# Changelog 1.0

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
