# ARM

From Epiphany v1.1.0 preliminary support for the ```arm64``` architecture was added. As the ```arm64``` architecture is relatively new to the datacenter at the time of writing only a subset of providers, operating system, components and applications are supported. Support will be extended in the future when there is a need for it.

## Support

Below we give the current state of ```arm64``` support across the different providers, operating systems, components and applications. Make sure to check the ***notes*** for limitations that might still be present for supported components or applications.

Besides making sure that the selected providers, operating systems, components and applications are supported with the tables below any other configuration for ```Epicli``` will work the same on ```arm64``` as they do on ```x86_64```. ```Epicli``` will return an error if any configuration is used that is not supported by the ```arm64``` architecture.

### Providers

| Providers | CentOS 7.x | RedHat 7.x | Ubuntu 18.04 |
| - | - | - | - |
| Any | :heavy_check_mark: | :x: | :x: |
| AWS | :heavy_check_mark: | :x: | :x: |
| Azure | :x: | :x: | :x: |

### Components

| Component | CentOS 7.x | RedHat 7.x | Ubuntu 18.04 |
| - | - | - | - |
| repository | :heavy_check_mark: | :x: | :x: |
| kubernetes_master | :heavy_check_mark: | :x: | :x: |
| kubernetes_node | :heavy_check_mark: | :x: | :x: |
| kafka | :heavy_check_mark: | :x: | :x: |
| rabbitmq | :heavy_check_mark: | :x: | :x: |
| logging | :heavy_check_mark: | :x: | :x: |
| monitoring | :heavy_check_mark: | :x: | :x: |
| load_balancer | :heavy_check_mark: | :x: | :x: |
| postgresql | :heavy_check_mark: | :x: | :x: |
| ignite | :heavy_check_mark: | :x: | :x: |
| opendistro_for_elasticsearch | :heavy_check_mark: | :x: | :x: |
| single_machine | :heavy_check_mark: | :x: | :x: |

***Notes***

- For the ```postgresql``` component the ```pgpool``` and ```pgbouncer``` extensions for load-balancing and replication are not jet supported on ```arm64```. These should be disabled in the ```postgressql``` and ```applications``` configurations.
- While not defined in any of the component configurations, the ```elasticsearch_curator``` role is currently not supported on ```arm64``` and should be removed from the ```feature-mapping``` configuration if defined.

### Applications

| Applications | Supported |
| - | - |
| ignite-stateless | :heavy_check_mark: |
| rabbitmq | :heavy_check_mark: |
| auth-service | :heavy_check_mark: |
| pgpool | :x: |
| pgbouncer | :x: |
| istio | :x: |

***Notes***

- Any of the applications that are not supported should be disabled in the ```applications``` configuration.

## Example configurations

### ```Any``` provider

