# Security Groups

This document describes the Security Groups layout which is used to deploy Epiphany Platform in AWS or Azure. You will find the default configuration here, as well as examples of adding own rules or changing existing ones.

## Introduction

By default Epiphany platform is creating security groups required to handle communication by all components (like postgress/rabbitmq etc). As per defaults, Epiphany creates a subnet per component and  each subnet has its own of security group, with rules that allow communication between them. This enables the smooth communication between all components. Please check our [security document](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/SECURITY.md) too. *Be aware, that whenever you want to add a new rule, you need to copy all default rules from mentioned above url*. That this document is splited into two parts: AWS and Azure. The reason why we do that, is that there are diffrent values in AWS and AZure, when setting the security rules.

## Setting own security groups

Sometimes, there is a need to set additional security rules for application which we're deploying in epiphany kubernetes cluster. Than, we need to stick into following rules:
- Whenever we want to add new rule - for example open port "X", we should *COPY* all current roles into our deployment .yaml file, and at the end, add the rule which we want.
- Each component has his own rule-set, so we need to be very carefull where we're putting them.
- After coping, we can also modify existing default security groups.
- After adding new rules, and infra part is done (terraform), we can go into terraform build directory and check if fiiles contain our port definition.

## Security groups diagram

Check bellow security diagram, which show how security groups are related to other components. This is example of AWS architecutre, but in Azure should be almost the same.
![](../AWS/aws_cluster_setup.svg)

## Azure Security groups

List of all security groups and related services in Azure are described [here](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/azure/defaults/infrastructure/virtual-machine.yml).

Rules description:
```yaml
- name:                       "Name of the rule"
  description:                "Short rule description"
  priority:                   "Priority (NUM), which describes which rules should be taken into conediration as first "
  direction:                  "Inbound || Outbound" - which direction are you allowing rule"
  access:                     "Allow|Deny - whenever we want to grant access or block"
  protocol:                   "TCP || UDP" - which protocol should be used for connections"
  source_port_range:          "Source port ranges"
  destination_port_range:     "Destination port/s range"
  source_address_prefix:      "Source network address"
  destination_address_prefix: "Destination network address"
```

Lets look into example on which, we are setting new rule name "nrpe-agent-port", with priority 250, which is allowing accesses from local network "10.1.4.0/24" into all hosts in our network on port 5666.

The rule:
```yaml
     - name: nrpe-agent-port
       description: Allow access all hosts on port 5666 where nagios agent is running.
       priority: 250
       direction: Inbound
       access: Allow
       protocol: Tcp
       source_port_range: "*"
       destination_port_range: "5666"
       source_address_prefix: "10.1.4.0/24"
       destination_address_prefix: "0.0.0.0/0"
```

## Azure Security groups full yaml file

