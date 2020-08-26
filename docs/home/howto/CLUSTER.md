## How to create an Epiphany cluster on existing infrastructure

Epicli has the ability to setup a cluster on infrastructure provided by you. These can be either bare metal machines or VM's and should meet the following requirements:

*Note. Hardware requirements are not listed since this dependends on use-case, component configuration etc.*

1. The cluster machines/vm`s are connected by a network or virtual network of some sorts and can communicate which each other and have access to the internet.
2. The cluster machines/vm`s are running one of the following Linux distributions:
    - RedHat 7.6+ and < 8
    - CentOS 7.6+ and < 8
    - Ubuntu 18.04
   Other distributions/version might work but are un-tested.
3. The cluster machines/vm`s are should be accessible through SSH with a set of SSH keys you provide and configure on each machine yourself.
4. A provisioning machine that:
    - Has access to the SSH keys
    - Is on the same network as your cluster machines
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To setup the cluster do the following steps from the provisioning machine:

1. First generate a minimal data yaml file:

    ```shell
    epicli init -p any -n newcluster
    ```

    The `any` provider will tell Epicli to create a minimal data config which does not contain any cloud provider related information. If you want full control you can add the `--full` flag which will give you a configuration with all parts of a cluster that can be configured.

2. Open the configuration file and setup the  `admin_user` data:

    ```yaml
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```

    Here you should specify the path to the SSH keys and the admin user name which will be used by Anisble to provision the cluster machines.

3. Define the components you want to install and link them to the machines you want to install them on:

    Under the  `components` tag you will find a bunch of definitions like this one:

    ```yaml
    kubernetes_master:
      count: 1
      machines:
      - default-k8s-master
    ```

    The `count` specifies how much machines you want to provision with this component. The `machines` tag is the array of machine names you want to install this component on. Note that the `count` and the number of `machines` defined must match. If you don't want to use a component you can set the `count` to 0 and remove the `machines` tag. Finally a machine can be used by multiple component since multiple components can be installed on one machine of desired.

    You will also find a bunch of `infrastructure/machine`  definitions like below:

    ```yaml
    kind: infrastructure/machine
    name: default-k8s-master
    provider: any
    specification:
      hostname: master
      ip: 192.168.100.101
    ```

    Each machine name used when setting up the component layout earlier must have such a configuration where the `name` tag matches with the defined one in the components. The `hostname` and `ip` fields must be filled to match the actual cluster machines you provide. Ansible will use this to match the machine to a component which in turn will determin which roles to install on the machine.

4. Finally start the deployment with:

    ```shell
    epicli apply -f newcluster.yml --no-infra
    ```

    This will create the inventory for Ansible based on the component/machine definitions made inside the `newcluster.yml` and let Absible deploy it. Note that the `--no-infra` is important since it tells Epicli to skip the Terraform part.

## How to create an Epiphany cluster on existing airgapped infrastructure

Epicli has the ability to setup a cluster on airgapped infrastructure provided by you. These can be either bare metal machines or VM's and should meet the following requirements:

*Note. Hardware requirements are not listed since this dependends on use-case, component configuration etc.*

1. The airgapped cluster machines/vm`s are connected by a network or virtual network of some sorts and can communicate which each other:
2. The airgapped cluster machines/vm`s are running one of the following Linux distributions:
    - RedHat 7.6+ and < 8
    - CentOS 7.6+ and < 8
    - Ubuntu 18.04
   Other distributions/version might work but are un-tested.
3. The airgapped cluster machines/vm`s should be accessible through SSH with a set of SSH keys you provide and configure on each machine yourself.
2. A requirements machine that:
    - Runs the same distribution as the airgapped cluster machines/vm`s (RedHat 7, CentOS 7, Ubuntu 18.04)
    - Has access to the internet.
3. A provisioning machine that:
    - Has access to the SSH keys
    - Is on the same network as your cluster machines
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To setup the cluster do the following steps:

1. First we need to get the tooling to prepare the requirements. On the provisioning machine run:

    ```shell
    epicli prepare --os OS
    ```

    Where OS should be `centos-7`, `redhat-7`, `ubuntu-18.04`. This will create a directory called `prepare_scripts` with the following files inside:

    - download-requirements.sh
    - requirements.txt
    - skopeo_linux

2. The scripts in the `prepare_scripts` will be used to download all requirements. To do that copy the `prepare_scripts` folder over to the requirements machine and run the following command:

    ```shell
    download-requirements.sh /requirementsoutput/
    ```

    This will start downloading all requirements and put them in the `/requirementsoutput/` folder. Once run succesfully the `/requirementsoutput/` needs to be copied to the provisioning machine to be used later on.

3. Then generate a minimal data yaml file on the provisioning machine:

    ```shell
    epicli init -p any -n newcluster
    ```

    The `any` provider will tell Epicli to create a minimal data config which does not contain any cloud provider related information. If you want full control you can add the `--full` flag which will give you a configuration with all parts of a cluster that can be configured.

4. Open the configuration file and setup the  `admin_user` data:

    ```yaml
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```
    Here you should specify the path to the SSH keys and the admin user name which will be used by Anisble to provision the cluster machines.

5. Define the components you want to install and link them to the machines you want to install them on:

    Under the  `components` tag you will find a bunch of definitions like this one:

    ```yaml
    kubernetes_master:
      count: 1
      machines:
      - default-k8s-master
    ```

    The `count` specifies how much machines you want to provision with this component. The `machines` tag is the array of machine names you want to install this component on. Note that the `count` and the number of `machines` defined must match. If you don't want to use a component you can set the `count` to 0 and remove the `machines` tag. Finally a machine can be used by multiple component since multiple components can be installed on one machine of desired.

    You will also find a bunch of `infrastructure/machine`  definitions like below:

    ```yaml
    kind: infrastructure/machine
    name: default-k8s-master
    provider: any
    specification:
      hostname: master
      ip: 192.168.100.101
    ```

    Each machine name used when setting up the component layout earlier must have such a configuration where the `name` tag matches with the defined one in the components. The `hostname` and `ip` fields must be filled to match the actual cluster machines you provide. Ansible will use this to match the machine to a component which in turn will determin which roles to install on the machine.

6. Finally start the deployment with:

    ```shell
    epicli apply -f newcluster.yml --no-infra --offline-requirements /requirementsoutput/
    ```

    This will create the inventory for Ansible based on the component/machine definitions made inside the `newcluster.yml` and let Absible deploy it. Note that the `--no-infra` is important since it tells Epicli to skip the Terraform part. The `--offline-requirements` tells Epicli it is an airgapped installation and to use the  `/requirementsoutput/` requirements folder prepared in steps 1 and 2 as source for all requirements.

## How to create an Epiphany cluster on a cloud provider

Epicli has the ability to setup a cluster on one of the following cloud providers:

- Azure
- AWS

Under the hood it uses [Terraform](https://www.terraform.io/) to create the virtual infrastructure before it applies our [Anisble](https://www.ansible.com/) playbooks to provision the VM's.

You need the following prerequisites:

1. Access to one of the supported cloud providers, `aws` or `azure`.
2. Adequate resources to deploy a cluster on the cloud provider.
3. A set of SSH keys you provide.
4. A provisioning machine that:
    - Has access to the SSH keys
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To setup the cluster do the following steps from the provisioning machine:

1. First generate a minimal data yaml file:

    ```shell
    epicli init -p aws/azure -n newcluster
    ```

    The `provider` flag should be either `aws` or `azure` and will tell Epicli to create a data config which contains the specifics for that cloud provider. If you want full control you can add the `--full` flag which will give you a config with all parts of a cluster that can be configured.

2. Open the configuration file and setup the `admin_user` data:

    ```yaml
    admin_user:
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```
    Here you should specify the path to the SSH keys and the admin user name which will be used by Anisble to provision the cluster machines.

    On `Azure` the name you specify will be configured as the admin name on the VM's.

    For `AWS` the admin name is already specified and is dependent on the Linux distro image you are using for the VM's:

    - Username for Ubuntu Server: `ubuntu`
    - Username for For Redhat: `ec2-user`

3. Setup the cloud specific data:

    To let Terraform access the cloud providers you need to setup some additional cloud configuration.

    AWS:

    ```yaml
    cloud:
      region: eu-west-2
      credentials:
        key: aws_key
        secret: aws_secret
      use_public_ips: false
    ```

    The [region](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) lets you chose the most optimal place to deploy your cluster. The `key` and `secret` are needed by Terraform and can be generated in the AWS console. More information about that [here](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)

    Azure:

    ```yaml
    cloud:
      region: West Europe
      subscription_name: Subscribtion_name
      use_service_principal: false
      use_public_ips: false
    ```

    The [region](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) lets you chose the most optimal place to deploy your cluster. The `subscription_name` is the Azure subscribtion under which you want to deploy the cluster.

    Terraform will ask you to sign in to your Microsoft Azure subscibtion when it prepares to build/modify/destroy the infrastructure on `azure`. In case you need to share cluster managment with other people you can set the `use_service_principal` tag to true. This will create a service principle and uses it to manage the resources. 

    If you already have a service principle and don't want to create a new one you can do the following. Make sure the `use_service_principal` tag is set to true. Then before you run `epicli apply -f yourcluster.yml` create the following folder structure from the path you are running Epicli:

    ```shell
    /build/clustername/terraform
    ```

    Where the clustername is the name you specified under `specification.name` in your cluster yaml. Then in the terraform folder add the file named `sp.yml` and fill it with the service priciple information like so:

    ```yaml
    appId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    displayName: "app-name"
    name: "http://app-name"
    password: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    tenant: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    subscriptionId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    ```

    Epicli will read this file and automaticly use it for authentication for resource creation and management.

    For both `aws`and `azure` there is a `use_public_ips` tag. When this is true the VM's will also have a direct inferface to the internet. While this is easy for setting up a cluster for testing it should not be used in production. A VPN setup should be used which we will document in a different section (TODO).

4. Define the components you want to install:

    Under the  `components` tag you will find a bunch of definitions like this one:

    ```yaml
    kubernetes_master:
      count: 1
    ```

    The `count` specifies how much VM's you want to provision with this component. If you don't want to use a component you can set the `count` to 0.

    Note that for each cloud provider Epicli already has a default VM configuration for each component. If you need more control over the VM's, generate a config with the `--full` flag. Then each component will have an additional machine tag:

    ```yaml
    kubernetes_master:
      count: 1
      machine: kubernetes-master-machine
      ...
    ```

    This links to a `infrastructure/virtual-machine` document which can be found inside the same configuration file. It gives you full control over the VM config (size, storage, provision image, security etc.). More details on this will be documented in a different section (TODO).

5. Finally start the deployment with:

    ```shell
    epicli apply -f newcluster.yml
    ```

## How to delete an Epiphany cluster on a cloud provider

Epicli has a delete command to remove a cluster from a cloud provider (AWS, Azure). With Epicli run the following:

  ```shell
  epicli delete -b /path/to/cluster/build/folder
  ```

From the defined cluster build folder it will take the information needed to remove the resources from the cloud provider.

## Single machine cluster

---
**NOTE**

Single machine cannot be scaled up or deployed alongside other types of cluster.

---

Sometimes it might be desirable to run an Epiphany cluster on a single machine. For this purpose Epiphany ships with a `single_cluster` component configuration. This cluster comes with the following main components:

- kubernetes-master: Untainted so pods can be deployed on it
- rabbitmq: Rabbitmq for messaging instead of Kafka
- applications: For deploying the Keycloak authentication service
- postgresql: To provide a database for Keycloak

Note that components like logging and monitoring are missing since they do not provide much benefit in a single machine scenario. Also RabbitMQ is included over Kafka since that is much less resource intensive.

To get started with a single machine cluster you can use the following template as a base. Note that some configurations are omitted:

```yaml
kind: epiphany-cluster
title: Epiphany cluster Config
name: default
specification:
  prefix: dev
  name: single
  admin_user:
    name: operations
    key_path: /user/.ssh/id_rsa
  cloud:
    ... # add other cloud configuration as needed
  components:
    kubernetes_master:
      count: 0
    kubernetes_node:
      count: 0
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
      count: 1
