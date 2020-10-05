# Security Groups layout information

This document describes the Security Groups layout which is used to deploy Epiphany Platform in AWS or Azure. You will find the default configuration here, as well as examples of adding own rules or changing existing ones.

## Table of Contents

- [Security groups created by default](#security-groups-created-by-default-in-aws)
- [Setting own security groups](#setting-own-security-groups-in-aws)
- [Example](#example-in-aws)

## Security groups created by default in AWS

By default Epiphany is creating security groups required to handle communication by all components (like postgress/rabbitmq etc). This enables the smooth communication between all of them. List of all security groups and related services are described [here](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/aws/defaults/infrastructure/).
Please note, that whenever you want to add a new rule, you need to copy all default rules from mentioned above url.

Rules description:

```yaml
- name:                       "Name of the rule"
  description:                "Short rule description"
  direction:                  "Inbound || Egress" - which direction are you allowing rule"
  protocol:                   "TCP || UDP" - which protocol should be used for connections"
  destination_port_range:     "Destination prot"
  source_address_prefix:      "Source network address"
  destination_address_prefix: "Destination network address"
```

Lets look into example of Prometheus machine setup, and rules required to allow connection from other network into Prometheus host.
The rule:

```yaml
     - name: nrpe-agent-port
       description: Allow access all hosts on port 5666 where nagios agent is running.
       direction: Inbound
       protocol: Tcp
       destination_port_range: "5666"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
```

In the above example, we are setting new rule name "prometheus", with priority 302, which is allowing accesses from local network "10.1.0.0/20" into Prometheus application host on port 9090. Note, that here we set dest "0.0.0.0/0" address and source 10.1.0.0/20, as those are the default configurations in Epiphany used if noone specify others. This might be adjusted in case you're using different addresses. 


## Setting own security groups in AWS

Sometimes, there is a need to set additional security rules for some application which we're deploying in epiphany kubernetes cluster. Than, we need to stick into following rules:
- Whenever we want to add new rule - for example open port "222", we should *COPY* all current roles into our deployment .yaml file, and at the end, add the rule which we want.

- Each component has his own rule-set, so we need to be very carefull where we're putting them.
- After adding new rules, and infra part is done (terraform), we can go into terraform build directory and check if fiiles contain our port definition.

**Example in AWS:**

Please check bellow example, how to setup basic epiphany cluster in AWS with 1 master, 2 nodes, mandatory repository machine, and open accesses to all hosts on port 10051 from monitoring network.

```yaml
kind: epiphany-cluster
name: default
provider: aws
specification:
  admin_user:
    name: ubuntu
    key_path: /path/to/your/ssh_key
  cloud:
    region: eu-central-1
    credentials:
      key: YOUR_AWS_KEY
      secret: YOUR_AWS_SECRET
    use_public_ips: true
  components:
    repository:
      count: 1
      machine: repository-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.11.0/24
    kubernetes_master:
      count: 1
      machine: kubernetes-master-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.1.0/24
      - availability_zone: eu-central-1b
        address_pool: 10.1.2.0/24
    kubernetes_node:
      count: 2
      machine: kubernetes-node-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.1.0/24
      - availability_zone: eu-central-1b
        address_pool: 10.1.2.0/24
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 0
    postgresql:
      count: 0
    load_balancer:
      count: 0
    rabbitmq:
      count: 0
    ignite:
      count: 0
    opendistro_for_elasticsearch:
      count: 0
    single_machine:
      count: 0
  name: testing
  prefix: 'aws-machine'
title: Epiphany cluster Config
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
provider: aws
name: kubernetes-master-machine
specification:
  size: t3.medium
  authorized_to_efs: true
  mount_efs: true
  security:
    rules:
     - name: ssh
       description: Allow ssh traffic
       direction: Inbound
       protocol: Tcp
       destination_port_range: "22"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     - name: node_exporter
       description: Allow node_exporter traffic
       direction: Inbound
       protocol: Tcp
       destination_port_range: "9100"
       source_address_prefix: "10.1.0.0/20"
       destination_address_prefix: "0.0.0.0/0"
     - name: subnet-traffic
       description: Allow master subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.1.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: monitoring-traffic
       description: Allow monitoring subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: node-subnet-traffic
       description: Allow node subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.2.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: out
       description: Allow out
       direction: Egress
       protocol: "all"
       destination_port_range: "0"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     # New Rule
     - name: nrpe-agent-port
       description: Allow access all hosts on port 5666 where nagios agent is running.
       direction: Inbound
       protocol: Tcp
       destination_port_range: "5666"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
provider: aws
name: kubernetes-node-machine
specification:
  size: t3.medium
  authorized_to_efs: true
  mount_efs: true
  security:
    rules:
     - name: ssh
       description: Allow ssh traffic
       direction: Inbound
       protocol: Tcp
       destination_port_range: "22"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     - name: node_exporter
       description: Allow node_exporter traffic
       direction: Inbound
       protocol: Tcp
       destination_port_range: "9100"
       source_address_prefix: "10.1.0.0/20"
       destination_address_prefix: "0.0.0.0/0"
     - name: subnet-traffic
       description: Allow master subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.1.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: monitoring-traffic
       description: Allow monitoring subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: node-subnet-traffic
       description: Allow node subnet traffic
       direction: Inbound
       protocol: ALL
       destination_port_range: "0"
       source_address_prefix: "10.1.2.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: out
       description: Allow out
       direction: Egress
       protocol: "all"
       destination_port_range: "0"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     # New Rule
     - name: nrpe-agent-port
       description: Allow access all hosts on port 5666 where nagios agent is running.
       direction: Inbound
       protocol: Tcp
       destination_port_range: "5666"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
```