```yaml
---
kind: epiphany-cluster
name: default
provider: any
title: Epiphany cluster Config
specification:
  prefix: arm
  name: centos
  admin_user:
    key_path: /shared/ssh/id_rsa
    name: admin
  components:
    kafka:
      count: 2
      machine: kafka-machine-arm
    kubernetes_master:
      count: 1
      machine: kubernetes-master-machine-arm
    kubernetes_node:
      count: 3
      machine: kubernetes-node-machine-arm
    load_balancer:
      count: 1
      machine: lb-machine-arm
    logging:
      count: 2
      machine: logging-machine-arm
    monitoring:
      count: 1
      machine: monitoring-machine-arm
    postgresql:
      count: 1
      machine: postgresql-machine-arm
    rabbitmq:
      count: 2
      machine: rabbitmq-machine-arm
    ignite:
      count: 2
      machine: ignite-machine-arm
    opendistro_for_elasticsearch:
      count: 1
      machine: opendistro-machine-arm
    repository:
      count: 1
      machine: repository-machine-arm
---
kind: infrastructure/virtual-machine
name: kafka-machine-arm
provider: any
based_on: kafka-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: kubernetes-master-machine-arm
provider: any
based_on: kubernetes-master-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: kubernetes-node-machine-arm
provider: any
based_on: kubernetes-node-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: logging-machine-arm
provider: any
based_on: logging-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: monitoring-machine-arm
provider: any
based_on: monitoring-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: postgresql-machine-arm
provider: any
based_on: postgresql-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: lb-machine-arm
provider: any
based_on: load-balancer-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: rabbitmq-machine-arm
provider: any
based_on: rabbitmq-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: ignite-machine-arm
provider: any
based_on: ignite-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: opendistro-machine-arm
provider: any
based_on: logging-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: infrastructure/virtual-machine
name: repository-machine-cent
provider: any
based_on: repository-machine
specification:
  hostname: hostname
  ip: x.x.x.x
---
kind: configuration/postgresql
name: default
provider: any
specification:
  extensions:
    pgaudit:
      enabled: yes
    pgbouncer:
      enabled: no
    replication:
      enabled: no
title: Postgresql
---        
kind: configuration/rabbitmq
title: "RabbitMQ"
provider: any
name: default
specification:
  rabbitmq_plugins:
    - rabbitmq_management_agent
    - rabbitmq_management
  cluster:
    is_clustered: true
---
kind: configuration/applications
title: "Kubernetes Applications Config"
provider: any
name: default
specification:
  applications:
  - name: auth-service # requires PostgreSQL to be installed in cluster
    enabled: yes
    image_path: epiphanyplatform/keycloak:9.0.0
    use_local_image_registry: true
    #image_pull_secret_name: regcred
    service:
      name: as-testauthdb
      port: 30104
      replicas: 2
      namespace: namespace-for-auth
      admin_user: auth-service-username
      admin_password: PASSWORD_TO_CHANGE
    database:
      name: auth-database-name
      #port: "5432" # leave it when default
      user: auth-db-user
      password: PASSWORD_TO_CHANGE
  - name: rabbitmq
    enabled: yes
    image_path: rabbitmq:3.8.9
    use_local_image_registry: true
    #image_pull_secret_name: regcred # optional
    service:
      name: rabbitmq-cluster
      port: 30672
      management_port: 31672
      replicas: 2
      namespace: queue
    rabbitmq:
      #amqp_port: 5672 #optional - default 5672
      plugins: # optional list of RabbitMQ plugins
        - rabbitmq_management_agent
        - rabbitmq_management
      policies: # optional list of RabbitMQ policies
        - name: ha-policy2
          pattern: ".*"
          definitions:
            ha-mode: all
      custom_configurations: #optional list of RabbitMQ configurations (new format -> https://www.rabbitmq.com/configure.html)
        - name: vm_memory_high_watermark.relative
          value: 0.5
      #cluster:
        #is_clustered: true #redundant in in-Kubernetes installation, it will always be clustered
        #cookie: "cookieSetFromDataYaml" #optional - default value will be random generated string
  - name: ignite-stateless
    enabled: yes
    image_path: "epiphanyplatform/ignite:2.9.1" # it will be part of the image path: {{local_repository}}/{{image_path}}
    use_local_image_registry: true
    namespace: ignite
    service:
      rest_nodeport: 32300
      sql_nodeport: 32301
      thinclients_nodeport: 32302
    replicas: 2
    enabled_plugins:
    - ignite-kubernetes # required to work on K8s
    - ignite-rest-http
---
kind: configuration/vault
title: Vault Config
name: default
provider: any
specification:
  vault_enabled: true
```

### ```AWS``` provider

