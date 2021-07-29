# Changelog 1.2

## [1.2.0] YYYY-MM-DD

### Added

- [#126](https://github.com/epiphany-platform/epiphany/issues/126) - Added default Kibana dashboards
- [#2127](https://github.com/epiphany-platform/epiphany/issues/2127) - Allow to specify configuration to be used in upgrade mode
- [#2397](https://github.com/epiphany-platform/epiphany/issues/2397) - Restart CoreDNS pods conditionally
- [#195](https://github.com/epiphany-platform/epiphany/issues/195) - Basic configuration type and schema validation

### Fixed

- [#2406](https://github.com/epiphany-platform/epiphany/issues/2406) - [Upgrade] [Filebeat] All settings for multiline feature are lost after upgrade
- [#2380](https://github.com/epiphany-platform/epiphany/issues/2380) - Unable to drain nodes with Istio application enabled due to PodDisruptionBudgets
- [#2332](https://github.com/epiphany-platform/epiphany/issues/2332) - [Elasticsearch] Error when having multiple VMs and non-clustered mode

### Updated

- [#1797](https://github.com/epiphany-platform/epiphany/issues/1797) - Upgrade Keycloak to v14.0.0
- [#2074](https://github.com/epiphany-platform/epiphany/issues/2074) - Upgrade repmgr to 5.2.1

### Deprecated

### Breaking changes

- [#195](https://github.com/epiphany-platform/epiphany/issues/195) - Basic configuration type and schema validation
  yes|no defined boolean values in the input schema will no longer be allowed as jsonschema used for validation requires
  true|false for booleans. The yes|no values need to be changed to true|false respectively.

### Known issues
