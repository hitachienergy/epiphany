# Changelog 0.8

## [0.8.0] 2020-09-xx

### Added
- [#1324](https://github.com/epiphany-platform/epiphany/issues/1324) - Added Logstash to export data from Elasticsearch to csv format

- [#1300](https://github.com/epiphany-platform/epiphany/issues/1300) - Configure OpenSSH according to Mozilla Infosec guidance
- [#1543](https://github.com/epiphany-platform/epiphany/issues/1543) - Add support for Azure availability sets

### Updated

- [#846](https://github.com/epiphany-platform/epiphany/issues/846) - Update Filebeat to v7.8.1
- [#1140](https://github.com/epiphany-platform/epiphany/issues/1140) - Upgrade Open Distro for Elasticsearch to v7.8.0

### Fixed

- Fix for changing Terraform templates between Epicli apply runs on Azure.
- [#1520](https://github.com/epiphany-platform/epiphany/issues/1520) - Added additional SANs to k8s-apiserver certificates to run kubectl outside the cluster
- [#1491](https://github.com/epiphany-platform/epiphany/issues/1491) - Error running upgrade on a 0.3 cluster: missing shared-config
