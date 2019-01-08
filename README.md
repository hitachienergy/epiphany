# Documentation

## Overview

Epiphany at it's core is full automation of Kubernetes and Docker plus additional builtin services such as Kafka for high speed messaging/events, Prometheus for monitoring and Graphana for dashboards, Elasticsearch and Kibana for centralized logging. Other optional services are being evaluated now.

Epiphany can run on as few as one node (laptop, desktop, server) but the real value comes from running 3 or more nodes for scale and HA. Nodes can be added or removed at will depending on data in the manifest. Everything is data driven so simply changing the manifest data and running the automation will modify the environment.

We currently use Terraform and Ansible for our automation orchestration. All automation is idempotent so you can run it as many times as you wish and it will maintain the same state unless you change the data. If someone makes a "snow flake" change to the environment (you should never do this) then simply running the automation again will put the environment back to the desired state.

## Table of Contents

<!-- TOC -->

- [Epiphany project](docs/home/README.md)

- [How-to guides](docs/home/HOWTO.md)

- [Troubleshooting](docs/home/TROUBLESHOOTING.md)

- Architecture
  - [Logical View](docs/architecture/logical-view.md)
  
  - [Process View](docs/architecture/process-view.md)
  
  - [Physical View](docs/architecture/physical-view.md)

- [How-to contribute](docs/home/CONTRIBUTING.md)

- [Workflow to follow](docs/home/GITWORKFLOW.md)

- [Governance model](docs/home/GOVERNANCE.md)

- [Changelog](CHANGELOG.md)

- [Project layout](docs/project_layout.md)

<!-- TOC -->

---