---
kind: configuration/applications
title: "Kubernetes Applications Config"
name: default
specification:
  applications:
  - name: auth-service
    enabled: yes # set to yest to enable authentication service
    ... # add other authentication service configuration as needed
```

To create a single machine cluster using the "any" provider (with extra load\_balancer config included) use the following template below:

```yaml
kind: epiphany-cluster
title: "Epiphany cluster Config"
provider: any
name: single
specification:
  name: single
  admin_user:
    name: ubuntu
    key_path: /shared/id_rsa
  components:
    kubernetes_master:
      count: 0
    kubernetes_node:
      count: 0
    logging:
      count: 0
    monitoring:
      count: 0
    kafka:
      count: 0
    postgresql:
      count: 0
    load_balancer:
      count: 1
      configuration: default
      machines: [single-machine]
    rabbitmq:
      count: 0
    single_machine:
      count: 1
      configuration: default
      machines: [single-machine]
---
kind: configuration/haproxy
title: HAProxy
provider: any
name: default
specification:
  version: '1.8'
  service_port: 30001
  logs_max_days: 60
  self_signed_certificate_name: self-signed-fullchain.pem
  self_signed_private_key_name: self-signed-privkey.pem
  self_signed_concatenated_cert_name: self-signed-test.tld.pem
  haproxy_log_path: /var/log/haproxy.log
  stats:
    enable: true
    bind_address: 127.0.0.1:9000
    uri: /haproxy?stats
    user: operations
    password: your-haproxy-stats-pwd
  frontend:
  - name: https_front
    port: 443
    https: yes
    backend:
    - http_back1
  backend: # example backend config below
  - name: http_back1
    server_groups:
    - kubernetes_master
      # servers: # Definition for server to that hosts the application.
      # - name: "node1"
      #   address: "epiphany-vm1.domain.com"
    port: 30104
