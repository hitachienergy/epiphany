# ⚠️UNSUPPORTED AS OF 01 Apr 2021⚠️
For up-to-date Epiphany version lifecycle information check [here.](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/LIFECYCLE.md)

# Documentation

## Overview

Epiphany at its core is a full automation of Kubernetes and Docker plus additional builtin services/components like:

- Kafka or RabbitMQ for high speed messaging/events
- Prometheus and Alertmanager for monitoring with Graphana for visualization
- Elasticsearch and Kibana for centralized logging
- HAProxy for loadbalancing
- Postgress for storage
- KeyCloak for authentication

Epiphany can run on as few as one node (laptop, desktop, server) but the real value comes from running 3 or more nodes for scale and HA. Nodes can be added or removed at will depending on data in the manifest. Everything is data driven so simply changing the manifest data and running the automation will modify the environment.

We currently use Terraform and Ansible for our automation orchestration. All automation is idempotent so you can run it as many times as you wish and it will maintain the same state unless you change the data. If someone makes a "snow flake" change to the environment (you should never do this) then simply running the automation again will put the environment back to the desired state.

## Note about documentation

- The documentation is a moving target. Always check the latest documentation on the develop branch. There is a big chance that whatever you are looking for is already added/updated or improved there.

## Quickstart

### Epicli

Use the following command to see a full run-down of all commands and flags:

```shell
epicli --help
```

Generate a new minimum cluster definition:

```shell
epicli init -p aws -n demo
```

This minimum file definition is fine to start with, if you need more control over the infrastructure created you can also create a full definition:

```shell
epicli init -p aws -n demo --full
```

You will need to modify a few values (like your AWS secrets, directory path for SSH keys). Once you are done with `demo.yaml` you can start cluster deployment by executing:

```shell
epicli apply -f demo.yaml
```
You will be asked for a password that will be used for encryption of some of build artifacts. More information [here](docs/home/howto/SECURITY.md#how-to-run-epicli-with-password)

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
- Architecture
  - [Logical View](docs/architecture/logical-view.md)
  - [Process View](docs/architecture/process-view.md)
  - [Physical View](docs/architecture/physical-view.md)
- Contributing
  - [Governance model](docs/home/GOVERNANCE.md)
  - [Development environment](docs/home/DEVELOPMENT.md)
  - [GIT Workflow](docs/home/GITWORKFLOW.md)
  
<!-- TOC -->
