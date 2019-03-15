# Documentation

## Overview

Epiphany at its core is a full automation of Kubernetes and Docker plus additional builtin services such as Kafka for high speed messaging/events, Prometheus for monitoring and Graphana for dashboards, Elasticsearch and Kibana for centralized logging. Other optional services are being evaluated now.

Epiphany can run on as few as one node (laptop, desktop, server) but the real value comes from running 3 or more nodes for scale and HA. Nodes can be added or removed at will depending on data in the manifest. Everything is data driven so simply changing the manifest data and running the automation will modify the environment.

We currently use Terraform and Ansible for our automation orchestration. All automation is idempotent so you can run it as many times as you wish and it will maintain the same state unless you change the data. If someone makes a "snow flake" change to the environment (you should never do this) then simply running the automation again will put the environment back to the desired state.

## Quickstart

Fork the `epiphany` repository and modify the yaml's under `core/data/` directory. For example in `data/azure/infrastructure/epiphany-playground/basic-data.yaml` file you will need to modify a few values (like you Azure subscription name, directory path for ssh keys). Once you are done done with `basic-data.yaml` you can execute Epiphany with the command:

```shell
./epiphany -a -b -i -f infrastructure/epiphany-playground -t infrastructure/epiphany-template
```

This setup works on a simplified file that is fine to start with, if you need more control over the infrastructure created you should look at `data/azure/infrastructure/epiphany-bld-apps/data.yaml`.
Execution of this full profile would look like:

```shell
./epiphany -a -b -i -f infrastructure/epiphany-bld-apps
```

Find more information using table of contents below - especially the [How-to guides](docs/home/HOWTO.md).

## Documentation

<!-- TOC -->

- Platform
  - [Resources](docs/home/RESOURCES.md)
  - [How-to guides](docs/home/HOWTO.md)
  - [Troubleshooting](docs/home/TROUBLESHOOTING.md)
- Architecture
  - [Logical View](docs/architecture/logical-view.md)
  - [Process View](docs/architecture/process-view.md)
  - [Physical View](docs/architecture/physical-view.md)
- Project
  - [How-to contribute](docs/home/CONTRIBUTING.md)
  - [Workflow to follow](docs/home/GITWORKFLOW.md)
  - [Governance model](docs/home/GOVERNANCE.md)
  - [Notices](docs/home/NOTICES.md)
  - [Changelog](CHANGELOG.md)

<!-- TOC -->
