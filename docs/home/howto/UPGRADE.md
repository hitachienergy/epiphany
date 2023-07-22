# Upgrade

- [Upgrade](#upgrade)
  - [Introduction](#introduction)
  - [Online upgrade](#online-upgrade)
    - [Online prerequisites](#online-prerequisites)
    - [Start the online upgrade](#start-the-online-upgrade)
  - [Offline upgrade](#offline-upgrade)
    - [Offline prerequisites](#offline-prerequisites)
    - [Start the offline upgrade](#start-the-offline-upgrade)
  - [Additional parameters](#additional-parameters)
  - [Run *apply* after *upgrade*](#run-apply-after-upgrade)
  - [Kubernetes applications](#kubernetes-applications)
  - [How to upgrade Kafka](#how-to-upgrade-kafka)
    - [Kafka upgrade](#kafka-upgrade)
    - [ZooKeeper upgrade](#zookeeper-upgrade)
  - [Node exporter upgrade](#node-exporter-upgrade)
  - [Kubernetes upgrade](#kubernetes-upgrade)
    - [Prerequisites](#prerequisites)
  - [PostgreSQL upgrade](#postgresql-upgrade)
    - [Versions](#versions)
    - [Prerequisites](#prerequisites-1)
    - [Upgrade](#upgrade-1)
    - [Manual actions](#manual-actions)
      - [Post-upgrade processing](#post-upgrade-processing)
      - [Statistics](#statistics)
      - [Delete old cluster](#delete-old-cluster)
  - [Terraform upgrade from Epiphany 1.x to 2.x](#terraform-upgrade-from-epiphany-1x-to-2x)
    - [Azure](#azure)
      - [v0.12.6 => v0.13.x](#v0126--v013x)
      - [v0.13.x => v0.14.x](#v013x--v014x)
      - [v0.14.x => v1.0.x](#v014x--v10x)
      - [v1.0.x => v1.1.3](#v10x--v113)
    - [AWS](#aws)
      - [v0.12.6 => v0.13.x](#v0126--v013x-1)
      - [v0.13.x => v0.14.x](#v013x--v014x-1)
      - [v0.14.x => v1.0.x](#v014x--v10x-1)
      - [v1.0.x => v1.1.3](#v10x--v113-1)

## Introduction

From Epicli 0.4.2 and up the CLI has the ability to perform upgrades on certain components on a cluster. The components
it currently can upgrade and will add are:

---
**NOTE**

There is an assertion to check whether K8s version is supported before running upgrade.

---

- Kubernetes (master and nodes). Supported versions: v1.18.6 (Epiphany 0.7.1+), v1.22.4 (Epiphany 1.3.0+)
- common: Upgrades all common configurations to match them to current Epiphany version
- repository: Adds the repository role needed for component installation in current Epiphany version
- image_registry: Adds the image_registry role needed for offline installation in current Epiphany version

The component upgrade takes the existing Ansible build output and based on that performs the upgrade of the currently
supported components. If you need to re-apply your entire Epiphany cluster a **manual** adjustment of the input yaml is
needed to the latest specification which then should be applied with `epicli apply...`. Please
see [Run apply after upgrade](./UPGRADE.md#run-apply-after-upgrade) chapter for more details.

Note about upgrade from pre-0.8 Epiphany:

- If you need to upgrade a cluster deployed with `epicli` in version earlier than 0.8, you should make sure that you've
  got enough disk space on master (which is used as repository). If you didn't extend OS disk on master during
  deployment process, you probably have only 32 GB disk which is not enough to properly upgrade cluster (we recommend at
  least 64 GB). Before you run upgrade, please extend OS disk on master machine according to cloud provider
  documentation: [AWS](https://aws.amazon.com/premiumsupport/knowledge-center/expand-root-ebs-linux/),
  [Azure](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks).

- If you use logging-machine(s) already in your cluster, it's necessary to scale up those machines before running
  upgrade. This allows to ensure you've got enough resources to run ELK stack in newer version. We recommend to use at
  least DS2_v2 Azure size (2 CPUs, 7 GB RAM) machine, or its equivalent on AWS and on-prem installations. It's very
  related to amount of data you'll store inside. Please see [logging](./LOGGING.md) documentation for more details.

## Online upgrade

### Online prerequisites

Your airgapped existing cluster should meet the following requirements:

1. The cluster machines/vm`s are connected by a network or virtual network of some sorts and can communicate which each
   other and have access to the internet:
2. The cluster machines/vm`s are **upgraded** to the following versions:
  - Ubuntu 20.04
3. The cluster machines/vm`s should be accessible through SSH with a set of SSH keys you provided and configured on each
   machine yourself.
4. A provisioning machine that:
- Has access to the SSH keys
- Has access to the build output from when the cluster was first created.
- Is on the same network as your cluster machines
- Has Epicli 0.4.2 or up running.
    *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

### Start the online upgrade

Start the upgrade with:

```shell
epicli upgrade -b /buildoutput/
```

This will backup and upgrade the Ansible inventory in the provided build folder `/buildoutput/` which will be used to
perform the upgrade of the components.

## Offline upgrade

### Offline prerequisites

Your airgapped existing cluster should meet the following requirements:

1. The airgapped cluster machines/vm`s are connected by a network or virtual network of some sorts and can communicate
   with each other:
2. The airgapped cluster machines/vm`s are **upgraded** to the following versions:
  - Ubuntu 20.04
3. The airgapped cluster machines/vm`s should be accessible through SSH with a set of SSH keys you provided and
   configured on each machine yourself.
4. A requirements machine that:
  - Runs the same distribution as the airgapped cluster machines/vm`s (Ubuntu 20.04)
  - Has access to the internet.
5. A provisioning machine that:
- Has access to the SSH keys
- Has access to the build output from when the cluster was first created.
- Is on the same network as your cluster machines
- Has Epicli 0.4.2 or up running.

---
**NOTE**

Before running `epicli`, check the [Prerequisites](./PREREQUISITES.md)

---

### Start the offline upgrade

To upgrade the cluster components run the following steps:

1. First we need to get the tooling to prepare the requirements for the upgrade. On the provisioning machine run:

    ```shell
    epicli prepare --os OS --arch ARCH
    ```

    Where:
    - OS should be `ubuntu-20.04`
    - ARCH should be `x86_64`

   This will create a directory called `prepare_scripts` with the needed files inside.

2. The scripts in the `prepare_scripts` will be used to download all requirements. To do that, copy
   the `prepare_scripts` folder over to the requirements machine and run the following command:

    ```shell
    download-requirements.py /requirementsoutput/ OS
    ```

    Where:
    - OS should be `ubuntu-20.04`, `detect`
    - /requirementsoutput/ where to output downloaded requirements

    This will run the download-requirements script for target OS type and save requirements under /requirementsoutput/. Once run successfully the `/requirementsoutput/` needs to be copied to the provisioning machine to be used later on.

3. Finally, start the upgrade with:

    ```shell
    epicli upgrade -b /buildoutput/ --offline-requirements /requirementsoutput/
    ```

   This will backup and upgrade the Ansible inventory in the provided build folder `/buildoutput/` which will be used to
   perform the upgrade of the components. The `--offline-requirements` flag tells Epicli where to find the folder with
   requirements (`/requirementsoutput/`) prepared in steps 1 and 2 which is needed for the offline upgrade.

## Additional parameters

The `epicli upgrade` command has additional flags:

- `--wait-for-pods`. When this flag is added, the Kubernetes upgrade will wait until all pods are in the **ready** state
  before proceeding. This can be useful when a zero downtime upgrade is required. **Note: that this can also cause the
  upgrade to hang indefinitely.**
- `--upgrade-components`. Specify comma separated component names, so the upgrade procedure will only process specific
  ones. List cannot be empty, otherwise execution will fail. By default, upgrade will process all components if this
  parameter is not provided

  Example:
   ```shell
   epicli upgrade -b /buildoutput/ --upgrade-components "kafka,filebeat"
   ```

---
**NOTE**

Parameter `--upgrade-components` should be use only for develop or testing purposes. Do not use this option for
production environments, since it may generate additional errors when running `apply` after that kind of upgrade

---

## Run *apply* after *upgrade*

Currently, Epiphany does not fully support apply after upgrade. There is a possibility to re-apply configuration from
newer version of Epicli but this needs some manual work from Administrator. Re-apply on already upgraded cluster needs
to be called with `--no-infra` option to skip Terraform part of configuration. If `apply` after `upgrade` is run
with `--no-infra`, the used system images from the older Epiphany version are preserved to prevent the destruction of
the VMs. If you plan modify any infrastructure unit (e.g., add Kubernetes Node) you need to create machine by yourself
and attach it into configuration yaml. While running `epicli apply...` on already upgraded cluster you should use yaml
config files generated in newer version of Epiphany and apply changes you had in older one. If the cluster is upgraded
to version 0.8 or newer you need also add additional feature mapping for repository role as shown on example below:

```yaml
---
kind: epiphany-cluster
name: clustername
provider: azure
specification:
  admin_user:
    key_path: /path/to/id_rsa
    name: operations
  components:
    repository:
      count: 0  # Set repository to 0 since it's introduced in v0.8
    kafka:
      count: 1
    kubernetes_master:
      count: 1
    kubernetes_node:
      count: 2
    load_balancer:
      count: 1
    logging:
      count: 1
    monitoring:
      count: 1
    postgresql:
      count: 1
  name: clustername
  prefix: 'prefix'
title: Epiphany cluster Config
---
kind: configuration/feature-mappings
title: "Feature mapping to components"
provider: azure
name: default
specification:
  mappings:
    kubernetes_master:
      - kubernetes-master
      - helm
      - applications
      - node-exporter
      - filebeat
      - firewall
      - repository      # add repository here
      - image-registry  # add image-registry here
...
```

## How to upgrade Kafka

### Kafka upgrade

Kafka will be automatically updated to the latest version supported by Epiphany. You can check the latest supported
version [here](../COMPONENTS.md#epiphany-cluster-components). Kafka brokers are updated one by one - but the update
procedure does not guarantee "zero downtime" because it depends on the number of available brokers, topics, and
partitioning configuration.
Note that old Kafka binaries are removed during upgrade.

### ZooKeeper upgrade

Redundant ZooKeeper configuration is also recommended, since service restart is required during upgrade - it can cause
ZooKeeper unavailability. Having **at least two ZooKeeper services** in *ZooKeepers ensemble* you can upgrade one and
then start with the rest **one by one**.

More detailed information about ZooKeeper you can find
in  [ZooKeeper documentation](https://cwiki.apache.org/confluence/display/ZOOKEEPER).

## Node exporter upgrade

---
**NOTE**

Before upgrade procedure, make sure you have a data backup, and you are familiar
with [breaking changes](https://github.com/prometheus/node_exporter/releases/tag/v1.0.0).

---

Starting from Epiphany v0.8.0 it's possible to upgrade node exporter according
to [components](/docs/home/COMPONENTS.md) file. Upgrade will
be performed automatically when the upgrade procedure detects node exporter hosts.
