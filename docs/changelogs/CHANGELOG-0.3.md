# Changelog 0.3

## [0.3.2] 2020-XX-XX

### Fixed

- [#1350](https://github.com/epiphany-platform/epiphany/issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm

## [0.3.1] 2020-04-20

### Fixed

- [#407](https://github.com/epiphany-platform/epiphany/issues/407) - Deployment/Application role fails because Kubernetes cluster is not ready after reboot.
- [#410](https://github.com/epiphany-platform/epiphany/issues/410) - Node_exporter ports are not present in defaults resulting in Prometheus not beeing able to scrape data with minimal cluster data.yaml.
- [#433](https://github.com/epiphany-platform/epiphany/issues/433) - Kafka exporter unnecessarily installed on RabbitMQ vms.
- [#548](https://github.com/epiphany-platform/epiphany/issues/548) - Epicli fails on AWS when clustering RabbitMQ nodes.
- [#549](https://github.com/epiphany-platform/epiphany/issues/549) - Need to allow traffic on port 5432 to enable PostgreSQL replication on AWS.
- [#839](https://github.com/epiphany-platform/epiphany/issues/839) - Add ServerAliveInterval option to keep SSH connection for long running tasks
- [#1016](https://github.com/epiphany-platform/epiphany/issues/1016) - Disable verify, backup and recovery as they are not fully implemented
- [#1105](https://github.com/epiphany-platform/epiphany/issues/1105) - [v0.3] failing on task: Install container-selinux for RHEL
- [#1106](https://github.com/epiphany-platform/epiphany/issues/1106) - [v0.3] Epicli exiting with exit code 0 despite errors
- [#1154](https://github.com/epiphany-platform/epiphany/issues/1154) - Node exporter is not installed on logging vms
- [#1163](https://github.com/epiphany-platform/epiphany/issues/1163) - [v0.4, v0.3] Typo in the role name rabbitmq
- Added default machines for rabbitmq and load_balancer components

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