- Important is to specify the right ```arm64``` machine type for component which can be found [here](https://aws.amazon.com/ec2/instance-types/a1/).
- Important is to specify the right ```arm64``` OS image which currently is only ```CentOS 7.9.2009 aarch64```.

```yaml
---
kind: epiphany-cluster
name: default
provider: aws
title: Epiphany cluster Config
specification:
  prefix: arm
  name: centos
  admin_user:
    key_path: /shared/ssh/testenvs/id_rsa
    name: centos
  cloud:
    credentials:
      key: xxxx
      secret: xxxx
    region: eu-west-1
    use_public_ips: true
  components:
    kafka:
      count: 2
      machine: kafka-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.5.0/24
    kubernetes_master:
      count: 1
      machine: kubernetes-master-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.1.0/24
        - availability_zone: eu-west-1b
          address_pool: 10.1.2.0/24
    kubernetes_node:
      count: 3
      machine: kubernetes-node-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.1.0/24
        - availability_zone: eu-west-1b
          address_pool: 10.1.2.0/24
    load_balancer:
      count: 1
      machine: lb-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.7.0/24
    logging:
      count: 2
      machine: logging-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.3.0/24
    monitoring:
      count: 1
      machine: monitoring-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.4.0/24
    postgresql:
      count: 1
      machine: postgresql-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.6.0/24
    rabbitmq:
      count: 2
      machine: rabbitmq-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.8.0/24
    ignite:
      count: 2
      machine: ignite-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.9.0/24
    opendistro_for_elasticsearch:
      count: 1
      machine: opendistro-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.10.0/24
    repository:
      count: 1
      machine: repository-machine-arm
      subnets:
        - availability_zone: eu-west-1a
          address_pool: 10.1.11.0/24
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
provider: aws
name: default
specification:
  os_full_name: CentOS 7.9.2009 aarch64
---
kind: infrastructure/virtual-machine
name: kafka-machine-arm
provider: aws
based_on: kafka-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: kubernetes-master-machine-arm
provider: aws
based_on: kubernetes-master-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: kubernetes-node-machine-arm
provider: aws
based_on: kubernetes-node-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: logging-machine-arm
provider: aws
based_on: logging-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: monitoring-machine-arm
provider: aws
based_on: monitoring-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: postgresql-machine-arm
provider: aws
based_on: postgresql-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: lb-machine-arm
provider: aws
based_on: load-balancer-machine
specification:
  size: a1.medium
---
kind: infrastructure/virtual-machine
name: rabbitmq-machine-arm
provider: aws
based_on: rabbitmq-machine
specification:
  size: a1.medium
---
kind: infrastructure/virtual-machine
name: ignite-machine-arm
provider: aws
based_on: ignite-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: opendistro-machine-arm
provider: aws
based_on: logging-machine
specification:
  size: a1.large
---
kind: infrastructure/virtual-machine
name: repository-machine-cent
provider: aws
based_on: repository-machine
specification:
  size: a1.large
---
kind: configuration/postgresql
name: default
provider: aws
specification:
  extensions:
    pgaudit:
      enabled: yes
    pgbouncer:
      enabled: no
    replication:
      enabled: no
title: Postgresql
---        
kind: configuration/rabbitmq
title: "RabbitMQ"
provider: aws
name: default
specification:
  rabbitmq_plugins:
    - rabbitmq_management_agent
    - rabbitmq_management
  cluster:
    is_clustered: true
---
kind: configuration/applications
title: "Kubernetes Applications Config"
provider: aws
name: default
specification:
  applications:
  - name: auth-service # requires PostgreSQL to be installed in cluster
    enabled: yes
    image_path: epiphanyplatform/keycloak:9.0.0
    use_local_image_registry: true
    #image_pull_secret_name: regcred
    service:
      name: as-testauthdb
      port: 30104
      replicas: 2
      namespace: namespace-for-auth
      admin_user: auth-service-username
      admin_password: PASSWORD_TO_CHANGE
    database:
      name: auth-database-name
      #port: "5432" # leave it when default
      user: auth-db-user
      password: PASSWORD_TO_CHANGE
  - name: rabbitmq
    enabled: yes
    image_path: rabbitmq:3.8.9
    use_local_image_registry: true
    #image_pull_secret_name: regcred # optional
    service:
      name: rabbitmq-cluster
      port: 30672
      management_port: 31672
      replicas: 2
      namespace: queue
    rabbitmq:
      #amqp_port: 5672 #optional - default 5672
      plugins: # optional list of RabbitMQ plugins
        - rabbitmq_management_agent
        - rabbitmq_management
      policies: # optional list of RabbitMQ policies
        - name: ha-policy2
          pattern: ".*"
          definitions:
            ha-mode: all
      custom_configurations: #optional list of RabbitMQ configurations (new format -> https://www.rabbitmq.com/configure.html)
        - name: vm_memory_high_watermark.relative
          value: 0.5
      #cluster:
        #is_clustered: true #redundant in in-Kubernetes installation, it will always be clustered
        #cookie: "cookieSetFromDataYaml" #optional - default value will be random generated string
  - name: ignite-stateless
    enabled: yes
    image_path: "epiphanyplatform/ignite:2.9.1" # it will be part of the image path: {{local_repository}}/{{image_path}}
    use_local_image_registry: true
    namespace: ignite
    service:
      rest_nodeport: 32300
      sql_nodeport: 32301
      thinclients_nodeport: 32302
    replicas: 2
    enabled_plugins:
    - ignite-kubernetes # required to work on K8s
    - ignite-rest-http
---
kind: configuration/vault
title: Vault Config
name: default
provider: aws
specification:
  vault_enabled: true
```

### ```Azure``` provider

```Azure``` does not have ```arm64```  support jet.
