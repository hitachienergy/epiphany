## Epicli

### How to create an Epiphany cluster on existing infrastructure

Epicli has the ability to setup a cluster on infrastructure provided by you. These can be either bare metal machines or VM's and should meet the following requirements:

*Note. Hardware requirements are not listed since this dependends on use-case, component configuration etc.*

1. All the machines are connected by a network or virtual network of some sorts and can communicate which each other.
2. Running one of the following Linux distributions:
    - Redhat 7.4+
    - CentOS 7.4+
    - Ubuntu 18.04
   Other distributions/version might work but are un-tested.
3. All machines should be accessible through SSH with a set of SSH keys you provide and configure on each machine yourself.
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

### How to create an Epiphany cluster on a cloud provider

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

### How to delete an Epiphany cluster on a cloud provider

Epicli has a delete command to remove a cluster from a cloud provider (AWS, Azure). With Epicli run the following:

  ```shell
  epicli apply -b /path/to/cluster/build/folder
  ```

From the defined cluster build folder it will take the information needed to remove the resources from the cloud provider.

### How to create an offline installation for an Epiphany cluster

TODO

### Single machine cluster

TODO

### How to scale components

TODO

## Legacy

### How to create an Epiphany legacy cluster on premise

0. Pull `core` repository and if needed `data` repository (contains data.yaml files that can be used as example or base for creating your own data.yaml).

1. Prepare your VM/Metal servers:
    1. Install one of supported OS: RedHat 7.4+, Ubuntu 18.04+
    2. Create user account with sudo privileges and nopasswd that will use rsa key for login.
    3. Assign static IP addresses for each of the machines - those addresses should not change after cluster creation.
    4. Assign hostnames for machines.
    5. Ensure machines have internet access - it will be needed during Epiphany execution.
    6. Machines will strongly utilize communication between each other, so ensure this communication does not go through proxy.
    7. Note down IP addresses and hostnames of your machines.

2. If you need you can create new directory in `repository_path/data/your_platform/` or you can use existing profile from data repository. Where `your_platform` can be `vmware`, `vbox`, `metal`.
3. Create or modify data.yaml.
4. Fill in data.yaml with hostname information (`nodes[*]/hosts/name`).
5. Fill in data.yaml with IP information (`nodes[*]/hosts/ips/public`).
6. You can adjust roles for each machine - according to your needs (`nodes[*]/ansible_roles`).
7. Run `bash epiphany -a -b -i -p your_platform -f your_profile` in main epiphany directory. Do not use trailing slash after profile name or as prefix to infrastructure.
8. Store artifacts in `/build` directory securely. Keep those files in order to upgrade/scale your cluster.

### How to create an Epiphany legacy cluster on Azure

0. Pull core repository and if needed data repository (contains data.yaml files that can be used as example or base for creating your own data.yaml).

1. If you need you can create new directory in `repository_path/data/azure/infrastructure/` or you can use existing profile from data repository.

2. Fill/modify content in the `data.yml` file in `repository_path/data/azure/infrastructure/your_profile` according to your needs. Please, make sure you have enough free public ips/cores assigned to your subscription.

    1. Data.yaml files can be very verbose and at the beginning you can find difficulties modifying it, especially when defining large clusters with many virtual machines. Instead of defining huge data.yaml file - you can use template.
    2. Look at data repository, there is a template for Azure environments in path `repository_path/data/azure/infrastructure/epiphany-template`
    3. Create folder and `basic-data.yaml` file in it (like `/infrastructure/epiphany-rhel-playground/basic-data.yaml`). This file contains basic data for new cluster like subscription, number of VMs, or keys location.
    4. Execute Epiphany engine with following command when using template file: `bash epiphany -a -b -i -f infrastructure/your_profile -t /infrastructure/epiphany-template`

3. If you executed point 2.4 - skip next step and go to 5.

4. Run `bash epiphany -a -b -i -f infrastructure/your_profile` in main epiphany directory. Do not use trailing slash after profile name or as prefix to infrastructure.

5. The first you run the above command line it will prompt you to login to Microsoft and show you something like the following:

    ```text
    To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code DBD7WRF3H to authenticate.
    ```

6. Store artifacts in `/build` directory securely. Keep those files in order to upgrade/scale your cluster.

    Follow the instructions and a token will be generated in your home directory and then a Service Principal will be created and you will not be prompted for this again.

