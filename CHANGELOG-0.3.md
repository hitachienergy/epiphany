# Changelog 0.3

## [0.3.1] 2020-03-xx

### Fixed

- [#839](https://github.com/epiphany-platform/epiphany/issues/839) - Add ServerAliveInterval option to keep SSH connection for long running tasks

## [0.3.0] 2019-07-31

### Added

- Support for AWS cloud platform
- New Python based CLI - epicli. Currently supports AWS and baremetal deployments only
- Kubernetes automatic upgrade (experimental)
- Server spec tests for cluster components
- Added Canal as network plugin for Kubernetes
- Improved security

### Changed

- Kubernetes version 1.14.4
- Documentation cleanup and updates

### Fixed

- Fixed vulnerabilities for KeyCloak examples

### Known issues

- Deployment/Application role fails because Kubernetes cluster is not ready after reboot. More info [here](https://github.com/epiphany-platform/epiphany/issues/407)
- Node_exporter ports are not present in defaults resulting in Prometheus not beeing able to scrape data with minimal cluster data.yaml. More info [here](https://github.com/epiphany-platform/epiphany/issues/410)