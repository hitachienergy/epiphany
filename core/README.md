# Epiphany

## Overview

Epiphany at it's core is full automation of Kubernetes and Docker plus additional builtin services such as Kafka for high speed messaging/events, Prometheus for monitoring and Graphana for dashboards, Elasticsearch and Kibana for centralized logging. Other optional services are being evaluated now.

Epiphany can run on as few as one node (laptop, desktop, server) but the real value comes from running 3 or more nodes for scale and HA. Nodes can be added or removed at will depending on data in the manifest. Everything is data driven so simply changing the manifest data and running the automation will modify the environment.

We currently use Terraform and Ansible for our automation orchestration. All automation is idempotent so you can run it as many times as you wish and it will maintain the same state unless you change the data. If someone makes a "snow flake" change to the environment (you should never do this) then simply running the automation again will put the environment back to the desired state.

For the full story, go to [Epiphany documentation](https://github.com/epiphany-platform/docs/README.md).