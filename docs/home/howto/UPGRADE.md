# Upgrade

## Introduction

From Epicli 0.4.2 and up the CLI has the ability to perform upgrades on certain components on a cluster. The components
it currently can upgrade and will add are:

---
**NOTE**

There is an assertion to check whether K8s version is supported before running upgrade.

---

- Kubernetes (master and nodes). Supported versions: v1.18.6 (Epiphany 0.7.1+), v1.20.12 (Epiphany 1.3.0+)
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
  - RedHat 7.6
  - CentOS 7.6
  - Ubuntu 18.04
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
  - RedHat 7.6
  - CentOS 7.6
  - Ubuntu 18.04
3. The airgapped cluster machines/vm`s should be accessible through SSH with a set of SSH keys you provided and
   configured on each machine yourself.
4. A requirements machine that:
  - Runs the same distribution as the airgapped cluster machines/vm`s (RedHat 7, CentOS 7, Ubuntu 18.04)
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
    epicli prepare --os OS
    ```

   Where OS should be `centos-7`, `redhat-7`, `ubuntu-18.04`. This will create a directory called `prepare_scripts` with
   the needed files inside.

2. The scripts in the `prepare_scripts` will be used to download all requirements. To do that, copy
   the `prepare_scripts` folder over to the requirements machine and run the following command:

    ```shell
    download-requirements.sh /requirementsoutput/
    ```

   This will start downloading all requirements and put them in the `/requirementsoutput/` folder. Once run successfully
   the `/requirementsoutput/` needs to be copied to the provisioning machine to be used later on.

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
    ignite:
      count: 0
    opendistro_for_elasticsearch:
      count: 0
  name: clustername
  prefix: 'prefix'
title: Epiphany cluster Config
---
kind: configuration/feature-mapping
title: Feature mapping to roles
provider: azure
name: default
specification:
  roles_mapping:
    kubernetes_master:
      - kubernetes-master
      - helm
      - applications
      - node-exporter
      - filebeat
      - firewall
      - vault
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

### ZooKeeper upgrade

Redundant ZooKeeper configuration is also recommended, since service restart is required during upgrade - it can cause
ZooKeeper unavailability. Having **at least two ZooKeeper services** in *ZooKeepers ensemble* you can upgrade one and
then start with the rest **one by one**.

More detailed information about ZooKeeper you can find
in  [ZooKeeper documentation](https://cwiki.apache.org/confluence/display/ZOOKEEPER).

## Open Distro for Elasticsearch upgrade

---
**NOTE**

Before upgrade procedure make sure you have a data backup!

---

Since Epiphany v1.0.0 we provide upgrade elasticsearch-oss package to v7.10.2 and opendistro-\* plugins package to
v1.13.\*. Upgrade will be performed automatically when the upgrade procedure detects your `logging`
, `opendistro_for_elasticsearch` or `kibana` hosts.

Upgrade of Elasticsearch uses API calls (GET, PUT, POST) which requires an admin TLS certificate. By default, Epiphany
generates self-signed certificates for this purpose but if you use your own, you have to provide the admin certificate's
location. To do that, edit the following settings changing `cert_path` and `key_path`.

```yaml
logging:
  upgrade_config:
    custom_admin_certificate:
      cert_path: /etc/elasticsearch/custom-admin.pem
      key_path: /etc/elasticsearch/custom-admin-key.pem

opendistro_for_elasticsearch:
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

### Upgrade

---
**NOTE**

If the K8s cluster that is going to be upgraded has the Istio control plane application deployed, issues can occur. The
default [profiles](https://istio.io/latest/docs/setup/additional-setup/config-profiles/) we currently support for
installing Istio only deploy a single replica for the control services with a `PodDisruptionBudgets` value of 0. This
will result in the following error while draining pods during an upgrade:

```shell
Cannot evict pod as it would violate the pods disruption budget.
```

As we currently don't support any kind of advanced configuration of the Istio control plane components outside the
default profiles, we need to scale up all components manually before the upgrade. This can be done with the following
command:

```shell
kubectl scale deploy -n istio-system --replicas=2 --all 
```

After the upgrade, the deployments can be scaled down to the original capacity:

```shell
kubectl scale deploy -n istio-system --replicas=1 --all 
```

**Note: The ```istio-system``` namespace value is the default value and should be set to whatever is being used in the
Istio application configuration.**

---

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
is `/var/lib/postgresql/upgrade/$PG_VERSION` and for RHEL/CentOS `/var/lib/pgsql/upgrade/$PG_VERSION`. Epiphany saves
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
