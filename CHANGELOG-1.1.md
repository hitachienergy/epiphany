# Changelog 1.1

## [1.1.0] YYYY-MM-DD

### Added

- [#1710](https://github.com/epiphany-platform/epiphany/issues/1710) - Add/extend retry functionality for all network related commands in download-requirements.sh
- [#2033](https://github.com/epiphany-platform/epiphany/issues/2033) - [ARM64] Add arm64 support to 'repository' component
- [#2109](https://github.com/epiphany-platform/epiphany/issues/2109) - [ARM64] Add arm64 support to 'kubernetes_master' and 'kubernetes_node' components
- [#2110](https://github.com/epiphany-platform/epiphany/issues/2111) - [ARM64] Add arm64 support to 'kafka' component
- [#2111](https://github.com/epiphany-platform/epiphany/issues/2111) - [ARM64] Add arm64 support to 'load_balancer' component
- [#2112](https://github.com/epiphany-platform/epiphany/issues/2112) - [ARM64] Add arm64 support to 'postgresql' component
- [#2113](https://github.com/epiphany-platform/epiphany/issues/2113) - [ARM64] Add arm64 support to 'applications' Ansible role to install 'Keycloak'
- [#2116](https://github.com/epiphany-platform/epiphany/issues/2116) - [ARM64] Add arm64 support to 'logging' component
- [#2117](https://github.com/epiphany-platform/epiphany/issues/2117) - [ARM64] Add arm64 support to 'monitoring' component
- [#2118](https://github.com/epiphany-platform/epiphany/issues/2118) - [ARM64] Block the install of unsupported components/roles on arm64
- [#2114](https://github.com/epiphany-platform/epiphany/issues/2114) - [ARM64] Add arm64 support to 'rabbitmq' component
- [#2225](https://github.com/epiphany-platform/epiphany/issues/2225) - [ARM64] Add arm64 support for RabbitMQ and Ignite K8s applications
- [#2241](https://github.com/epiphany-platform/epiphany/issues/2241) - [ARM64] Add arm64 support to 'vault' component
- [#2243](https://github.com/epiphany-platform/epiphany/issues/2243) - Configure Elasticsearch to use static (single) ports instead of ranges
- [#1914](https://github.com/epiphany-platform/epiphany/issues/1914) - Default plugins in Open Distro for Elasticsearch Kibana documented

### Fixed

- [#2098](https://github.com/epiphany-platform/epiphany/issues/2098) - The default values can't be changed in cluster config file for virtual machine
- [#2244](https://github.com/epiphany-platform/epiphany/issues/2244) - [Upgrade] Elasticsearch settings hard-coded instead of read from existing configuration file
- [#2247](https://github.com/epiphany-platform/epiphany/issues/2247) - [Upgrade] Automated tests fail when run after upgrade
- [#2262](https://github.com/epiphany-platform/epiphany/issues/2262) - [Ubuntu] elasticsearch-curator in version 5.8.3 is not available from APT repo
- [#2233](https://github.com/epiphany-platform/epiphany/issues/2233) - Filebeat communication error in AKS
- [#2291](https://github.com/epiphany-platform/epiphany/issues/2291) - PostgreSQL automated tests fail when run on a single machine
- [#2215](https://github.com/epiphany-platform/epiphany/issues/2215) - Grafana does not show metrics from kafka and haproxy exporters

### Updated

- [#2144](https://github.com/epiphany-platform/epiphany/issues/2144) - Update Epiphany support policy matrix
- [#2117](https://github.com/epiphany-platform/epiphany/issues/2117) - [AMD64/ARM64] Postgres exporter updated to version 0.9.0
- [#2241](https://github.com/epiphany-platform/epiphany/issues/2241) - [AMD64/ARM64] Vault (k8s) updated to version 0.10.0, helm chart with Vault updated to version 0.11.0 and Hashicorp Vault updated to version 1.7.0
- [#2116](https://github.com/epiphany-platform/epiphany/issues/2116) - [AMD64/ARM64] Logstash updated to version 7.12.0

### Breaking changes

### Known issues
