# Changelog 0.4

## [0.4.2] 2019-11-TOCHANGE

### Added

- Offline upgrade for K8n and Docker

### Fixed

- [#612](https://github.com/epiphany-platform/epiphany/issues/694) - epicli apply does not remove from build files removed from sources

## [0.4.1] 2019-10-17

### Fixed

- [#612](https://github.com/epiphany-platform/epiphany/issues/612) - 'epicli delete' - cannot delete a partially built infrastructure
- [#613](https://github.com/epiphany-platform/epiphany/pull/613) - Hotfixes for Ubuntu offline installation in air-gap mode
- [#614](https://github.com/epiphany-platform/epiphany/pull/614) - Fixed RotatingFileHandler permission error (for Docker Toolbox on Windows)
- [#615](https://github.com/epiphany-platform/epiphany/issues/615) - Minor Azure bugs for 0.4.0 release
- [#620](https://github.com/epiphany-platform/epiphany/issues/620) - Incorrect Ansible metadata (prerequisite) for Kubernetes Node

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