7. Go to section [Azure post deployment manual steps](#azure-post-deployment-manual-steps) that may be applicable for your deployment.

### How to create legacy production environment on Azure

Keep this in mind that Epiphany will create public IPs for each of the machines, you can remove it but running Epiphany again on the same cluster will recreate public IPs.

There are no manual steps required when you finished with [How to create an Epiphany cluster on Azure](#how-to-create-an-epiphany-cluster-on-azure) until you decide to move to `production environment` where cluster's virtual machines `must not` be exposed to internet (except load balancer - HAProxy role).

Production environment on cloud should be composed of two elements:

1. Demilitarized (`DMZ`) group that contains only load balancer (HAProxy role)
2. Applications (`APPS`) group that contains all other roles

Both elements are deployed independently (for now) that is why some manual steps, that will be described in this chapter, are required.

#### 1. DMZ group

DMZ group should contain HAProxy role that is used for load balancing and TLS termination. VM that hosts HAProxy should be `the only one` accessible from internet. You can see DMZ implementation with VPN for Epiphany build cluster `repository_path/data/azure/infrastructure/epiphany-bld-dmz`.

#### 2. APPS group

APPS group contains all features/roles required by your installation - this group should contain (you can enable or disable it) also contain VPN connection so you can access dashboards and logs. You can see APPS group implementation with VPN for Epiphany build cluster `repository_path/data/azure/infrastructure/epiphany-bld-apps`, there is nothing special with this configuration - normal Epiphany data.yaml with VPN enabled (just don't forget to specify you VPN' client certificate).

When you executed two deployments you should get two resource groups (dmz, apps) with two different VNETs and VPNs.
Now manual steps goes:

1. Peer you VNET's. Go to VNET setting blade and add peering to another vnet - you have to do it twice, both ways.

2. Add monitoring endpoints for Prometheus. Load balancer (HAProxy) is separate deployment (for now), but still we have to monitor and take logs from it. That is why we have to add scrape configs for Prometheus (monitoring)

    - SSH into monitoring machine and add `two` files in folder `/etc/prometheus/file_sd/`

      ```yaml
      # OS Monitoring - haproxy-vm-node
      - targets: ['HAPROXY_MACHINE_PRIVATE_IP:9100']
        labels:
          "job": "node"
      ```

      ```yaml
      # HAProxy monitoring - haproxy-exporter
      - targets: ['HAPROXY_MACHINE_PRIVATE_IP:9101']
        labels:
          "job": "haproxy"
      ```

3. ... and configure address for Elasticsearch (logging)

    - SSH into Load Balancer (HAProxy) machine, and edit file `/etc/filebeat/filebeat.yml`.
    - Find `### KIBANA ###` section and add private IP address of Logging VM (`Kibana`) as host value
    - Find `### OUTPUTS ###` section and add private IP address of Logging VM (`Elasticsearch`) as host value

4. For security reasons you should also disassociate public IPs from your APPS virtual machines.

5. Ensure you defined firewall settings for public VM (load balancer): [How to enable/disable network traffic- firewall](#how-to-enable-disable-network-traffic)

### Single machine legacy cluster

In certain circumstances it might be desired to run an Epiphany cluster on a single machine. There are 2 example data.yamls provided for baremetal and Azure:

- `/core/data/metal/epiphany-single-machine/data.yaml`
- `/core/data/azure/infrastructure/epiphany-single-machine/data.yaml`

These will install the following minimal set of components on the machine:

- kubernetes master (Untainted so it can run and manage deployments)
- node_exporter
- prometheus
- grafana
- rabbitmq
- postgresql (for keycloak)
- keycloak (2 instances)

This bare installation will consume arround 2.8Gb of memory with the following base memory usage of the different components:

- kubernetes    : 904 MiB
- node_exporter : 38 MiB
- prometheus    : 133 MiB
- grafana       : 54 MiB
- rabbitmq      : 85 MiB
- postgresql    : 35 MiB
- keycloak      : 1 Gb

Additional resource consumption will be highly dependant on how the cluster is utilized and it will be up to the product teams to define there hardware requirements. The absolute bare minimum this cluster was tested on was a quadcore CPU with 8Gb of ram and 60Gb of storage. However a minimum of an 8 core CPU with 16Gb of ram and 100Gb of storage would be recommended.

### How to scale Kubernetes and Kafka on a legacy cluster

#### Scaling Kubernetes

For Azure specific deployment configuration for Kubernetes Node looks like that:

```yaml
vms:
  - name: vm-k8s-node
    size: Standard_DS1_v2
    os_type: linux
    count: 1
    bastian_host: false
    # roles are how you define a grouping of nodes. These values will be used to create an inventory of your cluster
    # Must be a member of the 'role' in core
    roles:
    - linux
    - worker
    - node_exporter
    - filebeat
    - reboot
```

There is 1 worker role defined - it means only one Kubernetes node virtual machine will be created and configured to join Kubernetes cluster. When Epiphany deployment was created with one Kubernetes node and then you decide to have more nodes you can simply change

```yaml
count: 1
```

to

```yaml
count: 2
```

and wait for add new node. It is important to have your build folder from initial deployment so now state will be automatically refreshed with no downtime. For more information about build folder go to [Build artifacts](#build-artifacts) section.

For all other deployments (Metal, VMWare, VirtualBox, etc.) you just have to add another definition for machine with worker role.

#### Scaling Kafka

Scaling Kafka looks exactly the same like scaling Kubernetes. Once changed `count:` property from `1` to `n` and executed Epiphany you will have `n` Kafka machines.

To add new Kafka broker to non-Azure deployment looks the same as adding new Kubernetes node.

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