To deploy previously mentioned rule, we need to setup a complete YAML configuraiton file. Bellow example shows how this file should looks like. In this configuration we set simple setup of epiphany with 2nodes and 1 master vm in Azure.
```yaml
kind: epiphany-cluster
name: default
provider: azure
title: Epiphany cluster Config
specification:
  name: azure
  prefix: azure
  admin_user:
    name: operations
    key_path:  /workspaces/epiphany/core/src/epicli/clusters/keys/abb_rsa
  cloud:
    region: West Europe
    subscription_name: PUT_SUBSCRIPTION_NAME_HERE
    use_public_ips: true
    use_service_principal: true
    network:
      use_network_security_groups: true
  components:
    kafka:
      count: 0
    kubernetes_master:
      count: 1
      machine: kubernetes-master-machine
      configuration: default
    kubernetes_node:
      count: 2
    load_balancer:
      count: 0
    logging:
      count: 0
    monitoring:
      count: 0
    postgresql:
      count: 0
    rabbitmq:
      count: 0
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
provider: azure
name: kubernetes-master-machine
specification:
  size: Standard_DS3_v2
  security:
    rules:
      - name: ssh
        description: Allow SSH
        priority: 100
        direction: Inbound
        access: Allow
        protocol: Tcp
        source_port_range: "*"
        destination_port_range: "22"
        source_address_prefix: "0.0.0.0/0"
        destination_address_prefix: "0.0.0.0/0"
      - name: out
        description: Allow out
        priority: 101
        direction: Outbound
        access: Allow
        protocol: "*"
        source_port_range: "*"
        destination_port_range: "0"
        source_address_prefix: "0.0.0.0/0"
        destination_address_prefix: "0.0.0.0/0"
      - name: node_exporter
        description: Allow node_exporter traffic
        priority: 200
        direction: Inbound
        access: Allow
        protocol: Tcp
        source_port_range: "*"
        destination_port_range: "9100"
        source_address_prefix: "10.1.0.0/20"
        destination_address_prefix: "0.0.0.0/0"
      - name: subnet-traffic
        description: Allow subnet traffic
        priority: 201
        direction: Inbound
        access: Allow
        protocol: "*"
        source_port_range: "*"
        destination_from_port: 0
        destination_to_port: 65536
        destination_port_range: "0"
        source_address_prefix: "10.1.1.0/24"
        destination_address_prefix: "0.0.0.0/0"
      - name: monitoring-traffic
        description: Allow monitoring subnet traffic
        priority: 203
        direction: Inbound
        access: Allow
        protocol: "*"
        source_port_range: "*"
        destination_from_port: 0
        destination_to_port: 65536
        destination_port_range: "0"
        source_address_prefix: "10.1.4.0/24"
        destination_address_prefix: "0.0.0.0/0"
      - name: node-subnet-traffic
        description: Allow node subnet traffic
        priority: 204
        direction: Inbound
        access: Allow
        protocol: "*"
        source_port_range: "*"
        destination_from_port: 0
        destination_to_port: 65536
        destination_port_range: "0"
        source_address_prefix: "10.1.2.0/24"
        destination_address_prefix: "0.0.0.0/0"
      - name: package_repository
        description: Allow package repository traffic
        priority: 205
        direction: Inbound
        access: Allow
        protocol: Tcp
        source_port_range: "*"
        destination_port_range: "80"
        source_address_prefix: "10.1.0.0/20"
        destination_address_prefix: "0.0.0.0/0"
      - name: image_repository
        description: Allow image repository traffic
        priority: 206
        direction: Inbound
        access: Allow
        protocol: Tcp
        source_port_range: "*"
        destination_port_range: "5000"
        source_address_prefix: "10.1.0.0/20"
        destination_address_prefix: "0.0.0.0/0"
      # Add NRPE AGENT RULE
      - name: nrpe-agent-port
        description: Allow access all hosts on port 5666 where nagios agent is running.
        priority: 250
        direction: Inbound
        access: Allow
        protocol: Tcp
        source_port_range: "*"
        destination_port_range: "5666"
        source_address_prefix: "10.1.4.0/24"
        estination_address_prefix: "0.0.0.0/0"
```

## AWS Security groups

List of all security groups and related services in AWS are described [here](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/aws/defaults/infrastructure/virtual-machine.yml).

Rules description:
```yaml
- name:                       "Name of the rule"
  description:                "Short rule description"
  direction:                  "Inbound || Egress" - which direction are you allowing rule"
  protocol:                   "TCP || UDP" - which protocol should be used for connections"
  destination_port_range:     "Destination port/s range"
  source_address_prefix:      "Source network address"
  destination_address_prefix: "Destination network address"
```

Lets look into example on which, we are setting new rule name "nrpe-agent-port", which is allowing accesses from local network "10.1.4.0/24" into all hosts in our network on port 5666.

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

## AWS Setting groups full yaml file

Please check bellow example, how to setup basic epiphany cluster in AWS with 1 master, 2 nodes, mandatory repository machine, and open accesses to all hosts on port 5666 from monitoring network.

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
```
