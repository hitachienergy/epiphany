# Changelog 0.7

## [0.7.1] 2020-08-12

### Added

- Minor logging improvements added while fixing issue [#1424](../../issues/1424)
- [#1438](../../pull/1438) - Rename Terraform plugin vendor in VSCode recommendations
- [#1413](../../issues/1413) - Set protocol for Vault only in one place in configuration
- [#1423](../../issues/1423) - Error reading generated service principal

### Updated

- [#1479](../../issues/1479) - Upgrade K8s to v1.18.6
- [#1510](../../issues/1510) - Upgrade Kubernetes Dashboard to v2.0.3

### Fixed

- [#1424](../../issues/1424) - Terraform returning an error during deployments on Azure ("A retryable error occurred.")
- [#1399](../../issues/1399) - Epicli upgrade: Kubernetes upgrade may hang
- [#1398](../../issues/1398) - Vault installation fails when using canal/calico network plugin
- [#1412](../../issues/1412) - Certificate in Vault is also generated or copied even if flag in configuration tls_disable is set to true
- [#1408](../../issues/1408) - Epicli upgrade: Epiphany does not support upgrades for Kubernetes in HA mode
- [#1482](../../issues/1482) - Epicli upgrade: flannel CNI plugin is not upgraded to v0.12.0
- [#1462](../../issues/1461) - Epicli upgrade: [AWS/RHEL/calico] Upgrading cluster from 0.6 to 0.7 fails
- [#1072](../../issues/1072) - [AWS/RHEL] Cluster networking issues/lags when using flannel/canal plugin
- [#802](../../issues/802) - Docker version is hard-coded in installation tasks
- [#1495](../../issues/1495) - Offline installation is broken for CentOS 7.8 environments
- [#1347](../../issues/1347) - Kibana config always points its elasticsearch.hosts to a "logging" VM
- [#1336](../../issues/1336) - Deployment of version 0.7.0 failed on-prem (spec.hostname)
- [#1394](../../issues/1394) - Cannot access Kubernetes dashboard after upgrading

## [0.7.0] 2020-06-30

### Added

- [#1185](../../issues/1185) - Epicli backup implementation
- [#1188](../../issues/1188) - Backup: HAProxy
- [#885](../../issues/885)   - Backup: Prometheus
- [#884](../../issues/884)   - Backup: Elasticsearch and Kibana
- [#883](../../issues/883)   - Backup: PostgreSQL
- [#1187](../../issues/1187) - Backup: RabbitMQ Configuration

- [#1199](../../issues/1199) - Epicli restore implementation
- [#1200](../../issues/1200) - Restore: HAProxy
- [#1198](../../issues/1198) - Restore: Prometheus
- [#1197](../../issues/1197) - Restore: Elasticsearch and Kibana
- [#1195](../../issues/1195) - Restore: PostgreSQL
- [#1285](../../issues/1285) - Restore: RabbitMQ Configuration

- [#1149](../../issues/1149) - Helm installation

- [#1191](../../issues/1191) - Automatic Hashicorp Vault Agent installation, configuration and Kubernetes - Hashicorp Vault integration
- [#1190](../../issues/1190) - Automatic Hashicorp Vault installation and configuration

### General

- [#811](../../issues/811) - Measure execution time of Ansible tasks

### Updated

- Update Calico and Canal to v3.13.2
- [#1180](../../issues/1180) - Update list of ports used by Epiphany components
- [#1310](../../issues/1310) - Updated Azure-cli from 2.0.67 to 2.6.0
- [#1330](../../issues/1330) - Update cloud based OS images
- [#1138](../../issues/1138) - Upgrade Kubernetes to 1.17.70
- [#1395](../../issues/1395) - Upgrade RabbitMQ from 3.7.10 to 3.8.3

### Fixed

- [#1154](../../issues/1154) - Node exporter is not installed on logging vms
- [#1135](../../issues/1135) - 2ndquadrant yum repos remain enabled on repository host after teardown
- [#1169](../../issues/1169) - Task 'Get token from master' fails on-prem when calico plugin is used
- [#1181](../../issues/1181) - Configure Ignite to use fixed ports
- [#1182](../../issues/1182) - Re-run single machine installation may fail
- [#1209](../../issues/1209) - Can not apply cluster, "sudo: a password is required"
- [#1183](../../issues/1183) - Task 'Check if /etc/kubernetes/admin.conf file exists' fails when kubernetes\_master.count = 0
- [#1350](../../issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm
- [#1372](../../issues/1372) - [BUG] Epicli does not create Postgresql SET\_BY\_AUTOMATION values correctly
- [#1373](../../issues/1373) - [BUG] permission denied for shared directory in the container when no volume was mounted
- [#1385](../../issues/1385) - [BUG] Regression issue with disabling etcd encryption

### Known Issues

- [#1068](../../issues/1068) - K8s HA installation - failing in some cases on task "Get token from master"
- [#1075](../../issues/1075) - K8s HA installation - timed out on task "Join master to ControlPlane"
- [#1085](../../issues/1085) - K8s HA installation - etcdserver: request timed out
- [#1086](../../issues/1086) - K8s HA installation - Error from server: etcdserver: leader changed
- [#1072](../../issues/1072) - AWS RedHat - cluster networking issues/lags using canal and flannel plugins
- [#1129](../../issues/1129) - AWS cluster networking issues using calico plugin - NodePort service not always responding
