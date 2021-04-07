# Changelog 0.11

## [0.11.0] YYYY-MM-DD

### Added

- [#1710](https://github.com/epiphany-platform/epiphany/issues/1710) - Add/extend retry functionality for all network related commands in download-requirements.sh
- [#2033](https://github.com/epiphany-platform/epiphany/issues/2033) - [ARM64] Add arm64 support to 'repository' component
- [#2109](https://github.com/epiphany-platform/epiphany/issues/2109) - [ARM64] Add arm64 support to 'kubernetes_master' and 'kubernetes_node' components
- [#2110](https://github.com/epiphany-platform/epiphany/issues/2111) - [ARM64] Add arm64 support to 'kafka' component
- [#2111](https://github.com/epiphany-platform/epiphany/issues/2111) - [ARM64] Add arm64 support to 'load_balancer' component
- [#2243](https://github.com/epiphany-platform/epiphany/issues/2243) - Configure Elasticsearch to use static (single) ports instead of ranges

### Fixed

- [#2098](https://github.com/epiphany-platform/epiphany/issues/2098) - The default values can't be changed in cluster config file for virtual machine
- [#2244](https://github.com/epiphany-platform/epiphany/issues/2244) - [Upgrade] Elasticsearch settings hard-coded instead of read from existing configuration file
- [#2247](https://github.com/epiphany-platform/epiphany/issues/2247) - [Upgrade] Automated tests fail when run after upgrade
- [#2262](https://github.com/epiphany-platform/epiphany/issues/2262) - [Ubuntu] elasticsearch-curator in version 5.8.3 is not available from APT repo


### Updated
- [#2144](https://github.com/epiphany-platform/epiphany/issues/2144) - Update Epiphany support policy matrix

### Breaking changes

### Known issues
