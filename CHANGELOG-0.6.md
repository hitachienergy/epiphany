# Changelog 0.6

## [0.6.1] 2020-10-14

### Fixed

- [#1154](../../issues/1154) - Node exporter is not installed on logging vms
- [#1183](../../issues/1183) - Task 'Check if /etc/kubernetes/admin.conf file exists' fails when kubernetes\_master.count = 0
- [#1350](../../issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm

## [0.6.0] 2020-04-06

### Added

#### General

- [#986](../../issues/986) - Add vim to Epicli container and devcontainer
- [#987](../../issues/987) - Add verbosity levels for Terraform and Ansible
- [#656](../../issues/656) - Add logrotation to kafka by size
- [#1016](../../issues/1016) - Disable verify, backup and recovery as they are not fully implemented
- [#1044](../../issues/1044) - Add ability to add subscriptionId to sp.yml on Azure
- [#991](../../issues/991) - During apply load only images that are required for current version

#### Kubernetes HA

- [#934](../../issues/934) - Kubernetes HA - Test automation
- [#933](../../issues/933) - Integrate K8s HA to epicli
- [#932](../../issues/932) - Create/update role to install K8s HA - Dashboard
- [#931](../../issues/931) - Create/update role to install K8s HA - Node Role
- [#930](../../issues/930) - Create/update role to install K8s HA - Master Role
- [#929](../../issues/929) - Single Machine installation - update epicli
- [#928](../../issues/928) - Single Machine installation - update tests
- [#927](../../issues/927) - Single Machine installation - lightweight installation

#### PostgresSQL HA

- [#973](../../issues/973) - Refactoring of PostgreSQL and apply new data model for configuration
- [#954](../../issues/954) - Change template generation logic for additional components and extensions in postgres
- [#921](../../issues/921) - Implement log rotation for PGBouncer
- [#876](../../issues/876) - RepManager installation and configuration for Ubuntu
- [#938](../../issues/938) - RepManager installation and configuration for RedHat
- [#912](../../issues/912) - Implementation: PGBouncer or equivalent - K8s version
- [#908](../../issues/908) - Add configurable log rotation for PostgreSQL
- [#888](../../issues/888) - QA: Create automatic tests for RepManager
- [#879](../../issues/879) - QA: Create automatic tests for PGAudit
- [#878](../../issues/878) - QA: Create automatic tests for PGBouncer
- [#877](../../issues/877) - QA: Create automatic tests for PGPool
- [#875](../../issues/875) - PGPool installation and configuration

### Updates

- [#850](../../issues/850) - Upgrade Kubernetes to latest
- [#890](../../issues/890) - Update upgrade role
- [#891](../../issues/891) - Update core-dns installation
- [#892](../../issues/892) - Update network plugins installation
- [#893](../../issues/893) - Update dashboard installation
- [#894](../../issues/894) - Update packages (requirements.txt)
- [#895](../../issues/895) - Update init/join configurations
- [#397](../../issues/397) - Update KeyCloak
- [#955](../../issues/955) - Update "applications" definitions to be compatible with K8s 1.17.4

### Fixed

- [#624](../../issues/624) - Don't run epicli as root in container
- [#966](../../issues/966) - Ubuntu builds get stuck on 'Create epirepo repository' task waiting for user input in offline mode
- [#1043](../../issues/1043) - For vm template on Azure disk_size_gb is missing in storage_os_disk
- [#1049](../../issues/1049) - Azure/RedHat specified disk size 30 GB is smaller than the size of the disk in the VM image
- [#1054](../../issues/1054) - Application configurations are not included with epicli init -full
- [#1063](../../issues/1063) - Issues with single_machine install
- [#1108](../../issues/1108) - [Azure RedHat] Create epirepo: package httpd-2.4.6-93 requires httpd-tools = 2.4.6-93 but latest available is 2.4.6-90
- [#1110](../../issues/1110) - Install fixed version of httpd when latest fails (RHEL)

### Known Issues

- [#1068](../../issues/1068) - K8s HA installation - failing in some cases on task "Get token from master"
- [#1075](../../issues/1075) - K8s HA installation - timed out on task "Join master to ControlPlane"
- [#1085](../../issues/1085) - K8s HA installation - etcdserver: request timed out
- [#1086](../../issues/1086) - K8s HA installation - Error from server: etcdserver: leader changed
- [#1072](../../issues/1072) - AWS RedHat - cluster networking issues/lags using canal and flannel plugins
- [#1129](../../issues/1129) - AWS cluster networking issues using calico plugin - NodePort service not always responding
