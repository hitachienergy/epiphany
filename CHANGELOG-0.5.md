# Changelog 0.5

## [0.5.2] 2020-02-14

### Added

- PostgreSQL: PGBouncer implementation [#854](https://github.com/epiphany-platform/epiphany/issues/854)
- PostgreSQL: pgAudit extension for audit logging [#905](https://github.com/epiphany-platform/epiphany/pull/905)
- PostgreSQL: Send logs to Elasticsearch
- PostgreSQL: Add logrotate configuration [#915](https://github.com/epiphany-platform/epiphany/pull/915)

### Fixed

- Open Distro for Elasticsearch: Task 'Install Elasticsearch package' fails [#906](https://github.com/epiphany-platform/epiphany/issues/906)

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
