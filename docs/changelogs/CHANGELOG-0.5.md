# Changelog 0.5

## [0.5.5] 2020-XX-XX

### Fixed

- [#1350](https://github.com/epiphany-platform/epiphany/issues/1350) - Cannot deploy a non-k8s cluster with load\_balancer vm

## [0.5.4] 2020-04-14

### Added

- [#986](https://github.com/epiphany-platform/epiphany/issues/986) - Add vim to Epicli container and devcontainer
- [#1044](https://github.com/epiphany-platform/epiphany/issues/1044) - Add ability to add subscriptionId to sp.yml on Azure

### Fixed

- [#624](https://github.com/epiphany-platform/epiphany/issues/624) - Don't run epicli as root in container
- [#966](https://github.com/epiphany-platform/epiphany/issues/966) - Ubuntu builds get stuck on 'Create epirepo repository' task waiting for user input in offline mode
- [#1043](https://github.com/epiphany-platform/epiphany/issues/1043) - For vm template on Azure disk_size_gb is missing in storage_os_disk
- [#1049](https://github.com/epiphany-platform/epiphany/issues/1049) - Azure/RedHat specified disk size 30 GB is smaller than the size of the disk in the VM image
- [#1063](https://github.com/epiphany-platform/epiphany/issues/1063) - Issues with single_machine install
- [#1108](https://github.com/epiphany-platform/epiphany/issues/1108) - [Azure RedHat] Create epirepo: package httpd-2.4.6-93 requires httpd-tools = 2.4.6-93 but latest available is 2.4.6-90
- [#1110](https://github.com/epiphany-platform/epiphany/issues/1110) - Install fixed version of httpd when latest fails (RHEL)
- [#1016](https://github.com/epiphany-platform/epiphany/issues/1016) - Disable verify, backup and recovery as they are not fully implemented
- [#1154](https://github.com/epiphany-platform/epiphany/issues/1154) - Node exporter is not installed on logging vms

## [0.5.3] 2020-03-09

### Added

- Upgraded Epicli container and devcontainer from `python3.7-alpine` to `python:3.7-slim`
- Moved `epicli delete` out of experimental mode

### Fixed

- [#940](https://github.com/epiphany-platform/epiphany/issues/940) - Epicli init does not include any infrastructure documents
- [#611](https://github.com/epiphany-platform/epiphany/issues/611) - Lack of configuration/rabbitmq and configuration/postgresql after running epicli init --full
- [#736](https://github.com/epiphany-platform/epiphany/issues/736) - Running epicli init -p any --full generates cloud sample configuration instead of bare metal config
- [#942](https://github.com/epiphany-platform/epiphany/issues/942) - Additional security rules for NSGs are not applied properly for Azure
- [#951](https://github.com/epiphany-platform/epiphany/issues/951) - Fix PGBouncer to use v1.10 for all platforms
- [#945](https://github.com/epiphany-platform/epiphany/issues/945) - Disable NSG creation on Azure
- Fix for [CVE-2019-14864](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-14864)
- [#966](https://github.com/epiphany-platform/epiphany/issues/966) - Ubuntu builds get stuck on 'Create epirepo repository' task waiting for user input
- [#965](https://github.com/epiphany-platform/epiphany/issues/965) - Install Kibana on all logging vms

## [0.5.2] 2020-02-17

### Added

- [#854](https://github.com/epiphany-platform/epiphany/issues/854) - PostgreSQL: PGBouncer implementation
- [#905](https://github.com/epiphany-platform/epiphany/pull/905) - PostgreSQL: pgAudit extension for audit logging
- PostgreSQL: Send logs to Elasticsearch
- [#915](https://github.com/epiphany-platform/epiphany/pull/915) - PostgreSQL: Add logrotate configuration

### Fixed

- [#906](https://github.com/epiphany-platform/epiphany/issues/906) - Open Distro for Elasticsearch: Task 'Install Elasticsearch package' fails
- [#909](https://github.com/epiphany-platform/epiphany/issues/909) - Upgrade: Missing property 'name' when running epicli upgrade
- [#869](https://github.com/epiphany-platform/epiphany/issues/869) - Common: Issue installing Debian packages

### Known issues

- [#922](https://github.com/epiphany-platform/epiphany/issues/922) - Elasticsearch service not starting on RHEL after running epicli upgrade command

## [0.5.1] 2020-01-23

### Hotfixed

- [#849](https://github.com/epiphany-platform/epiphany/issues/849) - Firewall: Do not install firewalld package on Ubuntu
- [#842](https://github.com/epiphany-platform/epiphany/issues/842) - Firewall: Do not require kubernetes_master and kubernetes_node components
- Filebeat (Ubuntu): [Installing auditd sometimes fails in post-inst](https://bugs.launchpad.net/ubuntu/+source/auditd/+bug/1848330)
- Filebeat (Ubuntu): Restarting auditd service sometimes fails with error: "Job for auditd.service failed because a timeout was exceeded"
- Repository (RHEL/CentOS): Add second try for skopeo to avoid random error on Azure: "pinging docker registry returned: Get https://k8s.gcr.io/v2/: net/http: TLS handshake timeout"
- [#860](https://github.com/epiphany-platform/epiphany/issues/860) - Prometheus: K8s packages and their dependencies are installed on prometheus host

## [0.5.0] 2020-01-17

### Added

- [#820](https://github.com/epiphany-platform/epiphany/pull/820) - Firewall: OS level firewall setup (firewalld)
- [#381](https://github.com/epiphany-platform/epiphany/issues/381) - Add AWS EC2 Root Volume encryption
- [#782](https://github.com/epiphany-platform/epiphany/issues/781) - All disks encryption documentation - AWS
- [#782](https://github.com/epiphany-platform/epiphany/issues/782) - All disks encryption documentation - Azure
- [#784](https://github.com/epiphany-platform/epiphany/issues/784) - Switch to Open Distro for Elasticsearch
  - [Data storage](/docs/home/howto/DATABASES.md#how-to-start-working-with-opendistro-for-elasticsearch)
  - [Centralized logging](/docs/home/howto/LOGGING.md#centralized-logging-setup)

- [#755](https://github.com/epiphany-platform/epiphany/issues/755) - Create Ansible playbook to install Apache Ignite as a service on VM
  - [Stateful setup](/docs/home/howto/DATABASES.md#how-to-start-working-with-apache-ignite-stateful-setup)
- [#749](https://github.com/epiphany-platform/epiphany/issues/749) - Deploy stateless Apache Ignite on K8s
  - [Stateless setup](/docs/home/howto/DATABASES.md#how-to-start-working-with-apache-ignite-stateless-setup)
- [#831](https://github.com/epiphany-platform/epiphany/issues/831) - Build artifacts encryption (Kubernetes config) using ansible vault
  - [epicli asks for password](/docs/home/howto/SECURITY.md#how-to-run-epicli-with-password)

### Changed

- [#763](https://github.com/epiphany-platform/epiphany/pull/763) - Elasticsearch Curator: Flexible configuration of cron jobs
- [#763](https://github.com/epiphany-platform/epiphany/pull/763) - Elasticsearch Curator: Upgrade to v5.8.1
- [#766](https://github.com/epiphany-platform/epiphany/issues/766) - Elasticsearch: Upgrade to v6.8.5
- [#775](https://github.com/epiphany-platform/epiphany/issues/775) - Filebeat: Upgrade to v6.8.5
- [#752](https://github.com/epiphany-platform/epiphany/pull/752) - Kafka: Upgrade to v2.3.1
