# Changelog 0.7

## [0.7.0] 2020-06-30

### Added

- [#1185](https://github.com/epiphany-platform/epiphany/issues/1185) - Epicli backup implementation
- [#1188](https://github.com/epiphany-platform/epiphany/issues/1188) - Backup: HAProxy
- [#885](https://github.com/epiphany-platform/epiphany/issues/885)   - Backup: Prometheus
- [#884](https://github.com/epiphany-platform/epiphany/issues/884)   - Backup: Elasticsearch and Kibana
- [#883](https://github.com/epiphany-platform/epiphany/issues/883)   - Backup: PostgreSQL
- [#1187](https://github.com/epiphany-platform/epiphany/issues/1187) - Backup: RabbitMQ Configuration

- [#1199](https://github.com/epiphany-platform/epiphany/issues/1199) - Epicli restore implementation
- [#1200](https://github.com/epiphany-platform/epiphany/issues/1200) - Restore: HAProxy
- [#1198](https://github.com/epiphany-platform/epiphany/issues/1198) - Restore: Prometheus
- [#1197](https://github.com/epiphany-platform/epiphany/issues/1197) - Restore: Elasticsearch and Kibana
- [#1195](https://github.com/epiphany-platform/epiphany/issues/1195) - Restore: PostgreSQL
- [#1285](https://github.com/epiphany-platform/epiphany/issues/1285) - Restore: RabbitMQ Configuration

- [#1149](https://github.com/epiphany-platform/epiphany/issues/1149) - Helm installation

- [#1191](https://github.com/epiphany-platform/epiphany/issues/1191) - Automatic Hashicorp Vault Agent installation, configuration and Kubernetes - Hashicorp Vault integration
- [#1190](https://github.com/epiphany-platform/epiphany/issues/1190) - Automatic Hashicorp Vault installation and configuration

### General

- [#811](https://github.com/epiphany-platform/epiphany/issues/811) - Measure execution time of Ansible tasks

### Updated

- Update Calico and Canal to v3.13.2
- [#1180](https://github.com/epiphany-platform/epiphany/issues/1180) - Update list of ports used by Epiphany components
- [#1310](https://github.com/epiphany-platform/epiphany/issues/1310) - Updated Azure-cli from 2.0.67 to 2.6.0
- [#1330](https://github.com/epiphany-platform/epiphany/issues/1330) - Update cloud based OS images
- [#1138](https://github.com/epiphany-platform/epiphany/issues/1138) - Upgrade Kubernetes to 1.17.7

### Fixed

- [#1154](https://github.com/epiphany-platform/epiphany/issues/1154) - Node exporter is not installed on logging vms
- [#1135](https://github.com/epiphany-platform/epiphany/issues/1135) - 2ndquadrant yum repos remain enabled on repository host after teardown
- [#1169](https://github.com/epiphany-platform/epiphany/issues/1169) - Task 'Get token from master' fails on-prem when calico plugin is used
- [#1181](https://github.com/epiphany-platform/epiphany/issues/1181) - Configure Ignite to use fixed ports
- [#1182](https://github.com/epiphany-platform/epiphany/issues/1182) - Re-run single machine installation may fail
- [#1209](https://github.com/epiphany-platform/epiphany/issues/1209) - Can not apply cluster, "sudo: a password is required"
- [#1183](https://github.com/epiphany-platform/epiphany/issues/1183) - Task 'Check if /etc/kubernetes/admin.conf file exists' fails when kubernetes\_master.count = 0
- [#1350](https://github.com/epiphany-platform/epiphany/issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm
- [#1372](https://github.com/epiphany-platform/epiphany/issues/1372) - [BUG] Epicli does not create Postgresql SET\_BY\_AUTOMATION values correctly
- [#1373](https://github.com/epiphany-platform/epiphany/issues/1373) - [BUG] permission denied for shared directory in the container when no volume was mounted
- [#1385](https://github.com/epiphany-platform/epiphany/issues/1385) - [BUG] Regression issue with disabling etcd encryption
- [#1399](https://github.com/epiphany-platform/epiphany/issues/1399) - [BUG] Epicli upgrade issue - the process hangs for several hours on the task kubeadm upgrade apply

### Known Issues

- [#1068](https://github.com/epiphany-platform/epiphany/issues/1068) - K8s HA installation - failing in some cases on task "Get token from master"
- [#1075](https://github.com/epiphany-platform/epiphany/issues/1075) - K8s HA installation - timed out on task "Join master to ControlPlane"
- [#1085](https://github.com/epiphany-platform/epiphany/issues/1085) - K8s HA installation - etcdserver: request timed out
- [#1086](https://github.com/epiphany-platform/epiphany/issues/1086) - K8s HA installation - Error from server: etcdserver: leader changed
- [#1072](https://github.com/epiphany-platform/epiphany/issues/1072) - AWS RedHat - cluster networking issues/lags using canal and flannel plugins
- [#1129](https://github.com/epiphany-platform/epiphany/issues/1129) - AWS cluster networking issues using calico plugin - NodePort service not always responding
