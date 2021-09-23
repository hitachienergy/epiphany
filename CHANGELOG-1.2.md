# Changelog 1.2

## [1.2.0] YYYY-MM-DD

### Added

- [#126](https://github.com/epiphany-platform/epiphany/issues/126) - Added default Kibana dashboards
- [#2127](https://github.com/epiphany-platform/epiphany/issues/2127) - Allow to specify configuration to be used in upgrade mode
- [#2397](https://github.com/epiphany-platform/epiphany/issues/2397) - Restart CoreDNS pods conditionally
- [#195](https://github.com/epiphany-platform/epiphany/issues/195) - Basic configuration type and schema validation
- [#2434](https://github.com/epiphany-platform/epiphany/issues/2434) - Python 3 installation
- [#2346](https://github.com/epiphany-platform/epiphany/issues/2346) - Allow more than 2 PostgreSQL nodes installation with repmgr
- [#2124](https://github.com/epiphany-platform/epiphany/issues/2124) - Added Internet connection test to download-requirements.sh
- [#2531](https://github.com/epiphany-platform/epiphany/issues/2531) - Add Pylint configuration to epicli devcontainer
- [#1892](https://github.com/epiphany-platform/epiphany/issues/1892) - Add ansible-lint to epicli devcontainer
- [#2558](https://github.com/epiphany-platform/epiphany/issues/2558) - Add rubocop to epicli devcontainer
- [#2271](https://github.com/epiphany-platform/epiphany/issues/2271) - Add more retries for running ansible ping command

### Fixed

- [#2406](https://github.com/epiphany-platform/epiphany/issues/2406) - [Upgrade] [Filebeat] All settings for multiline feature are lost after upgrade
- [#2380](https://github.com/epiphany-platform/epiphany/issues/2380) - Unable to drain nodes with Istio application enabled due to PodDisruptionBudgets
- [#2332](https://github.com/epiphany-platform/epiphany/issues/2332) - [Elasticsearch] Error when having multiple VMs and non-clustered mode
- [#1294](https://github.com/epiphany-platform/epiphany/issues/1294) - Implement proper merging of lists of dictionaries for epicli yaml docs
- [#1370](https://github.com/epiphany-platform/epiphany/issues/1370) - Epicli does not correctly generate vars for Postgres
- [#2425](https://github.com/epiphany-platform/epiphany/issues/2425) - Feature-mapping - 'enabled: no' do nothing
- [#2449](https://github.com/epiphany-platform/epiphany/issues/2449) - [Grafana] Unable to add Grafana repository
- [#2485](https://github.com/epiphany-platform/epiphany/issues/2485) - [Upgrade] Refactor upgrade role to not include "specification" at top level
- [#2521](https://github.com/epiphany-platform/epiphany/issues/2521) - Fix 2 unit tests that are marked to be skipped during test execution
- [#2542](https://github.com/epiphany-platform/epiphany/issues/2542) - Non critical error in epicli if no 'path' is provided
- [#1296](https://github.com/epiphany-platform/epiphany/issues/1296) - Epicli does not interpret alternative yaml boolean values as true booleans

### Updated

- [#2075](https://github.com/epiphany-platform/epiphany/issues/2075) - Upgrade of Pgpool to v4.2.4
- [#2076](https://github.com/epiphany-platform/epiphany/issues/2076) - Upgrade of PgBouncer [Kubernetes] to v1.16.0
- [#1797](https://github.com/epiphany-platform/epiphany/issues/1797) - Upgrade Keycloak to v14.0.0
- [#1861](https://github.com/epiphany-platform/epiphany/issues/1861) - Upgrade PostgreSQL to v13
- [#2074](https://github.com/epiphany-platform/epiphany/issues/2074) - Upgrade repmgr to v5.2.1
- [#2077](https://github.com/epiphany-platform/epiphany/issues/2077) - Upgrade PgAudit to v1.5.0
- [#2453](https://github.com/epiphany-platform/epiphany/issues/2453) - Upgrade PgBouncer to v1.16.0 [standalone]
- [#2457](https://github.com/epiphany-platform/epiphany/issues/2457) - Upgrade Docker-CE to v20.10.8
- [#2511](https://github.com/epiphany-platform/epiphany/issues/2511) - Upgrade Python packages to at least the latest patch version.
- [#2591](https://github.com/epiphany-platform/epiphany/issues/2591) - Update OS cloud images to the latest
- [#2578](https://github.com/epiphany-platform/epiphany/issues/2578) - Update documentation on how to upgrade PostgreSQL

### Deprecated

- PgBouncer standalone installation will be removed in the next release.


### Breaking changes

### Known issues
