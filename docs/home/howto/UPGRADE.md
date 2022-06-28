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
  - [Migration from Open Distro for Elasticsearch & Kibana to OpenSearch and OpenSearch Dashboards](#migration-from-open-distro-for-elasticsearch--kibana-to-opensearch-and-opensearch-dashboards)
  - [Open Distro for Elasticsearch upgrade](#open-distro-for-elasticsearch-upgrade)
  - [Node exporter upgrade](#node-exporter-upgrade)
  - [RabbitMQ upgrade](#rabbitmq-upgrade)
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
  - AlmaLinux 8.4+
  - RedHat 8.4+
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
  - AlmaLinux 8.4+
  - RedHat 8.4+
  - Ubuntu 20.04
3. The airgapped cluster machines/vm`s should be accessible through SSH with a set of SSH keys you provided and
   configured on each machine yourself.
4. A requirements machine that:
  - Runs the same distribution as the airgapped cluster machines/vm`s (AlmaLinux 8, RedHat 8, Ubuntu 20.04)
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
    - OS should be `almalinux-8`, `rhel-8`, `ubuntu-20.04`
    - ARCH should be `x86_64`, `arm64`

   This will create a directory called `prepare_scripts` with the needed files inside.

2. The scripts in the `prepare_scripts` will be used to download all requirements. To do that, copy
   the `prepare_scripts` folder over to the requirements machine and run the following command:

    ```shell
    download-requirements.py /requirementsoutput/ OS
    ```

    Where:
    - OS should be `almalinux-8`, `rhel-8`, `ubuntu-20.04`, `detect`
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
    rabbitmq:
      count: 0
    opensearch:
      count: 0
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

## Kubernetes applications

To upgrade applications on Kubernetes to the desired version after `epicli upgrade` you have to:

- generate new configuration manifest using `epicli init`
- in case of generating minimal configuration manifest (without --full argument), copy and
  paste [the default configuration](https://github.com/epiphany-platform/epiphany/blob/develop/schema/common/defaults/configuration/applications.yml)
  into it
- run `epicli apply`

---
**NOTE**

The above link points to develop branch. Please choose the right branch that suits to Epiphany version you are using.

---

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

## Migration from Open Distro for Elasticsearch & Kibana to OpenSearch and OpenSearch Dashboards

---
**NOTE**

Make sure you have a backup before proceeding to migration steps described below!

---
Following the decision of Elastic NV<sup>[1]</sup> on ceasing open source options available for Elasticsearch and Kibana and releasing them under the Elastic license (more info [here](https://github.com/epiphany-platform/epiphany/issues/2870)) Epiphany team decided to implement a mechanism of automatic migration from ElasticSearch 7.10.2 to OpenSearch 1.2.4.

It is important to remember, that while the new platform makes an effort to continue to support a broad set of third party tools (ie. Beats) there can be some drawbacks or even malfunctions as not everything has been tested or has explicitly been added to OpenSearch compatibility scope<sup>[2]</sup>.
Additionally some of the components (ie. ElasticSearch Curator) or some embedded service accounts ( ie. *kibanaserver*) can be still found in OpenSearch environment but they will be phased out.

Keep in mind, that for the current version of OpenSearch and OpenSearch Dashboards it is necessary to include the `filebeat` component along with the loggging one in order to implement the workaround for *Kibana API not available* [bug](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/656#issuecomment-978036236).

Upgrade of the ESS/ODFE versions not shipped with the previous Epiphany releases is not supported. If your environment is customized it needs to be standardized ( as described in [this](https://opensearch.org/docs/latest/upgrade-to/upgrade-to/#upgrade-paths) table ) prior to running the subject migration.

Migration of Elasticsearch Curator is not supported. More info on use of Curator in OpenSearch environment can be found [here](https://github.com/opensearch-project/OpenSearch/issues/1352).

<sup>[1]</sup> https://www.elastic.co/pricing/faq/licensing#what-are-the-key-changes-being-made-to-the-elastic-license

<sup>[2]</sup> https://opensearch.org/docs/latest/clients/agents-and-ingestion-tools/index/

Upgrade will be performed automatically when the upgrade procedure detects your `logging`, `opensearch` or `kibana` hosts.

Upgrade of Elasticsearch uses API calls (GET, PUT, POST) which requires an admin TLS certificate. By default, Epiphany
generates self-signed certificates for this purpose but if you use your own, you have to provide the admin certificate's
location. To do that, edit the following settings changing `cert_path` and `key_path`.

```yaml
logging:
  upgrade_config:
    custom_admin_certificate:
      cert_path: /etc/elasticsearch/custom-admin.pem
      key_path: /etc/elasticsearch/custom-admin-key.pem

opensearch:
  upgrade_config:
    custom_admin_certificate:
      cert_path: /etc/elasticsearch/custom-admin.pem
      key_path: /etc/elasticsearch/custom-admin-key.pem
```

They are accessible via the defaults of `upgrade`
role (`/usr/local/epicli/data/common/ansible/playbooks/roles/upgrade/defaults/main.yml`).

## Node exporter upgrade

---
**NOTE**

Before upgrade procedure, make sure you have a data backup, and you are familiar
with [breaking changes](https://github.com/prometheus/node_exporter/releases/tag/v1.0.0).

---

Starting from Epiphany v0.8.0 it's possible to upgrade node exporter according
to [components](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/COMPONENTS.md) file. Upgrade will
be performed automatically when the upgrade procedure detects node exporter hosts.

## RabbitMQ upgrade

---
**NOTE**

Before upgrade procedure, make sure you have a data backup. Check that the node or cluster is in a good state: no alarms
are in effect, no ongoing queue synchronisation operations and the system is otherwise under a reasonable load. For more
information visit RabbitMQ [site](https://www.rabbitmq.com/upgrade.html).

---

With the version of Epiphany 0.9 it's possible to upgrade RabbitMQ to v3.8.9. It requires Erlang system packages upgrade
that is done automatically to v23.1.4. Upgrade is performed in offline mode after stopping all RabbitMQ nodes.
[Rolling upgrade](https://www.rabbitmq.com/upgrade.html#rolling-upgrades) is not supported by Epiphany, and it is
advised not to use this approach when Erlang needs to be upgraded.

## Kubernetes upgrade

### Prerequisites

Before K8s version upgrade make sure that deprecated API versions are not used:

- [v1.19](https://v1-19.docs.kubernetes.io/docs/setup/release/notes/#deprecation)
- [v1.20](https://v1-20.docs.kubernetes.io/docs/setup/release/notes/#deprecation)
- [v1.21](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.21.md)
- [v1.22](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.22.md)

## PostgreSQL upgrade

---
**NOTE**

Before upgrade procedure, make sure you have a data backup.

---

### Versions

Epiphany upgrades PostgreSQL 10 to 13 with the following extensions
(for versions, see [COMPONENTS.md](../COMPONENTS.md#epiphany-cluster-components)):

- PgAudit
- PgBouncer
- PgPool
- repmgr

### Prerequisites

The prerequisites below are checked by the preflight script before upgrading PostgreSQL. Nevertheless, it's good to
check these manually before doing any upgrade:

- Diskspace: When Epiphany upgrades PostgreSQL 10 to 13 it will make a copy of the data directory on each node to ensure
  easy recovery in the case of a failed data migration. It is up to the user to make sure there is enough space
  available. The used rule is:

  total storage used on the data volume + total size of the data directory < 95% of total size of the data volume

  We use 95% of used storage after data directory copy as some space is needed during the upgrade.

- Cluster health: Before starting the upgrade the state of the PostgreSQL cluster needs to be healthy. This means that
  executing:

  ```shell
  repmgr cluster show
  repmgr node check
  test $(repmgr node check | grep -c CRITICAL) -eq 0
  ```

  Should not fail and return 0 as exit code.

### Upgrade

Upgrade procedure is based on [PostgreSQL documentation](https://www.postgresql.org/docs/13/pgupgrade.html) and requires
downtime as there is a need to stop old service(s) and start new one(s).

There is a possibility to provide a custom configuration for upgrade with `epicli upgrade -f`, and there are a few
limitations related to specifying parameters for upgrade:

- If there were non-default values provided for installation (`epicli apply`), they have to be used again not to be
  overwritten by defaults.

- `wal_keep_segments` parameter for replication is replaced
  by [wal_keep_size](https://www.postgresql.org/docs/13/runtime-config-replication.html#GUC-WAL-KEEP-SIZE) with the
  default value of 500 MB. Previous parameter is not supported.

- `archive_command` parameter for replication is set to `/bin/true` by default. It was planned to disable archiving, but
  changes to `archive_mode` require a full PostgreSQL server restart, while `archive_command` changes can be applied via
  a normal configuration reload. See [documentation](https://repmgr.org/docs/repmgr.html#CONFIGURATION-POSTGRESQL).

- There is no possibility to disable an extension after installation, so `specification.extensions.*.enabled: false`
  value will be ignored during upgrade if it was set to `true` during installation.

### Manual actions

Epiphany runs `pg_upgrade` (on primary node only) from a dedicated location (`pg_upgrade_working_dir`). For Ubuntu, this
is `/var/lib/postgresql/upgrade/$PG_VERSION` and for RHEL `/var/lib/pgsql/upgrade/$PG_VERSION`. Epiphany saves
there output from `pg_upgrade` as logs which should be checked after the upgrade.

#### Post-upgrade processing

As the "Post-upgrade processing" step in [PostgreSQL documentation](https://www.postgresql.org/docs/13/pgupgrade.html)
states if any post-upgrade processing is required, `pg_upgrade` will issue warnings as it completes. It will also
generate SQL script files that must be run by the administrator. There is no clear description in which cases they are
created, so please check logs in `pg_upgrade_working_dir` after the upgrade to see if additional steps are required.

#### Statistics

Because optimizer statistics are not transferred by `pg_upgrade`, you may need to run a command to regenerate that
information after the upgrade. For this purpose, consider running `analyze_new_cluster.sh` script (created
in `pg_upgrade_working_dir`)
as `postgres` user.

#### Delete old cluster

For safety Epiphany does not remove old PostgreSQL data. This is a user responsibility to identify if data is ready to
be removed and take care about that. Once you are satisfied with the upgrade, you can delete the old cluster's data
directories by running `delete_old_cluster.sh` script (created in `pg_upgrade_working_dir` on primary node) **on all
nodes**. The script is not created if you have user-defined tablespaces inside the old data directory. You can also
delete the old installation directories (e.g., `bin`, `share`). You may delete `pg_upgrade_working_dir`
on primary node once the upgrade is completely over.

## Terraform upgrade from Epiphany 1.x to 2.x

From Epiphany 1.x to 2.x the Terraform stack received the following major updates:
- Terraform 0.12.6 to 1.1.3
- Azurerm provider 1.38.0 to 2.91.0
- AWS provider 2.26 to 3.71.0
- Removal of auto-scaling-groups in favor of plain EC2 instances on AWS.

These introduce some breaking changes which will require manual steps for upgrading an existing 1.x clusters. As this is not straight forward we recommend deploying a new cluster on 2.x and migrating data instead.

If you do want to upgrade a 1.x manually it will require you to upgrade between a few different versions of Terraform. The basic steps are described below for each provider. As always ensure backup of any data required.

Final note is that you can also leave the Terraform in place and use the `--no-infra` flag to skip applying the new Terraform scripts. This however makes you unable to make any changes to your cluster layout.

### Azure

Notes:
- If you made any manual changes to your cluster infrastructure outside of Terraform this might cause issues.
- Some resources might be changed or added which are usually security-groups and security-groups-association or NIC's. This is normal behaviour and is ok, just make sure no other resources like VM's are included when reviewing the `terraform plan` output.
- Only run `terraform apply` if `terraform plan` shows your infrastructure does not match the configuration.
- Manual Terraform upgrade up to v1.0.x should be completed before running `epicli apply` command with Epiphany 2.x.
- Terraform can be installed as a binary package or by using package managers, see more: https://learn.hashicorp.com/tutorials/terraform/install-cli

#### v0.12.6 => v0.13.x

The official documentation can be found here: https://www.terraform.io/language/upgrade-guides/0-13

General steps:
- Download the latest Terraform v0.13.x: https://releases.hashicorp.com/terraform/
- Run the following sets of commands in the `build/clustername/terraform` folder and follow the steps if asked:
  ```shell
  terraform init
  terraform 0.13upgrade
  terraform plan
  terraform apply (if needed)
  ```

#### v0.13.x => v0.14.x

The official documentation can be found here: https://www.terraform.io/language/upgrade-guides/0-14

General steps:
- Download the latest Terraform v0.14.x: https://releases.hashicorp.com/terraform/
- Run the following sets of commands in the `build/clustername/terraform` folder and follow the steps if asked:
  ```shell
  terraform init
  terraform plan
  terraform apply (if needed)
  ```

#### v0.14.x => v1.0.x

Note: From v0.14.x we can upgrade straight to v1.0.x. No need to upgrade to v0.15.x first.

The official documentation can be found here: https://www.terraform.io/language/upgrade-guides/1-0

General steps:
- Download the latest Terraform v1.0.x: https://releases.hashicorp.com/terraform/
- Run the following sets of commands in the `build/clustername/terraform` folder and follow the steps if asked:
  ```shell
  terraform init
  terraform plan
  terraform apply (if needed)
  ```

#### v1.0.x => v1.1.3

In this step we also force the upgrade from Azurerm provider 1.38.0 to 2.91.0 which requires a few more steps to resolve some pending issues.
At this point, the steps assume that you are already running Epiphany 2.x image.

The official documentation can be found here: https://www.terraform.io/language/upgrade-guides/1-1

General steps:
- Run epicli to generate new Azurerm provider Terraform scripts:
  ```shell
  epicli apply -f data.yml
  ```
  After the Terraform scripts generation `terraform init ...` will result in the following error:
  `Error: Failed to query available provider packages`
- To fix the issue from previous step manually run from the epicli container in `build/clustername/terraform`:
  ```shell
  terraform init -upgrade
  ```
- Now re-run epicli again:
  ```shell
  epicli apply -f data.yml
  ```
  This might succeed but depending on the cluster configuration this might lead to several errors for each NIC:
  `Error: A resource with the ID "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/prefix-name-rg/providers/Microsoft.Network/networkInterfaces/prefix-name-component-nic-x|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/prefix-name-rg/providers/Microsoft.Network/networkSecurityGroups/prefix-name-component-nsg-x" already exists - to be managed via Terraform this resource needs to be imported into the State. Please see the resource documentation for "azurerm_network_interface_security_group_association" for more information.`
- To resolve the above error we need to import the azurerm_network_interface_security_group_association for each NIC by using the `terraform input` command for each of the above errors using the ID and the propper name from the xxx_prefix-name-component-nsga-x.tf Terraform resources like so:
  ```shell
  terraform import 'azurerm_network_interface_security_group_association.prefix-name-component-nsga-0' '/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/prefix-name-rg/providers/Microsoft.Network/networkInterfaces/prefix-name-component-nic-x|/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/prefix-name-rg/providers/Microsoft.Network/networkSecurityGroups/prefix-name-component-nsg-x'
  ```
- Once all azurerm_network_interface_security_group_association are imported sucessfully you can re-run epicli apply one more time:
  ```shell
  epicli apply -f data.yml
  ```

### AWS

The Terraform for AWS deployments between Epiphany 1.x and 2.x is not compatible and migration is not possible without destruction of the enviroment. The only options is to deploy a new cluster and migrate the data.
