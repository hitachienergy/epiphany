# Security Groups layout information

This document describes the Security Groups layout which is used to deploy Epiphany Platform in AWS or Azure. You will find the default configuration here, as well as examples of adding own rules. 

## Contents

- [Security groups created by default](#security-groups-created-by-default)
- [Setting own security groups](#setting-own-security-groups)
- [Example](#example)

### Security groups created by default

By default Epiphany is creating security groups required to handle communication by all components (like postgress/rabbitmq etc). This enables the smooth communication between all of them. List of all security groups and related services are described [here](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/aws/defaults/infrastructure/).

Rules description:
```
- name:                       "Name of the rule"
  description:                "Short rule description"
  priority:                   "Rule priority; which rules should be considered as first-used basing on lowest number"
  direction:                  "Inbound || Egress" - which direction are you allowing rule"
  access:                     "Allow || Deny" - whenever rule should allow connections or block"
  protocol:                   "TCP || UDP" - which protocol should be used for connections"
  source_port_range:          "Source port ranges"
  destination_port_range:     "Destination prot ranges"
  source_address_prefix:      "Source network address"
  destination_address_prefix: "Destination network address"
```

Lets look into example of Prometheus machine setup, and rules required to allow connection from other network into Prometheus host.
The rule:
```
- name: prometheus
  description: Allow connection to Prometheus
  priority: 302
  direction: Inbound
  access: Allow
  protocol: Tcp
  source_port_range: "*"
  destination_port_range: "9090"
  source_address_prefix: "10.1.0.0/20"
  destination_address_prefix: "0.0.0.0/0"
```
As we see, on this example, we are seting new rule name "prometheus", with priority 302, which is allowing accesses from local network "10.1.0.0/20" into Prometheus application host on port 9090. Note, that here we set dest "0.0.0.0/0" address and source 10.1.0.0/20, as those are the default configurations in Epiphany used if noone specify others. This might be adjusted in case you're using difrent addresses. 


### Setting own security groups
Sometimes, there is a need to set additional security rules for some application which we're deploying in epiphany kubernetes cluster. Than, we need to stick into following rules:
- Whenever we want to add new rule - for example open port "222", we should *COPY* all current roles into our deployment .yaml file, and at the end, add the rule which we want.
- Each component has his own rule-set, so we need to be very carefull where we're putting them.
- After adding new rules, and infra part is done (terraform), we can go into terraform build directory and check if fiiles contain our port definition.

###### Example
Please check bellow example, how to setup basic epiphany cluster in AWS with 1 master, 2 nodes, and open accesses to all hosts on port 10051 from monitoring network.

```
kind: epiphany-cluster
name: default
provider: aws
specification:
  admin_user:
    name: ubuntu
    key_path: /PATH/TO/SSH_KEY
  cloud:
    region: eu-central-1
    credentials:
      key: YOUR_AWS_KEY
      secret: YOUR_AWS_SECRET
    use_public_ips: true  
  components:
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
      machine: logging-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.3.0/24
    monitoring:
      count: 0
      machine: monitoring-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.4.0/24
    kafka:
      count: 0
      machine: kafka-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.5.0/24
    postgresql:
      count: 0
      machine: postgresql-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.6.0/24
    load_balancer:
      count: 0
      machine: load-balancer-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.7.0/24
    rabbitmq:
      count: 0
      machine: rabbitmq-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.8.0/24
    ignite:
      count: 0
      machine: ignite-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.9.0/24
    opendistro_for_elasticsearch:
      count: 0
      machine: logging-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.10.0/24
    single_machine:
      count: 0
      machine: single-machine
      configuration: default
      subnets:
      - availability_zone: eu-central-1a
        address_pool: 10.1.1.0/24
      - availability_zone: eu-central-1b
        address_pool: 10.1.2.0/24
  name: awsu
  prefix: 'test'
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
       priority: 101
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "22"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     - name: repository
       description: Allow repository traffic
       priority: 302
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "80"
       source_address_prefix: "10.1.0.0/20"
       destination_address_prefix: "0.0.0.0/0"
     - name: node_exporter
       description: Allow node_exporter traffic
       priority: 302
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "9100"
       source_address_prefix: "10.1.0.0/20"
       destination_address_prefix: "0.0.0.0/0"
     - name: subnet-traffic
       description: Allow subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.1.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: monitoring-traffic
       description: Allow monitoring subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: node-subnet-traffic
       description: Allow node subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.2.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: node2-subnet-traffic
       description: Allow node subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: out
       description: Allow out
       priority: 101
       direction: Egress
       access: Allow
       protocol: "all"
       source_port_range: "*"
       destination_port_range: "0"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     # NEW RULE
     - name: allow-port-10051
       description: Allow monitoring subnet, to access all hosts on port 10051.
       priority: 101
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "10051"
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
       priority: 101
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "22"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     - name: node_exporter
       description: Allow node_exporter traffic
       priority: 302
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "9100"
       source_address_prefix: "10.1.0.0/20"
       destination_address_prefix: "0.0.0.0/0"
     - name: subnet-traffic
       description: Allow master subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.1.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: monitoring-traffic
       description: Allow monitoring subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: node-subnet-traffic
       description: Allow node subnet traffic
       priority: 102
       direction: Inbound
       access: Allow
       protocol: ALL
       source_port_range: "*"
       destination_from_port: 0
       destination_to_port: 65536
       destination_port_range: "0"
       source_address_prefix: "10.1.2.0/24"
       destination_address_prefix: "0.0.0.0/0"
     - name: out
       description: Allow out
       priority: 101
       direction: Egress
       access: Allow
       protocol: "all"
       source_port_range: "*"
       destination_port_range: "0"
       source_address_prefix: "0.0.0.0/0"
       destination_address_prefix: "0.0.0.0/0"
     # NEW RULE
     - name: allow-port-10051
       description: Allow monitoring subnet, to access all hosts on port 10051.
       priority: 101
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "10051"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
```