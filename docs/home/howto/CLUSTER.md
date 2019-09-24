## Epicli

### How to create an Epiphany cluster on premise

TODO

### How to create an offline installation for an Epiphany cluster

TODO

### How to create an Epiphany cluster on a cloud provider

TODO

### Single machine cluster

TODO

### How to scale Kubernetes, Kafka and RabbitMQ

TODO

## Legacy

### How to create an Epiphany legacy cluster on premise

0. Pull `core` repository and if needed `data` repository (contains data.yaml files that can be used as example or base for creating your own data.yaml).

1. Prepare your VM/Metal servers:
    1. Install one of supported OS: RedHat 7.4+, Ubuntu 16.04+
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

### Build artifacts

Epiphany engine produce build artifacts during each deployment. Those artifacts contains:

- Generated terraform files.
- Generated terraform state files.
- Generated cluster manifest file.
- Generated ansible files.
- Azure login credentials for `service principal` if deploying to Azure.

Artifacts contains sensitive data so it is important to keep it in safe place like `private GIT repository` or `storage with limited access`. Generated build is also important in case of scaling or updating cluster - you will it in build folder in order to edit your cluster.

Epiphany creates (or use if you don't specified it to create) service principal account which can manage all resources in subscription, please store build artifacts securely.

### Kafka replication and partition setting

When planning Kafka installation you have to think about number of partitions and replicas since it is strongly related to throughput of Kafka and its reliability. By default Kafka's `replicas` number is set to 1 - you should change it in `core/src/ansible/roles/kafka/defaults` in order to have partitions replicated to many virtual machines.  

```yaml
  ...
  replicas: 1 # Default to at least 1 (1 broker)
  partitions: 8 # 100 x brokers x replicas for reasonable size cluster. Small clusters can be less
  ...
```

You can read more [here](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster) about planning number of partitions.

### RabbitMQ installation and setting

To install RabbitMQ in single mode just add rabbitmq role to your data.yaml for your server and in general roles section. All configuration on RabbitMQ - e.g. user other than guest creation should be performed manually.
