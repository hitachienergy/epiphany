# Changelog 2.0

## [2.0.0] YYYY-MM-DD

### Added

- [#2701](https://github.com/epiphany-platform/epiphany/issues/2701) - Epicli prepare - generate files in separate directory
- [#2812](https://github.com/epiphany-platform/epiphany/issues/2812) - Extend K8s config validation
- [#2844](https://github.com/epiphany-platform/epiphany/issues/2844) - Refactor K8s upgrade task in order to simplify its flow

### Fixed

- [#2653](https://github.com/epiphany-platform/epiphany/issues/2653) - Epicli is failing in air-gapped infra mode
- [#1569](https://github.com/epiphany-platform/epiphany/issues/1569) - Azure unmanaged disks not supported by Epiphany but there is misleading setting in the default configuration
- [#2832](https://github.com/epiphany-platform/epiphany/issues/2832) - Make the DoD checklist clear

- [#2669](https://github.com/epiphany-platform/epiphany/issues/2669) - Restarting the installation process can cause certificate problems if K8s was not fully configured

### Updated

- [#2828](https://github.com/epiphany-platform/epiphany/issues/2828) - K8s improvements
  - Re-generate apiserver certificates only by purpose
  - Do not ignore preflight errors in `kubeadm join`
  - Update documentation about control plane certificates renewal
- [#2825](https://github.com/epiphany-platform/epiphany/issues/2825) - Upgrade Terraform and providers
  - Terraform 0.12.6 to 1.1.3 ([#2706](https://github.com/epiphany-platform/epiphany/issues/2706))
  - Azurerm provider 1.38.0 to 2.91.0
  - AWS provider 2.26 to 3.71.0
  - Upgraded Azure-cli 2.29 to 2.32
- [#2847](https://github.com/epiphany-platform/epiphany/issues/2847) - Upgrade Ansible to 5.2.0
  - Ansible 2.10.15 to 5.2.0
  - Python 3.7 to 3.10

### Removed

- [#2834](https://github.com/epiphany-platform/epiphany/issues/2834) - Removal of Hashicorp Vault component
- [#2833](https://github.com/epiphany-platform/epiphany/issues/2833) - Removal of Logstash component
- [#2836](https://github.com/epiphany-platform/epiphany/issues/2836) - Removal of Istio component
- [#2837](https://github.com/epiphany-platform/epiphany/issues/2837) - Removal of Apache Ignite component

### Deprecated


### Breaking changes

- Upgrade of Terraform components in issue [#2825](https://github.com/epiphany-platform/epiphany/issues/2825) will make running re-apply with infrastructure break on existing 1.x clusters. The advice is to deploy a new cluster and migrate data. If needed a manual upgrade path is described [here.](../home/howto/UPGRADE.md#terraform-upgrade-from-epiphany-1.x-to-2.x)

### Known issues
