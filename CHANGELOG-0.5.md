# Changelog 0.5

## [0.5.0] 2020-01-17

### Added

- [#820](https://github.com/epiphany-platform/epiphany/pull/820) - Firewall: OS level firewall setup (firewalld)

### Added

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
