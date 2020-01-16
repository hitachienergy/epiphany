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

## Note about legacy Epiphany

Epicli 0.4.0 adds support for Azure deployments so using legacy Epiphany is no longer needed. We advice new projects to start straight with Epicli and older projects which still use legacy Epiphany to move over to Epicli 0.4.0. A tool to migrate legacy data files to the new format is in the works and will be released shortly.

The Epicli 0.5.0 release later this year will drop the inclusion of the legacy path entirely.

## Note about documentation

- The documentation is a moving target. Always check the latest documentation on the develop branch. There is a big chance that whatever you are looking for is already added/updated or improved there.
- We are currently in the process of documenting all features of Epicli and phasing out legacy Epiphany documentation. When documentation is specific for `Epicli` or `Legacy` it will be marked under a header with the these names. If its not under any of these headers then it applies to both.

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

### Legacy

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
