## How to enable/disable Epiphany repository VM

Enable for Ubuntu (default):

1. Enable `repository` component:

    ```yaml
    specification:
    ...
      components:
        repository:
          count: 1
    ```

Enable for AlmaLinux on AWS/Azure:

1. Enable `repository` component and specify `default_os_image`:

    ```yaml
    specification:
    ...
      cloud:
        default_os_image: almalinux-8-x86_64
        ...
      components:
        repository:
          count: 1
    ```

Enable for RHEL on AWS/Azure:

1. Enable `repository` component and specify `default_os_image`:

    ```yaml
    specification:
    ...
      cloud:
        default_os_image: rhel-8-x86_64
        ...
      components:
        repository:
          count: 1
    ```

Disable:

1. Disable `repository` component:

    ```yaml
    specification:
    ...
      components:
        repository:
          count: 0
    ```

2. Prepend `kubernetes_master` mapping (or any other mapping if you don't deploy Kubernetes) with:

    ```yaml
    kind: configuration/feature-mappings
    specification:
      mappings:
      ...
        kubernetes_master:
          - repository
          - image-registry
    ```

## How to create an Epiphany cluster on existing infrastructure

*Please read first prerequisites related to [hostname requirements](./PREREQUISITES.md#hostname-requirements).*

Epicli has the ability to set up a cluster on infrastructure provided by you. These can be either bare metal machines or VMs and should meet the following requirements:

*Note. Hardware requirements are not listed since this depends on use-case, component configuration etc.*

1. The cluster machines/VMs are connected by a network (or virtual network of some sorts) and can communicate with each other.
At least one of them (with `repository` role) has Internet access in order to download dependencies.
If there is no Internet access, you can use [air gap feature (offline mode)](#how-to-create-an-epiphany-cluster-on-existing-air-gapped-infrastructure).
2. The cluster machines/VMs are running one of the following Linux distributions:
    - AlmaLinux 8.4+
    - RedHat 8.4+
    - Ubuntu 20.04
3. The cluster machines/VMs are accessible through SSH with a set of SSH keys you provide and configure on each machine yourself (key-based authentication).
4. The user used for SSH connection (`admin_user`) has passwordless root privileges through `sudo`.
5. A provisioning machine that:
    - Has access to the SSH keys
    - Is on the same network as your cluster machines
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To set up the cluster do the following steps from the provisioning machine:

1. First generate a minimal data yaml file:

    ```shell
    epicli init -p any -n newcluster
    ```

    The `any` provider will tell Epicli to create a minimal data config which does not contain any cloud provider related information. If you want full control you can add the `--full` flag which will give you a configuration with all parts of a cluster that can be configured.

2. Open the configuration file and set up the  `admin_user` data:

    ```yaml
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```

    Here you should specify the path to the SSH keys and the admin user name which will be used by Ansible to provision the cluster machines.

3. Define the components you want to install and link them to the machines you want to install them on:

    Under the  `components` tag you will find a bunch of definitions like this one:

    ```yaml
    kubernetes_master:
      count: 1
      machines:
      - default-k8s-master
    ```

    The `count` specifies how many machines you want to provision with this component. The `machines` tag is the array of machine names you want to install this component on. Note that the `count` and the number of `machines` defined must match. If you don't want to use a component you can set the `count` to 0 and remove the `machines` tag. Finally, a machine can be used by multiple component since multiple components can be installed on one machine of desired.

    You will also find a bunch of `infrastructure/machine`  definitions like below:

    ```yaml
    kind: infrastructure/machine
    name: default-k8s-master
    provider: any
    specification:
      hostname: master
      ip: 192.168.100.101
    ```

    Each machine name used when setting up the component layout earlier must have such a configuration where the `name` tag matches with the defined one in the components. The `hostname` and `ip` fields must be filled to match the actual cluster machines you provide. Ansible will use this to match the machine to a component which in turn will determine which roles to install on the machine.

4. Finally, start the deployment with:

    ```shell
    epicli apply -f newcluster.yml --no-infra
    ```

    This will create the inventory for Ansible based on the component/machine definitions made inside the `newcluster.yml` and let Ansible deploy it. Note that the `--no-infra` is important since it tells Epicli to skip the Terraform part.

## How to create an Epiphany cluster on existing air-gapped infrastructure

*Please read first prerequisites related to [hostname requirements](./PREREQUISITES.md#hostname-requirements).*

Epicli has the ability to set up a cluster on air-gapped infrastructure provided by you. These can be either bare metal machines
or VMs and should meet the following requirements:

*Note. Hardware requirements are not listed since this depends on use-case, component configuration etc.*

1. The air-gapped cluster machines/VMs are connected by a network or virtual network of some sorts and can communicate with each other.
2. The air-gapped cluster machines/VMs are running one of the following Linux distributions:
    - RedHat 7.6+ and < 8
    - Ubuntu 20.04
3. The cluster machines/VMs are accessible through SSH with a set of SSH keys you provide and configure on each machine yourself (key-based authentication).
4. The user used for SSH connection (`admin_user`) has passwordless root privileges through `sudo`.
5. A requirements machine that:
    - Runs the same distribution as the air-gapped cluster machines/VMs (RedHat 7, Ubuntu 20.04)
    - Has access to the internet.
   If you don't have access to a similar machine/VM with internet access, you can also try to download the requirements with a Docker container. More information [here](./CLUSTER.md#downloading-offline-requirements-with-a-docker-container).
6. A provisioning machine that:
    - Has access to the SSH keys
    - Is on the same network as your cluster machines
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To set up the cluster do the following steps:

1. First we need to get the tooling to prepare the requirements. On the provisioning machine run:

    ```shell
    epicli prepare --os OS --arch ARCH
    ```

    Where:
    - OS should be `almalinux-8`, `rhel-8`, `ubuntu-20.04`
    - ARCH should be `x86_64`, `arm64`

    This will create a directory called `prepare_scripts` with the needed files inside.

2. The scripts in the `prepare_scripts` will be used to download all requirements. To do that copy the `prepare_scripts` folder over to the requirements machine and run the following command:

    ```shell
    download-requirements.py /requirementsoutput/ OS
    ```

    Where:
    - OS should be `almalinux-8`, `rhel-8`, `ubuntu-20.04`, `detect`
    - /requirementsoutput/ where to output downloaded requirements

    This will run the download-requirements script for target OS type and save requirements under /requirementsoutput/. Once run successfully the `/requirementsoutput/` needs to be copied to the provisioning machine to be used later on.

3. Then generate a minimal data yaml file on the provisioning machine:

    ```shell
    epicli init -p any -n newcluster
    ```

    The `any` provider will tell Epicli to create a minimal data config which does not contain any cloud provider related information. If you want full control you can add the `--full` flag which will give you a configuration with all parts of a cluster that can be configured.

4. Open the configuration file and set up the  `admin_user` data:

    ```yaml
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```

    Here you should specify the path to the SSH keys and the admin user name which will be used by Ansible to provision the cluster machines.

5. Define the components you want to install and link them to the machines you want to install them on:

    Under the  `components` tag you will find a bunch of definitions like this one:

    ```yaml
    kubernetes_master:
      count: 1
      machines:
      - default-k8s-master
    ```

    The `count` specifies how many machines you want to provision with this component. The `machines` tag is the array of machine names you want to install this component on. Note that the `count` and the number of `machines` defined must match. If you don't want to use a component you can set the `count` to 0 and remove the `machines` tag. Finally, a machine can be used by multiple component since multiple components can be installed on one machine of desired.

    You will also find a bunch of `infrastructure/machine`  definitions like below:

    ```yaml
    kind: infrastructure/machine
    name: default-k8s-master
    provider: any
    specification:
      hostname: master
      ip: 192.168.100.101
    ```

    Each machine name used when setting up the component layout earlier must have such a configuration where the `name` tag matches with the defined one in the components. The `hostname` and `ip` fields must be filled to match the actual cluster machines you provide. Ansible will use this to match the machine to a component which in turn will determine which roles to install on the machine.

6. Finally, start the deployment with:

    ```shell
    epicli apply -f newcluster.yml --no-infra --offline-requirements /requirementsoutput/
    ```

    This will create the inventory for Ansible based on the component/machine definitions made inside the `newcluster.yml` and let Ansible deploy it. Note that the `--no-infra` is important since it tells Epicli to skip the Terraform part. The `--offline-requirements` tells Epicli it is an air-gapped installation and to use the  `/requirementsoutput/` requirements folder prepared in steps 1 and 2 as source for all requirements.

## How to create an Epiphany cluster using custom system repository and Docker image registry

Epiphany has the ability to use external repository and image registry during `epicli apply` execution.

Custom urls need to be specified inside the `configuration/shared-config` document, for example:

```yaml
kind: configuration/shared-config
title: Shared configuration that will be visible to all roles
name: default
specification:
  custom_image_registry_address: "10.50.2.1:5000"
  custom_repository_url: "http://10.50.2.1:8080/epirepo"
  use_ha_control_plane: false
```

The repository and image registry implementation must be compatible with already existing Ansible code:

- the repository data (including apt or yum repository) is served from HTTP server and structured exactly as in the offline package
- the image registry data is loaded into and served from standard Docker registry implementation

*Note. If both custom repository/registry and offline installation are configured then the custom repository/registry is preferred.*

*Note. You can switch between custom repository/registry and offline/online installation methods. Keep in mind this will cause "imageRegistry" change in Kubernetes which in turn may cause short downtime.*

By default, Epiphany creates "repository" virtual machine for cloud environments. When custom repository and registry are used there is no need for additional empty VM.
The following config snippet can illustrate how to mitigate this problem:

```yaml
kind: epiphany-cluster
title: Epiphany cluster Config
provider: <provider>
name: default
specification:
  ...
  components:
    repository:
      count: 0
    kubernetes_master:
      count: 1
    kubernetes_node:
      count: 2
---
kind: configuration/feature-mappings
title: "Feature mapping to components"
provider: <provider>
name: default
specification:
  mappings:
    kubernetes_master:
      - repository
      - image-registry
      - kubernetes-master
      - helm
      - applications
      - node-exporter
      - filebeat
      - firewall
---
kind: configuration/shared-config
title: Shared configuration that will be visible to all roles
provider: <provider>
name: default
specification:
  custom_image_registry_address: "<ip-address>:5000"
  custom_repository_url: "http://<ip-address>:8080/epirepo"
```

1. Disable `repository` component:

   ```yaml
   repository:
     count: 0
   ```

2. Prepend "kubernetes\_master" mapping (or any other mapping if you don't deploy Kubernetes) with:

   ```yaml
   kubernetes_master:
     - repository
     - image-registry
   ```

3. Specify custom repository/registry in `configuration/shared-config`:

   ```yaml
   specification:
     custom_image_registry_address: "<ip-address>:5000"
     custom_repository_url: "http://<ip-address>:8080/epirepo"
   ```

## How to create an Epiphany cluster on a cloud provider

*Please read first prerequisites related to [hostname requirements](./PREREQUISITES.md#hostname-requirements).*

Epicli has the ability to set up a cluster on one of the following cloud providers:

- Azure
- AWS

Under the hood it uses [Terraform](https://www.terraform.io/) to create the virtual infrastructure before it applies our [Ansible](https://www.ansible.com/) playbooks to provision the VMs.

You need the following prerequisites:

1. Access to one of the supported cloud providers, `aws` or `azure`.
2. Adequate resources to deploy a cluster on the cloud provider.
3. A set of SSH keys you provide.
4. A provisioning machine that:
    - Has access to the SSH keys
    - Has Epicli running.
      *Note. To run Epicli check the [Prerequisites](./PREREQUISITES.md)*

To set up the cluster do the following steps from the provisioning machine:

1. First generate a minimal data yaml file:

    ```shell
    epicli init -p aws/azure -n newcluster
    ```

    The `provider` flag should be either `aws` or `azure` and will tell Epicli to create a data config which contains the specifics for that cloud provider. If you want full control you can add the `--full` flag which will give you a config with all parts of a cluster that can be configured.

2. Open the configuration file and set up the `admin_user` data:

    ```yaml
    admin_user:
      key_path: /path/to/your/ssh/keys
      name: user_name
    ```

    Here you should specify the path to the SSH keys and the admin user name which will be used by Ansible to provision the cluster machines.

    On `Azure` the name you specify will be configured as the admin name on the VM's.

    For `AWS` the admin name is already specified and is dependent on the Linux distro image you are using for the VM's:

    - Username for Ubuntu Server: `ubuntu`
    - Username for AlmaLinux/RHEL: `ec2-user`

3. Set up the cloud specific data:

    To let Terraform access the cloud providers you need to set up some additional cloud configuration.

    AWS:

    ```yaml
    cloud:
      region: eu-west-2
      credentials:
        access_key_id: aws_key
        secret_access_key: aws_secret
      use_public_ips: false
      default_os_image: default
    ```

    The [region](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) lets you chose the optimal place to deploy your cluster. The `access_key_id` and `secret_access_key` are needed by Terraform and can be generated in the AWS console. More information about that [here](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys)

    Azure:

    ```yaml
    cloud:
      region: West Europe
      subscription_name: Subscribtion_name
      use_service_principal: false
      use_public_ips: false
      default_os_image: default
    ```

    The [region](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html) lets you chose the most optimal place to deploy your cluster. The `subscription_name` is the Azure subscription under which you want to deploy the cluster.

    Terraform will ask you to sign in to your Microsoft Azure subscription when it prepares to build/modify/destroy the infrastructure on `azure`. In case you need to share cluster management with other people you can set the `use_service_principal` tag to true. This will create a service principle and uses it to manage the resources.

    If you already have a service principle and don't want to create a new one you can do the following. Make sure the `use_service_principal` tag is set to true. Then before you run `epicli apply -f yourcluster.yml` create the following folder structure from the path you are running Epicli:

    ```shell
    /path/to/build_dir/clustername/terraform
    ```

    Where the `clustername` is the name you specified under `specification.name` in your cluster definition yaml. Then in `terraform` folder add the file named `sp.yml` and fill it up with the service principal information like so:

    ```yaml
    appId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    displayName: "app-name"
    name: "http://app-name"
    password: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    tenant: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    subscriptionId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
    ```

    Epicli will read this file and automatically use it for authentication for resource creation and management.

    For both `aws`and `azure` the following cloud attributes overlap:
    - `use_public_ips`: When `true`, the VMs will also have a direct interface to the internet. While this is easy for setting up a cluster for testing, it should not be used in production. A VPN setup should be used which we will document in a different section (TODO).
    - `default_os_image`: Lets you more easily select Epiphany team validated and tested OS images. When one is selected, it will be applied to **every** `infrastructure/virtual-machine` document in the cluster regardless of user defined ones.
                  The following values are accepted:
                  - `default`: Applies user defined `infrastructure/virtual-machine` documents when generating a new configuration.
                  - `ubuntu-20.04-x86_64`: Applies the latest validated and tested Ubuntu 20.04 image to all `infrastructure/virtual-machine` documents on `x86_64` on Azure and AWS.
                  - `rhel-8-x86_64`: Applies the latest validated and tested RedHat 8.x image to all `infrastructure/virtual-machine` documents on `x86_64` on Azure and AWS.
                  - `almalinux-8-x86_64`: Applies the latest validated and tested AlmaLinux 8.x image to all `infrastructure/virtual-machine` documents on `x86_64` on Azure and AWS.
                  - `almalinux-8-arm64`: Applies the latest validated and tested AlmaLinux 8.x image to all `infrastructure/virtual-machine` documents on `arm64` on AWS. Azure currently doesn't support `arm64`.
                  The images which will be used for these values will be updated and tested on regular basis.

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

5. Finally, start the deployment with:

    ```shell
    epicli apply -f newcluster.yml
    ```

### Note for RHEL Azure images

Epiphany currently supports RHEL 8 RAW-partitioned images (`rhel-raw` [offer](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/redhat.rhel-raw))
attached to standard RHEL repositories. For more details, refer to [Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/workloads/redhat/redhat-images).

In the past Epiphany supported LVM-partitioned images (`RHEL` [offer](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/redhat.rhel-20190605))
which require merging small logical volumes in order to deploy a cluster. This feature is still present but not tested.
It uses cloud-init custom data to merge small logical volumes (`homelv`, `optlv`, `tmplv` and `varlv`)
into the `rootlv` which is extended (with underlying filesystem) by the current free space in its volume group.
The `usrlv` LV, which has 10G, is not merged since it would require a reboot.
The merging [can be disabled](#how-to-disable-merging-lvm-logical-volumes) for troubleshooting since it performs some
administrative tasks (such as remounting filesystems or restarting services).

NOTE: RHEL LVM images require at least 64 GB for OS disk.

### How to disable merging LVM logical volumes

In order to not merge logical volumes (for troubleshooting), use the following doc:

```yaml
kind: infrastructure/cloud-init-custom-data
title: cloud-init user-data
provider: azure
name: default
specification:
  enabled: false
```

## How to delete an Epiphany cluster on a cloud provider

Epicli has a delete command to remove a cluster from a cloud provider (AWS, Azure). With Epicli run the following:

  ```shell
  epicli delete -b /path/to/cluster/build/folder
  ```

From the defined cluster build folder it will take the information needed to remove the resources from the cloud provider.

### Note for Azure cloud provider

Make sure you can safely remove OS and data disks - Epiphany does not support cluster removal from Azure
while preserving existing disks.

## Single machine cluster

*Please read first prerequisites related to [hostname requirements](./PREREQUISITES.md#hostname-requirements).*

---
**NOTE**

Single machine cannot be scaled up or deployed alongside other types of cluster.

---

Sometimes it might be desirable to run an Epiphany cluster on a single machine. For this purpose Epiphany ships with a `single_cluster` component configuration. This cluster comes with the following main components:

- kubernetes-master: Untainted so pods can be deployed on it
- rabbitmq: Rabbitmq for messaging instead of Kafka
- applications: For deploying the Keycloak authentication service
- postgresql: To provide a database for Keycloak

Note that components like logging and monitoring are missing since they do not provide much benefit in a single machine scenario. Also, RabbitMQ is included over Kafka since that is much less resource intensive.

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
    opensearch:
      count: 0
    single_machine:
      count: 1
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
title: "HAProxy"
provider: any
name: default
specification:
  logs_max_days: 60
  self_signed_certificate_name: self-signed-fullchain.pem
  self_signed_private_key_name: self-signed-privkey.pem
  self_signed_concatenated_cert_name: self-signed-test.tld.pem
  haproxy_log_path: "/var/log/haproxy.log"

  stats:
    enable: true
    bind_address: 127.0.0.1
    port: 9000
    uri: "/haproxy?stats"
    user: operations
    password: your-haproxy-stats-pwd
  metrics:
    enable: true
    bind_address: "*"
    port: 9101
  frontend:
    - name: https_front
      port: 443
      https: yes
      backend:
      - http_back1
  backend: # example backend config below
    - name: http_back1
      server_groups:
      - kubernetes_node
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

Epiphany gives you the ability to define custom components. This allows you to define a custom set of roles for a component you want to use in your cluster. It can be useful when you for example want to maximize usage of the available machines you have at your disposal.

The first thing you will need to do is define it in the `configuration/features` and the `configuration/feature-mappings` configurations. To get these configurations you can run `epicli init ... --full` command. In the `configuration/features` doc you can see all the available features that Epiphany provides. The `configuration/feature-mappings` doc is where all the Epiphany components are defined and where you can add your custom components.

Below are parts of an example `configuration/features` and `configuration/feature-mappings` docs where we define a new `single_machine_new` component. We want to use Kafka instead of RabbitMQ and don't need applications and postgres since we don't want a Keycloak deployment:

```yaml
kind: configuration/features
title: "Features to be enabled/disabled"
name: default
specification:
  features:  # All entries here represent the available features within Epiphany
    - name: repository
      enabled: yes
    - name: firewall
      enabled: yes
    - name: image-registry
    ...
---
kind: configuration/feature-mappings
title: "Feature mapping to components"
name: default
specification:
  mappings: # All entries here represent the default components provided with Epiphany
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

*Note: After defining a new component you might also need to define additional configurations for virtual machines and security rules depending on what you are trying to achieve.*

## How to scale or cluster components

Not all components are supported for this action. There is a bunch of issues referenced below in this document.

Epiphany has the ability to automatically scale and cluster certain components on cloud providers (AWS, Azure). To upscale or downscale a component the `count` number must be increased or decreased:

  ```yaml
  components:
    kubernetes_node:
      count: ...
      ...
  ```

Then when applying the changed configuration using Epicli, additional VM's will be spawned and configured or removed. The following table shows what kind of operation component supports:

Component | Scale up | Scale down | HA | Clustered |Known issues
--- | --- | --- | --- | --- | ---
Repository | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | --- |
Monitoring | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | ---
Logging | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | ---
Kubernetes master | :heavy_check_mark: | :x: | :heavy_check_mark: | :heavy_check_mark: | [#1579](https://github.com/epiphany-platform/epiphany/issues/1579)
Kubernetes node | :heavy_check_mark: | :x: | :heavy_check_mark: | :heavy_check_mark: | [#1580](https://github.com/epiphany-platform/epiphany/issues/1580)
Kafka | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | ---
Load Balancer | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | ---
OpenSearch | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | ---
Postgresql | :x: | :x: | :heavy_check_mark: | :heavy_check_mark: | [#1577](https://github.com/epiphany-platform/epiphany/issues/1577)
RabbitMQ | :heavy_check_mark: | :heavy_check_mark: | :x: | :heavy_check_mark: |  [#1578](https://github.com/epiphany-platform/epiphany/issues/1578), [#1309](https://github.com/epiphany-platform/epiphany/issues/1309)
RabbitMQ K8s | :heavy_check_mark: | :heavy_check_mark: | :x: | :heavy_check_mark: | [#1486](https://github.com/epiphany-platform/epiphany/issues/1486)
Keycloak K8s | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | ---
Pgpool K8s | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | ---
Pgbouncer K8s | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | ---

Additional notes:

- Repository:  
In standard Epiphany deployment only one repository machine is required.  
:arrow_up: Scaling up the repository component will create a new standalone VM.  
:arrow_down: Scaling down will remove it in LIFO order (Last In, First Out).  
However, even if you create more than one VM, by default all other components will use the first one.
- Kubernetes master:  
:arrow_up: When increased this will set up additional control plane nodes, but in the case of non-ha k8s cluster, the existing control plane node must be promoted first.  
:arrow_down: At the moment there is no ability to downscale.
- Kubernetes node:  
:arrow_up: When increased this will set up an additional node and join into the Kubernetes cluster.  
:arrow_down: There is no ability to downscale.
- Load balancer:  
:arrow_up: Scaling up the load_balancer component will create a new standalone VM.  
:arrow_down: Scaling down will remove it in LIFO order (Last In, First Out).
- Logging:  
:arrow_up:  Scaling up will create new VM with both Kibana and ODFE components inside.  
ODFE will join the cluster but Kibana will be a standalone instance.  
:arrow_down: When scaling down VM will be deleted.
- Monitoring:  
:arrow_up: Scaling up the monitoring component will create a new standalone VM.  
:arrow_down: Scaling down will remove it in LIFO order (Last In, First Out).
- Postgresql:  
:arrow_up: At the moment does not support scaling up. Check known issues.  
:arrow_down: At the moment does not support scaling down. Check known issues.
- RabbitMQ:  
If the instance count is changed, then additional RabbitMQ nodes will be added or removed.  
:arrow_up: Will create new VM and adds it to the RabbitMQ cluster.  
:arrow_down: At the moment scaling down will just remove VM. All data not processed on this VM will be purged. Check known issues.  
Note that clustering requires a change in the `configuration/rabbitmq` document:

  ```yaml
  kind: configuration/rabbitmq
  ...
  specification:
    cluster:
      is_clustered: true
  ...
  ```

- RabbitMQ K8s:
  Scaling is controlled via replicas in StatefulSet. RabbitMQ on K8s uses plugin rabbitmq_peer_discovery_k8s to works in cluster.

Additional known issues:

- [#1574](https://github.com/epiphany-platform/epiphany/issues/1574) - Disks are not removed after downscale of any Epiphany component on Azure.

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

- the regular epicli apply cycle must be executed

Epiphany can promote / convert older single-master clusters to HA mode (since v0.6). To achieve that, it is required that:

- the existing cluster is legacy single-master cluster

- the existing cluster has been [upgraded](UPGRADE.md) to Kubernetes 1.17 or above first

- the HA mode and HA promotion must be enabled in `configuration/shared-config`:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: true
  ```

- the regular epicli apply cycle must be executed

- since it is one-time operation, after successful promotion, the HA promotion must be disabled in the config:

  ```yaml
  kind: configuration/shared-config
  ...
  specification:
    use_ha_control_plane: true
    promote_to_ha: false
  ```

*Note: It is not supported yet to reverse HA promotion.*

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

- the regular epicli apply cycle must be executed

*Note: It is not supported yet to scale-down clusters (master count cannot be decreased).*

## Build artifacts

Epiphany engine produce build artifacts during each deployment. Those artifacts contain:

- Generated terraform files.
- Generated terraform state files.
- Generated cluster manifest file.
- Generated ansible files.
- Azure login credentials for `service principal` if deploying to Azure.

Artifacts contain sensitive data, so it is important to keep it in safe place like `private GIT repository` or `storage with limited access`. Generated build is also important in case of scaling or updating cluster - you will it in build folder in order to edit your cluster.

Epiphany creates (or use if you don't specified it to create) service principal account which can manage all resources in subscription, please store build artifacts securely.

## Kafka replication and partition setting

When planning Kafka installation you have to think about number of partitions and replicas since it is strongly related to throughput of Kafka and its reliability. By default, Kafka's `replicas` number is set to 1 - you should change it in `core/src/ansible/roles/kafka/defaults` in order to have partitions replicated to many virtual machines.  

```yaml
  ...
  replicas: 1 # Default to at least 1 (1 broker)
  partitions: 8 # 100 x brokers x replicas for reasonable size cluster. Small clusters can be less
  ...
```

You can read more [here](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster) about planning number of partitions.

## RabbitMQ installation and setting

To install RabbitMQ in single mode just add rabbitmq role to your data.yaml for your server and in general roles section. All configuration on RabbitMQ, e.g., user other than guest creation should be performed manually.

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
# The "name" attribute (omitted here) is generated automatically according to Epiphany's naming conventions
  platform_fault_domain_count: 2
  platform_update_domain_count: 5
  managed: true
provider: azure
---
kind: infrastructure/availability-set
name: postgresql  # Short and simple name is preferred
specification:
# The "name" attribute (omitted here) is generated automatically according to Epiphany's naming conventions
  platform_fault_domain_count: 2
  platform_update_domain_count: 5
  managed: true
provider: azure
```

## Downloading offline requirements with a Docker container

This paragraph describes how to use a Docker container to download the requirements for air-gapped/offline installations. At this time we don't officially support this, and we still recommend using a full distribution which is the same as the air-gapped cluster machines/VMs.

A few points:

- This only describes how to set up the Docker containers for downloading. The rest of the steps are similar as in the paragraph [here](./CLUSTER.md#how-to-create-an-epiphany-cluster-on-existing-air-gapped-infrastructure).
- Main reason why you might want to give this a try is to download ```arm64``` architecture requirements on a ```x86_64``` machine. More information on the current state of ```arm64``` support can be found [here](./../ARM.md#arm).

### Ubuntu 20.04

For Ubuntu, you can use the following command to launch a container:

```shell
docker run -v /shared_folder:/home <--platform linux/amd64 or --platform linux/arm64> --rm -it ubuntu:20.04
```

As the ```ubuntu:20.04``` image is multi-arch you can include ```--platform linux/amd64``` or ```--platform linux/arm64``` to run the container as the specified architecture. The ```/shared_folder``` should be a folder on your local machine containing the required scripts.

When you are inside the container run the following commands to prepare for the running of the ```download-requirements.py``` script:

```shell
apt-get update # update the package manager
apt-get install sudo # install sudo so we can make the download-requirements.py executable and run it as root
sudo chmod +x /home/download-requirements.py # make the requirements script executable
```

After this you should be able to run the ```download-requirements.py``` from the ```home``` folder.

### RedHat 8.x

For RedHat you can use the following command to launch a container:

```shell
docker run -v /shared_folder:/home <--platform linux/amd64 or --platform linux/arm64> --rm -it registry.access.redhat.com/ubi8/ubi:8.4
```

As the ```registry.access.redhat.com/ubi8/ubi:8.4``` image is multi-arch you can include ```--platform linux/amd64``` or ```--platform linux/arm64``` to run the container as the specified architecture. The ```/shared_folder``` should be a folder on your local machine containing the requirement scripts.

For running the ```download-requirements.py``` script you will need a RedHat developer subscription to register the running container and make sure you can access to official Redhat repos for the packages needed. More information on getting this free subscription [here](https://developers.redhat.com/articles/getting-red-hat-developer-subscription-what-rhel-users-need-know).

When you are inside the container run the following commands to prepare for the running of the ```download-requirements.py``` script:

```shell
subscription-manager register # will ask for you credentials of your RedHat developer subscription and setup the container
subscription-manager attach --auto # will enable the RedHat official repositories
chmod +x /home/download-requirements.py # make the requirements script executable
```

After this you should be able to run the ```download-requirements.py```  from the ```home``` folder:

```shell
/usr/libexec/platform-python /home/download-requirements.py /home/offline_requirements_rhel_8_x86_64 rhel-8
```

### AlmaLinux 8.x

For AlmaLinux, you can use the following command to launch a container:

```shell
docker run -v /shared_folder:/home --rm -it almalinux:8.4
```

The ```almalinux:8.4``` image is amd64 arch only. The ```/shared_folder``` should be a folder on your local machine containing the requirement scripts.

When you are inside the container run the following command to prepare for the running of the ```download-requirements.py``` script:

```shell
chmod +x /home/download-requirements.py # make the requirements script executable
```

After this you should be able to run the ```download-requirements.py```  from the ```home``` folder:

```shell
/usr/libexec/platform-python /home/download-requirements.py /home/offline_requirements_almalinux_8_4_x86_64 almalinux-8
```

### Known issues

In some local environments (eg. using AlmaLinux image) the following issue could appear:

```sh
Failed to set locale, defaulting to C.UTF-8
```

To fix the issue, verify or set your locales. Example: `export LC_ALL=C.UTF-8`

## How to additional custom Terraform templates

For both cloud providers (AWS, Azure) Epicli generates the following terraform components for deploying a cluster:

- VPC (AWS) or VNet (Azure)
- Subnets inside the VPC or VNet
- Security rules between the subnets
- Virtual machines with network interfaces deployed in the different subnets

Sometimes it is required to have additional resources like VPN access or other cloud native resources like EKS or AKS to this infrastructure. Epiphany gives the user the ability to add these additional resources during or after the cluster creation.

The Terraform scripts Epicli generates will have the following naming convention:

```shell
xxx_resourc-name-nr.tf
```

And will be placed in the following folder:

```shell
/shared/build/clustername/terraform
```

When Epicli is run/re-run any Terraform scripts which will start with the ```xxx_*.tf``` filter  will be removed and regenerated. The user can make custom Terraform scripts and place them allongside the Epicli generated ones and these will be applied/re-applied during the Epicli run.

If you need to define any additional security rules for component subnets for custom infrastructure you can check the documentation [here](./SECURITY_GROUPS.md).
