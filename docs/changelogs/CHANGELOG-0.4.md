# Changelog 0.4

## [0.4.5] 2020-XX-XX

### Fixed

- [#1350](https://github.com/epiphany-platform/epiphany/issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm

## [0.4.4] 2020-04-16

### Fixed

- [#966](https://github.com/epiphany-platform/epiphany/issues/966) - Ubuntu builds get stuck on 'Create epirepo repository' task waiting for user input in offline mode
- [#1043](https://github.com/epiphany-platform/epiphany/issues/1043) - For vm template on Azure disk_size_gb is missing in storage_os_disk
- [#1049](https://github.com/epiphany-platform/epiphany/issues/1049) - Azure/RedHat specified disk size 30 GB is smaller than the size of the disk in the VM image
- [#1063](https://github.com/epiphany-platform/epiphany/issues/1063) - Issues with single_machine install
- [#1108](https://github.com/epiphany-platform/epiphany/issues/1108) - [Azure RedHat] Create epirepo: package httpd-2.4.6-93 requires httpd-tools = 2.4.6-93 but latest available is 2.4.6-90
- [#1016](https://github.com/epiphany-platform/epiphany/issues/1016) - Disable verify, backup and recovery as they are not fully implemented
- [#1154](https://github.com/epiphany-platform/epiphany/issues/1154) - Node exporter is not installed on logging vms
- [#1163](https://github.com/epiphany-platform/epiphany/issues/1163) - [v0.4, v0.3] Typo in the role name rabbitmq

## [0.4.3] 2020-03-16

### Fixed

- [#966](https://github.com/epiphany-platform/epiphany/issues/966) - Ubuntu builds get stuck on task [repository : Create epirepo repository] waiting for user input
- [#839](https://github.com/epiphany-platform/epiphany/issues/839) - Add ServerAliveInterval option to keep SSH connection for long running tasks

## [0.4.2] 2019-11-20

### Added

- Online/offline upgrade of K8s, Docker and common packages

### Changed

- Removed legacy Epiphany from the repository
- [#617](https://github.com/epiphany-platform/epiphany/issues/617) - Docker images are loaded only on image registry host

### Fixed

- [#694](https://github.com/epiphany-platform/epiphany/issues/694) - epicli apply does not remove from build files that were removed from sources

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
