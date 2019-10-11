# Changelog 0.4

## [0.4.0] 2019-10-11

### Added

- Offline installation
- Azure cluster deployments with Epicli
- Delete commands to remove clusters from cloud providers (AWS, Azure)
- Devcontainer for Epicli development using VSCode
- Debug flag for Epicli

### Changed

- Various improvements in Epicli
- Documentation cleanup and updates

### Fixed

- [#407](https://github.com/epiphany-platform/epiphany/issues/407) - Deployment/Application role fails because Kubernetes cluster is not ready after reboot.
- [#410](https://github.com/epiphany-platform/epiphany/issues/410) - Node_exporter ports are not present in defaults resulting in Prometheus not beeing able to scrape data with minimal cluster data.yaml.
- [#548](https://github.com/epiphany-platform/epiphany/issues/548) - Epicli fails on AWS when clustering RabbitMQ nodes.
- [#549](https://github.com/epiphany-platform/epiphany/issues/549) - Need to allow traffic on port 5432 to enable PostgreSQL replication on AWS.

### Known issues

-