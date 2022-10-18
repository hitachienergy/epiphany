# Epiphany Platform
[![GitHub release](https://img.shields.io/github/v/release/epiphany-platform/epiphany.svg)](https://github.com/epiphany-platform/epiphany/releases)
[![Github license](https://img.shields.io/github/license/epiphany-platform/epiphany)](https://github.com/epiphany-platform/epiphany/releases)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=bugs)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=epiphany-platform_epiphany&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=epiphany-platform_epiphany)

**⚠️ Epiphany is no longer under active development, no new features or upgrades will be done by the [core team](https://github.com/orgs/epiphany-platform/teams/epiphany-team). The [core team](https://github.com/orgs/epiphany-platform/teams/epiphany-team) however, will address critical defects and security issues during the [LTS versions](docs/home/LIFECYCLE.md) lifecycle. Finally the  [core team](https://github.com/orgs/epiphany-platform/teams/epiphany-team) will continue the [governance](docs/home/GOVERNANCE.md) of external contributions and publish intermittent releases for [LTS versions](docs/home/LIFECYCLE.md) during their lifecycle.⚠️**

## Overview

Epiphany at its core is a full automation of Kubernetes and Docker plus additional builtin services/components like:

- Kafka or RabbitMQ for high speed messaging/events
- Prometheus and Alertmanager for monitoring with Graphana for visualization
- OpenSearch for centralized logging
- HAProxy for loadbalancing
- Postgres and OpenSearch for data storage
- KeyCloak for authentication
- Helm as package manager for Kubernetes

The following target platforms are available: AWS, Azure and on-prem installation.

Epiphany can run on as few as one node (laptop, desktop, server) but the real value comes from running 3 or more nodes for scale and HA. Everything is data driven so simply changing the manifest data and running the automation will modify the environment.
Kubernetes hosts (masters, nodes) and component VMs can be added depending on data in the initial manifest. More information [here](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/howto/CLUSTER.md#how-to-scale-or-cluster-components).

Please note that currently Epiphany supports only creating new masters and nodes and adding them to the Kubernetes cluster. It doesn't support downscale. To remove them from Kubernetes cluster you have to do it manually.

We currently use Terraform and Ansible for our automation orchestration. All automation is idempotent so you can run it as many times as you wish and it will maintain the same state unless you change the data. If someone makes a "snow flake" change to the environment (you should never do this) then simply running the automation again will put the environment back to the desired state.

## Note about documentation

- The documentation is a moving target. Always check the latest documentation on the develop branch. There is a big chance that whatever you are looking for is already added/updated or improved there.

## Deprecation Note

At the link presented below you can find the information about deprecated components with plan of removal from Epiphany.  
[Deprecation Note](docs/home/DEPRECATION-NOTE.md)

## Quickstart

### Epicli

Use the following command to see a full run-down of all [epicli](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/howto/PREREQUISITES.md#run-epicli-from-docker-image) commands and flags:

```shell
epicli --help
```

Generate a new minimum cluster definition:

```shell
epicli init -p aws -n demo
```

This minimum file definition is fine to start with, however if you need more control over the infrastructure created you can also create a full definition:

```shell
epicli init -p aws -n demo --full
```
and this will create a cluster definition with all available in Epiphany components.

You will need to modify a few values (like your AWS secrets, directory path for SSH keys). Once you are done with `demo.yml` you can start cluster deployment by executing:

```shell
epicli apply -f demo.yml
```
You will be asked for a password that will be used for encryption of some of build artifacts. More information [here](docs/home/howto/SECURITY.md#how-to-run-epicli-with-password).

Since version 0.7 epicli has an option to backup/recovery some of its components. More information [here](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/howto/BACKUP.md).
```shell
epicli backup -f <file.yml> -b <build_folder>
epicli recovery -f <file.yml> -b <build_folder>
```

To delete all deployed components following command should be used

```shell
epicli delete -b <build_folder>
```

Find more information using table of contents below - especially the [How-to guides](docs/home/HOWTO.md).

## Documentation

<!-- TOC -->

- Platform
  - [Resources](docs/home/RESOURCES.md)
  - [How-to guides](docs/home/HOWTO.md)
  - [Components](docs/home/COMPONENTS.md)
  - [Security](docs/home/SECURITY.md)
  - [Troubleshooting](docs/home/TROUBLESHOOTING.md)
  - [Changelog](CHANGELOG.md)
  - [Release policy and lifecycle](docs/home/LIFECYCLE.md)
- Architecture
  - [Logical View](docs/architecture/logical-view.md)
  - [Process View](docs/architecture/process-view.md)
  - [Physical View](docs/architecture/physical-view.md)
- Contributing
  - [Governance model](docs/home/GOVERNANCE.md)
  - [Development environment](docs/home/DEVELOPMENT.md)
  - [GIT Workflow](docs/home/GITWORKFLOW.md)

<!-- TOC -->