---
kind: infrastructure/machine
provider: any
name: single-machine
specification:
  hostname: x1a1
  ip: 10.20.2.10
```

## How to create custom cluster components

Epiphany gives you the ability to define custom components. This allows you define a custom set of roles for a component you want to use in your cluster and can be usefull when you for example want to maximize usage of the available machines you have at your disposal.

The first thing you will need to do is define it in the `configuration/feature-mapping` configuration. To get this configuration you can run `epicli init ... --full` command. In the `available_roles` roles section you can see all the available roles that Epiphany provides. The `roles_mapping` is where all the Epiphany components are defined and were you need to add your custom components.

Below are parts of an example `configuration/feature-mapping` were we define an new `single_machine_new` component. We want to use Kafka instead of RabbitMQ and don`t need applications and postgress since we dont want a Keycloak deployment:

```yaml
kind: configuration/feature-mapping
title: Feature mapping to roles
name: default
specification:
  available_roles: # All entries here represent the available roles within Epiphany
  - name: repository
    enabled: yes
  - name: firewall
    enabled: yes
  - name: image-registry
  ...
  roles_mapping: # All entries here represent the default components provided with Epiphany
  ...
    single_machine:
    - repository
    - image-registry
    - kubernetes-master
    - applications
    - rabbitmq
    - postgresql
    - firewall
    # Below is the new single_machine_new definition
    single_machine_new:
    - repository
    - image-registry
    - kubernetes-master
    - kafka
    - firewall
  ...
```

