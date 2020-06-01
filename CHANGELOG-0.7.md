# Changelog 0.7

## [0.7.0] 2020-0X-XX

### Added

#### General

- [#811](https://github.com/epiphany-platform/epiphany/issues/811) - Measure execution time of Ansible tasks

### Updated

- Update Calico and Canal to v3.13.2
- [#1180](https://github.com/epiphany-platform/epiphany/issues/1180) - Update list of ports used by Epiphany components
- [#1310](https://github.com/epiphany-platform/epiphany/issues/1310) - Updated Azure-cli from to 2.0.67 to 2.6.0

### Fixed

- [#1154](https://github.com/epiphany-platform/epiphany/issues/1154) - Node exporter is not installed on logging vms
- [#1135](https://github.com/epiphany-platform/epiphany/issues/1135) - 2ndquadrant yum repos remain enabled on repository host after teardown
- [#1169](https://github.com/epiphany-platform/epiphany/issues/1169) - Task 'Get token from master' fails on-prem when calico plugin is used
- [#1181](https://github.com/epiphany-platform/epiphany/issues/1181) - Configure Ignite to use fixed ports
- [#1182](https://github.com/epiphany-platform/epiphany/issues/1182) - Re-run single machine installation may fail
- [#1209](https://github.com/epiphany-platform/epiphany/issues/1209) - Can not apply cluster, "sudo: a password is required"

### Known Issues

- [#1068](https://github.com/epiphany-platform/epiphany/issues/1068) - K8s HA installation - failing in some cases on task "Get token from master"
- [#1075](https://github.com/epiphany-platform/epiphany/issues/1075) - K8s HA installation - timed out on task "Join master to ControlPlane"
- [#1085](https://github.com/epiphany-platform/epiphany/issues/1085) - K8s HA installation - etcdserver: request timed out
- [#1086](https://github.com/epiphany-platform/epiphany/issues/1086) - K8s HA installation - Error from server: etcdserver: leader changed
- [#1072](https://github.com/epiphany-platform/epiphany/issues/1072) - AWS RedHat - cluster networking issues/lags using canal and flannel plugins
- [#1129](https://github.com/epiphany-platform/epiphany/issues/1129) - AWS cluster networking issues using calico plugin - NodePort service not always responding
