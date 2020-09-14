# Changelog 0.8

## [0.8.0] 2020-09-xx

### Added

- [#1302](https://github.com/epiphany-platform/epiphany/issues/1302) - Ability to update control plane certificates expiration date
- [#1324](https://github.com/epiphany-platform/epiphany/issues/1324) - Added Logstash to export data from Elasticsearch to csv format
- [#1300](https://github.com/epiphany-platform/epiphany/issues/1300) - Configure OpenSSH according to Mozilla Infosec guidance
- [#1543](https://github.com/epiphany-platform/epiphany/issues/1543) - Add support for Azure availability sets
- [#1609](https://github.com/epiphany-platform/epiphany/issues/1609) - Build epicli image using Dockerfile only (without shell script)
- [#765](https://github.com/epiphany-platform/epiphany/issues/765) - Added multiline support for logs statements in Filebeat
- [#1618](https://github.com/epiphany-platform/epiphany/issues/1618) - Add kubectl and Helm to epicli and devcontainer images

### Updated

- [#846](https://github.com/epiphany-platform/epiphany/issues/846) - Update Filebeat to v7.8.1
- [#1140](https://github.com/epiphany-platform/epiphany/issues/1140) - Upgrade Open Distro for Elasticsearch to v7.8.0
- [#1316](https://github.com/epiphany-platform/epiphany/issues/1316) - Upgrade HAProxy to v2.2

### Fixed

- Fix for changing Terraform templates between Epicli apply runs on Azure.
- [#1520](https://github.com/epiphany-platform/epiphany/issues/1520) - Added additional SANs to k8s-apiserver certificates to run kubectl outside the cluster
- [#1491](https://github.com/epiphany-platform/epiphany/issues/1491) - Error running upgrade on a 0.3 cluster: missing shared-config
