# Changelog 0.4

## [0.4.0] 2019-09-30

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

### Known issues

-