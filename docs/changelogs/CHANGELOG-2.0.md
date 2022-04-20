# Changelog 2.0

## [2.0.0] YYYY-MM-DD

### Added

- [#959](https://github.com/epiphany-platform/epiphany/issues/959) - Add usage of use_network_security_groups to disable NSG on AWS
- [#2701](https://github.com/epiphany-platform/epiphany/issues/2701) - Epicli prepare - generate files in separate directory
- [#2812](https://github.com/epiphany-platform/epiphany/issues/2812) - Extend K8s config validation
- [#2950](https://github.com/epiphany-platform/epiphany/issues/2950) - CLI refactor to make it more consistent
- [#2844](https://github.com/epiphany-platform/epiphany/issues/2844) - Refactor K8s upgrade task in order to simplify its flow
- [#2985](https://github.com/epiphany-platform/epiphany/issues/2985) - Make RabbitMQ Plugins configurable
- [#2974](https://github.com/epiphany-platform/epiphany/issues/2974) - Refactor Apply command
- [#2976](https://github.com/epiphany-platform/epiphany/issues/2976) - Allow for custom Terraform scripts
- [#2716](https://github.com/epiphany-platform/epiphany/issues/2716) - Change container runtime to containerd
- [#805](https://github.com/epiphany-platform/epiphany/issues/805) - Refactor download-requirements script
- [#2858](https://github.com/epiphany-platform/epiphany/issues/2858) - Make Ruby spec tests code compliant with rubocop lint rules
- [#2975](https://github.com/epiphany-platform/epiphany/issues/2975) - Copy only required files
- [#2991](https://github.com/epiphany-platform/epiphany/issues/2991) - Add automatic backup creation for download requirements
- [#2448](https://github.com/epiphany-platform/epiphany/issues/2448) - Passwordless SSH communication for postgres user between DB nodes
- [#2821](https://github.com/epiphany-platform/epiphany/issues/2821) - Node Exporter preflight checks
- [#2996](https://github.com/epiphany-platform/epiphany/issues/2996) - Introduce the new configuration field to change a component name
- [#2888](https://github.com/epiphany-platform/epiphany/issues/2888) - Define additional disks with defined sizes to VMs for Azure
- [#2812](https://github.com/epiphany-platform/epiphany/issues/2812) - Extend K8s config validation
- [#2890](https://github.com/epiphany-platform/epiphany/issues/2890) - Rook/Ceph Kubernetes Native Storage for Azure Kubernetes non-AKS cluster
- [#1452](https://github.com/epiphany-platform/epiphany/issues/1452) - Create Kubernetes Native Storage Epiphany configuration for Azure provider
- [#2891](https://github.com/epiphany-platform/epiphany/issues/2891) - Rook/Ceph Kubernetes Native Storage for AWS non-EKS
- [#2887](https://github.com/epiphany-platform/epiphany/issues/2887) - Create Kubernetes Native Storage Epiphany configuration for AWS provider

### Fixed

- [#2653](https://github.com/epiphany-platform/epiphany/issues/2653) - Epicli is failing in air-gapped infra mode
- [#1569](https://github.com/epiphany-platform/epiphany/issues/1569) - Azure unmanaged disks not supported by Epiphany but there is misleading setting in the default configuration
- [#2832](https://github.com/epiphany-platform/epiphany/issues/2832) - Make the DoD checklist clear
- [#2853](https://github.com/epiphany-platform/epiphany/issues/2853) - Change autoscaling_group approach in AWS provider in favor of plain VM creation.
- [#2669](https://github.com/epiphany-platform/epiphany/issues/2669) - Restarting the installation process can cause certificate problems if K8s was not fully configured
- [#2944](https://github.com/epiphany-platform/epiphany/issues/2944) - Refactor InitEngine class to be agnostic to changes in ApplyEngine and UpgradeEngine
- [#2945](https://github.com/epiphany-platform/epiphany/issues/2945) - epicli apply sleeps 10 seconds after creating inventory
- [#2968](https://github.com/epiphany-platform/epiphany/issues/2968) - `epicli init` should generate `specification.cloud.subscription_name` for minimal cluster config
- [#2940](https://github.com/epiphany-platform/epiphany/issues/2940) - firewalld.service unit could not be found on host however ansible_facts sees it as defined
- [#2979](https://github.com/epiphany-platform/epiphany/issues/2979) - Restore the possibility of choosing the availability zone in AWS
- [#2984](https://github.com/epiphany-platform/epiphany/issues/2984) - Validation blocks overwriting of destination_address_prefix in NSG rules, which is 0.0.0.0/0 by default
- [#2966](https://github.com/epiphany-platform/epiphany/issues/2966) - `epicli init --full` does not generate configuration for OpenDistro
- [#2942](https://github.com/epiphany-platform/epiphany/issues/2942) - rsync command fails trying to copy artifacts
- [#2930](https://github.com/epiphany-platform/epiphany/issues/2930) - Backup/recovery commands fail when default configuration for backup attached to cluster-config.yml
- [#2989](https://github.com/epiphany-platform/epiphany/issues/2989) - Task `Remove swap from /etc/fstab` does not remove swap entry from file
- [#2907](https://github.com/epiphany-platform/epiphany/issues/2907) - Backup/recovery commands fail when executed directly after upgrade
- [#3025](https://github.com/epiphany-platform/epiphany/issues/3025) - Running yum commands may hang waiting for user input
- [#2728](https://github.com/epiphany-platform/epiphany/issues/2728) - PostgreSQL's configuration files located outside the data directory are not copied by repmgr
- [#3029](https://github.com/epiphany-platform/epiphany/issues/3029) - [RHEL] Single machine upgrade fails on preflight check: 'dict object' has no attribute 'size_available'
- [#2997](https://github.com/epiphany-platform/epiphany/issues/2997) - Doubled HAProxy entries in prometheus.yml after upgrade
- [#2803](https://github.com/epiphany-platform/epiphany/issues/2803) - Refactor: rename 'kafka_var' setting
- [#2995](https://github.com/epiphany-platform/epiphany/issues/2995) - Update expired RHUI client certificate before installing any RHEL packages
- [#3049](https://github.com/epiphany-platform/epiphany/issues/3049) - HAProxy upgrade fails on re-run trying to remove haproxy_exporter
- [#3006](https://github.com/epiphany-platform/epiphany/issues/3006) - install 'containerd.io=1.4.12-*' failed, when upgrade from v1.3.0 to 2.0.0dev
- [#3065](https://github.com/epiphany-platform/epiphany/issues/3065) - Flag `delete_os_disk_on_termination` has no effect when removing cluster

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
- [#2871](https://github.com/epiphany-platform/epiphany/issues/2871) - Upgrade Kafka to 2.8.1
- [#3090](https://github.com/epiphany-platform/epiphany/issues/3090) - Update cloud OS images to the latest

### Removed

- [#2834](https://github.com/epiphany-platform/epiphany/issues/2834) - Removal of Hashicorp Vault component
- [#2833](https://github.com/epiphany-platform/epiphany/issues/2833) - Removal of Logstash component
- [#2836](https://github.com/epiphany-platform/epiphany/issues/2836) - Removal of Istio component
- [#2837](https://github.com/epiphany-platform/epiphany/issues/2837) - Removal of Apache Ignite component
- [#2927](https://github.com/epiphany-platform/epiphany/issues/2927) - Review Epiphany tools (remove outdated)
- [#2864](https://github.com/epiphany-platform/epiphany/issues/2864) - Remove unnecessary design docs

### Deprecated

### Breaking changes

- Upgrade of Terraform components in issue [#2825](https://github.com/epiphany-platform/epiphany/issues/2825) and [#2853](https://github.com/epiphany-platform/epiphany/issues/2853) will make running re-apply with infrastructure break on existing 1.x clusters. The advice is to deploy a new cluster and migrate data. If needed a manual upgrade path is described [here.](../home/howto/UPGRADE.md#terraform-upgrade-from-epiphany-1.x-to-2.x)
- Kubernetes container runtime changed. Dockershim and Docker are no longer on Kubernetes hosts.
- Filebeat `docker` input replaced by `container` input. New field provided for Filebeat as system service installation: `container.id`. Field `kubernetes.container.name` is no longer valid.

### Known issues