Once defined the new `single_machine_new` can be used inside the `epiphany-cluster` configuration:

```yaml
kind: epiphany-cluster
title: Epiphany cluster Config
name: default
specification:
  prefix: new
  name: single
  admin_user:
    name: operations
    key_path: /user/.ssh/id_rsa
  cloud:
    ... # add other cloud configuration as needed
  components:
    ... # other components as needed
    single_machine_new:
      count: x
```

*Note: After defining a new component you might also need to define aditional configurations for virtual machines and security rules depending on what you are trying to achieve.*

## How to scale or cluster components

---
**NOTE**

Not all components are supported for this action. There is a bunch of issues referenced below in this document, [one](https://github.com/epiphany-platform/epiphany/issues/1574) of them is that disks are not removed for all components after downscale.

---

Epiphany has the ability to automaticly scale and cluster certain components on cloud providers (AWS, Azure). To upscale or downscale a component the `count` number must be increased or decreased:

  ```yaml
  components:
    kubernetes_node:
      count: ...
      ...
  ```

Then when applying the changed configuration using Epicli additional VM's will be spawned and configured or removed. The following components support scaling/clustering:

- kubernetes_master: When increased this will setup additional control plane nodes, but in the case of non-ha k8s cluster, existing control plane node must be promoted first. At the moment there is [no ability](https://github.com/epiphany-platform/epiphany/issues/1579) to downscale.
- kubernetes_node: When increased this will setup additional nodes with `kubernetes_master`. There is [no ability](https://github.com/epiphany-platform/epiphany/issues/1580) to downscale.
- ignite
- kafka: When changed this will setup or remove additional nodes for the Kafka cluster. Note that there is an [issue](https://github.com/epiphany-platform/epiphany/issues/1576) that needs to be fixed before scaling usage.
- load_balancer
- logging: Sometimes it works, but often there is an [issue](https://github.com/epiphany-platform/epiphany/issues/1575) with Kibana installation that needs to be resoved
- monitoring
- opendistro_for_elasticsearch: Works the same as `logging` component, without issues if there is no `kibana` part in feature mapping configuration.
- postgresql: At the moment does not work correctly, there is an [issue](https://github.com/epiphany-platform/epiphany/issues/1577). When changed this will setup or remove additional nodes for Postgresql. Note that extra nodes can only be setup to do replication by adding the following additional `configuration/postgresql` configuration:

  ```yaml
  kind: configuration/postgresql
  ...
  specification:
    replication:
      enable: true
      user: postgresql-replication-user
      password: postgresql-replication-password
      max_wal_senders: 5
      wal_keep_segments: 32  
    ...
  ```

- rabbitmq: At the moment scaling is not supported, there is an [issue](https://github.com/epiphany-platform/epiphany/issues/1578). When changed this will setup or remove additional nodes for the RabbitMQ cluster. Note that this will require to enable clustering in the `configuration/rabbitmq` configuration:

  ```yaml
  kind: configuration/rabbitmq
  ...
  specification:
    cluster:
      is_clustered: true
  ...
  ```

## Multi master cluster

Epiphany can deploy [HA Kubernetes clusters](../../design-docs/kubernetes-ha/kubernetes-ha.md) (since v0.6). To achieve that, it is required that:

- the master count must be higher than 1 (proper values should be 1, 3, 5, 7):

  ```yaml
  kubernetes_master:
    count: 3
  ```

- the HA mode must be enabled in `configuration/shared-config`:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: false
  ```

- the regular epcli apply cycle must be executed

Epiphany can promote / convert older single-master clusters to HA mode (since v0.6). To achieve that, it is required that:

- the existing cluster is legacy single-master cluster

- the existing cluster has been [upgraded](UPGRADE.md) to Kubernetes 1.17 first

- the HA mode and HA promotion must be enabled in `configuration/shared-config`:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: true
  ```

- the regular epcli apply cycle must be executed

- since it is one-time operation, after successful promotion, the HA promotion must be disabled in the config:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: false
  ```

<em>Note: it is not supported yet to reverse HA promotion.</em>

Epiphany can scale-up existing HA clusters (including ones that were promoted). To achieve that, it is required that:

- the existing cluster must be already running in HA mode

- the master count must be higher than previous value (proper values should be 3, 5, 7):

  ```yaml
  kubernetes_master:
    count: 5
  ```

- the HA mode must be enabled in `configuration/shared-config`:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: false
  ```

- the regular epcli apply cycle must be executed

<em>Note: it is not supported yet to scale-down clusters (master count cannot be decreased).</em>

## Build artifacts

Epiphany engine produce build artifacts during each deployment. Those artifacts contains:

- Generated terraform files.
- Generated terraform state files.
- Generated cluster manifest file.
- Generated ansible files.
- Azure login credentials for `service principal` if deploying to Azure.

Artifacts contains sensitive data so it is important to keep it in safe place like `private GIT repository` or `storage with limited access`. Generated build is also important in case of scaling or updating cluster - you will it in build folder in order to edit your cluster.

Epiphany creates (or use if you don't specified it to create) service principal account which can manage all resources in subscription, please store build artifacts securely.

## Kafka replication and partition setting

When planning Kafka installation you have to think about number of partitions and replicas since it is strongly related to throughput of Kafka and its reliability. By default Kafka's `replicas` number is set to 1 - you should change it in `core/src/ansible/roles/kafka/defaults` in order to have partitions replicated to many virtual machines.  

```yaml
  ...
  replicas: 1 # Default to at least 1 (1 broker)
  partitions: 8 # 100 x brokers x replicas for reasonable size cluster. Small clusters can be less
  ...
```

You can read more [here](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster) about planning number of partitions.

## RabbitMQ installation and setting

To install RabbitMQ in single mode just add rabbitmq role to your data.yaml for your server and in general roles section. All configuration on RabbitMQ - e.g. user other than guest creation should be performed manually.

## How to use Azure availability sets

In your cluster yaml config declare as many as required objects of kind `infrastructure/availability-set` like
in the example below, change the `name` field as you wish.

```yaml
---
kind: infrastructure/availability-set
name: kube-node  # Short and simple name is preferred
specification:
# The "name" attribute is generated automatically according to Epiphany's naming conventions
  platform_fault_domain_count: 2
  platform_update_domain_count: 5
  managed: true
provider: azure
```

Then set it also in the corresponding `components` section of the `kind: epiphany-cluster` doc.

```yaml
  components:
    kafka:
      count: 0
    kubernetes_master:
      count: 1
    kubernetes_node:
# This line tells we generate the availability-set terraform template
      availability_set: kube-node  # Short and simple name is preferred
      count: 2
```

The example below shows a complete configuration. Note that it's recommended to have a dedicated availability set for each clustered component.

```yaml
# Test availability set config
---
kind: epiphany-cluster
name: default
provider: azure
specification:
  name: test-cluster
  prefix: test
  admin_user:
    key_path: /path/to/ssk/key
    name: di-dev
  cloud:
    region: Australia East
    subscription_name: <your subscription name>
    use_public_ips: true
    use_service_principal: true
  components:
    kafka:
      count: 0
    kubernetes_master:
      count: 1
    kubernetes_node:
# This line tells we generate the availability-set terraform template
      availability_set: kube-node  # Short and simple name is preferred
      count: 2
    load_balancer:
      count: 1
    logging:
      count: 0
    monitoring:
      count: 0
    postgresql:
# This line tells we generate the availability-set terraform template
      availability_set: postgresql  # Short and simple name is preferred
      count: 2
    rabbitmq:
      count: 0
title: Epiphany cluster Config
---
kind: infrastructure/availability-set
name: kube-node  # Short and simple name is preferred
specification:
# The "name" attribute (ommited here) is generated automatically according to Epiphany's naming conventions
  platform_fault_domain_count: 2
  platform_update_domain_count: 5
  managed: true
provider: azure
---
kind: infrastructure/availability-set
name: postgresql  # Short and simple name is preferred
specification:
# The "name" attribute (ommited here) is generated automatically according to Epiphany's naming conventions
  platform_fault_domain_count: 2
  platform_update_domain_count: 5
  managed: true
provider: azure
```
