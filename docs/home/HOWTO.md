# How-To Guides

## Contents

- [Prerequisites for Epiphany engine](#prerequisites-to-run-epiphany-engine)
  - [Run directly from OS](#run-directly-from-os)
  - [Run with Docker image for development](#run-with-docker-image-for-development)
  - [Run with Docker image for deployment](#run-with-docker-image-for-deployment)
  - [Note for Windows users](#note-for-windows-users)
- Epiphany cluster
  - [How to create an Epiphany cluster on premise](#how-to-create-an-epiphany-cluster-on-premise)
  - [How to create an Epiphany cluster on Azure](#how-to-create-an-epiphany-cluster-on-azure)
  - [How to create production environment on Azure](#how-to-create-production-environment-on-azure)
  - [Build artifacts](#build-artifacts)
  - [How to scale Kubernetes and Kafka](#how-to-scale-kubernetes-and-kafka)
  - [Kafka replication and partition setting](#kafka-replication-and-partition-setting)
  - [RabbitMQ installation and setting](#rabbitmq-installation-and-setting)
  - [Single machine cluster](#single-machine-cluster)
- Monitoring
  - [Import and create of Grafana dashboards](#import-and-create-of-grafana-dashboards)
  - [How to configure Kibana](#how-to-configure-kibana)
  - [How to configure Prometheus alerts](#how-to-configure-prometheus-alerts)
  - [How to configure scalable Prometheus setup](#how-to-configure-scalable-prometheus-setup)
  - [How to configure Azure additional monitoring and alerting](#how-to-configure-azure-additional-monitoring-and-alerting)
- Kubernetes
  - [How to do Kubernetes RBAC](#how-to-do-kubernetes-rbac)
  - [How to run an example app](#how-to-run-an-example-app)
  - [How to set resource requests and limits for Containers](#how-to-set-resource-requests-and-limits-for-containers)
  - [How to run CronJobs](#how-to-run-cronjobs)
  - [How to test the monitoring features](#how-to-test-the-monitoring-features)
  - [How to run chaos on Epiphany Kubernetes cluster and monitor it with Grafana](#how-to-run-chaos-on-epiphany-kubernetes-cluster-and-monitor-it-with-grafana)
  - [How to tunnel Kubernetes dashboard from remote kubectl to your PC](#how-to-tunnel-kubernetes-dashboard-from-remote-kubectl-to-your-pc)
  - [How to setup Azure VM as docker machine for development](#how-to-setup-azure-vm-as-docker-machine-for-development)
  - [How to upgrade Kubernetes cluster](#how-to-upgrade-kubernetes-cluster)
  - [How to upgrade Kubernetes cluster from 1.13.0 to 1.13.1](#how-to-upgrade-kubernetes-cluster-from-1130-to-1131)
  - [How to authenticate to Azure AD app](#how-to-authenticate-to-azure-ad-app)
  - [How to expose service through HA Proxy load balancer](#how-to-expose-service-lb)
- Security
  - [How to use TLS/SSL certificate with HA Proxy](#how-to-use-tls/ssl-certificate-with-ha-proxy)
  - [How to use Kubernetes Secrets](#how-to-use-kubernetes-secrets)
  - [How to enable or disable network traffic - firewall](#how-to-enable-or-disable-network-traffic)
  - [Client certificate for Azure VPN connection](#client-certificate-for-azure-vpn-connection)
- [Data and log retention](#data-and-log-retention)
  - [Elasticsearch](#elasticsearch)
  - [Grafana](#grafana)
  - [Kafka](#kafka)
  - [Kibana](#kibana)
  - [Kubernetes](#kubernetes)
  - [Prometheus](#prometheus)
  - [Zookeeper](#zookeeper)
- Databases
  - [How to configure PostgreSQL](#how-to-configure-postgresql)
  - [How to configure PostgreSQL replication](#how-to-configure-postgresql-replication)


## Prerequisites to run Epiphany engine

### Run directly from OS

To be able to run the Epiphany engine from your local OS you have to install:

- Bash 4.4+
  - Should be natively installed on Linux distributions.
  - MacOS version of bash most likely needs upgrading.
  - For Windows 10 you can install Ubuntu subsystem.
  - For Windows 7 see the docker image options below.
- Ansible 2.6+
- Hashicorp Terraform 0.11.8+
- jq (JSON Query tool: <https://stedolan.github.io/jq/download>)
- Python 2.7
  - jinja2 2.10+
  - jmespath 0.9.3+
- Git
- Azure CLI 2.0+
- SSH

This can both be used for deploying/managing clusters or for development.

### Run with Docker image for development

To facilitate an easier path for developers to contribute to Epiphany we have a development docker image based on alpine. This image will help to more easily setup a development environment or to develop on systems which do not support Bash like Windows 7.

The following prerequisites are needed when working with the development image:

- Docker <https://www.docker.com>
  - For Windows 7 check [here](https://docs.docker.com/toolbox/toolbox_install_windows)
- Git <https://git-scm.com>

There are 2 ways to get the image, build it localy yourself or pull it from the Epiphany docker registry.

#### To build it locally and run it:

1. Run the following to build the image locally:

    ```bash
    docker build -t epiphany-dev -f core/src/docker/dev/Dockerfile .
    ```

2. To run the locally build image in a container use:

    ```bash
    docker run -it -v LOCAL_DEV_DIR:/epiphany --rm epiphany-dev
    ```
    
    Where `LOCAL_DEV_DIR` should be replaced with the local path to your core and data repositories. This will then be mapped to `epiphany` inside the container. If everything is ok you will be presented with a Bash prompt from which one can run the Epiphany engine. Note that when filling in your data YAMLs one needs to specify the paths from the container's point of view.

#### To get it from the registry and run it:

1. Pull down the image from the registry:

    ```bash
    docker pull epiphanyplatform/epiphany-dev
    ```

2. To run the pulled image in a container use:

    ```bash
    docker run -it -v LOCAL_DEV_DIR:/epiphany --rm epiphanyplatform/epiphany-dev
    ```

    Where `LOCAL_DEV_DIR` should be replaced with the local path to your local Epiphany repo. This will then be mapped to `epiphany` inside the container. If everything is ok you will be presented with a Bash prompt from which one can run the Epiphany engine while editing the core and data sources on the local OS. Note that when filling in your data YAMLs one needs to specify the paths from the container's point of view.

### Run with Docker image for deployment

For people who are only using the Epiphany engine to deploy and maintain clusters there is a Dockerfile for the image with the engine already embedded.

To get it from the registry and run it:

1. Build an dev image described [here](#run-with-docker-image-for-development).
2. Run the following command to build the deployment image locally:
    ```bash
    docker build -t epiphany-deploy -f core/core/src/docker/deploy/Dockerfile .
    ```
3. To run the pulled image in a container use:
    ```bash
    docker run -it -v LOCAL_DATA_DIR:/epiphany/core/data \
                   -v LOCAL_BUILD_DIR:/epiphany/core/build \
                   -v LOCAL_SSH_DIR:/epiphany/core/ssh \
                   --rm epiphany-deploy
    ```

```LOCAL_DATA_DIR``` should be the host input directy for your data YAMLs and certificates.  ```LOCAL_BUILD_DIR``` should be the host directory where you want the Epiphany engine to write its build output. ```LOCAL_SSH_DIR``` should be the host directory where the SSH keys are stored. If everything is ok you will be presented with a Bash prompt from which one can run the Epiphany engine. Note that when filling in your data YAMLs one needs to specify the paths from the container's point of view.

[`Azure specific`] Ensure that you have already enough resources/quotas accessible in your region/subscription on Azure before you run Epiphany - depending on your configuration it can create large number of resources.

### Note for Windows users

- Watch out for the line endings conversion. By default Git for Windows sets `core.autocrlf=true`. Mounting such files with Docker results in `^M` end-of-line character in the config files.
Use: [Checkout as-is, commit Unix-style](https://stackoverflow.com/questions/10418975/how-to-change-line-ending-settings) (`core.autocrlf=input`) or Checkout as-is, commit as-is (`core.autocrlf=false`). Be sure to use a text editor that can work with Unix line endings (e.g. Notepad++). 

- Remember to allow Docker Desktop to mount drives in Settings -> Shared Drives

- Escape your paths properly:

  * Powershell example:
  ```bash
  docker run -it -v C:\Users\USERNAME\git\epiphany:/epiphany --rm epiphany-dev
  ```
  * Git-Bash example:
  ```bash
  winpty docker run -it -v C:\\Users\\USERNAME\\git\\epiphany:/epiphany --rm epiphany-dev
  ```

- Mounting NTFS disk folders in a linux based image causes permission issues with SSH keys. When running either the development or deploy image:

1. Copy the certs on the image:

    ```bash
    mkdir -p ~/.ssh/epiphany-operations/
    cp /epiphany/core/ssh/id_rsa* ~/.ssh/epiphany-operations/
    ```
2. Set the propper permission on the certs:

    ```bash
    chmod 400 ~/.ssh/epiphany-operations/id_rsa*
    ```

## Import and create of Grafana dashboards

Epiphany uses Grafana for monitoring data visualization. Epiphany installation creates Prometheus datasource in Grafana, so the only additional step you have to do is to create your dashboard.

### Creating dashboards

You can create your own dashboards [Grafana getting started](http://docs.grafana.org/guides/getting_started/) page will help you with it.
Knowledge of Prometheus will be really helpful when creating diagrams since it use [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) to fetch data.

### Importing dashboards

There are also many ready to take [Grafana dashboards](https://grafana.com/dashboards) created by community - remember to check license before importing any of those dashboards.
To import existing dashboard:

1. If you have found dashboard that suits your needs you can import it directly to Grafana going to menu item `Dashboards/Manage` in your Grafana web page.
2. Click `+Import` button.
3. Enter dashboard id or load json file with dashboard definition
4. Select datasource for dashboard - you should select `Prometheus`.
5. Click `Import`

### How to configure PostgreSQL

To configure PostgreSQL login to server using ssh and switch to postgres user with command:

```bash
sudo -u postgres -i
```

And then configure database server using psql according to your needs and
PostgreSQL documentation, to which link you can find at <https://www.postgresql.org/docs/>

### How to configure PostgreSQL replication

In order to configure PostgreSQL replication add to your data.yaml a block similar to the one below to core section:

```yaml
  postgresql:
    replication:
      enable: yes
      user: your-postgresql-replication-user
      password: your-postgresql-replication-password
      max_wal_senders: 10 # (optional) - default value 5
      wal_keep_segments: 34 # (optional) - default value 32
```
If enable is set to yes in replication then Epiphany will automatically create cluster of master and slave server with replication user with name and password
specified in data.yaml.

### Components used for monitoring

There are many monitoring components deployed with Epiphany that you can visualize data from. The knowledge which components are used is important when you look for appropriate dashboard on Grafana website or creating your own query to Prometheus.

List of monitoring components - so called exporters:

- cAdvisor
- HAProxy Exporter
- JMX Exporter
- Kafka Exporter
- Node Exporter
- Zookeeper Exporter

When dashboard creation or import succeeds you will see it on your dashboard list.

## How to configure Kibana

In order to start viewing and analyzing logs with Kibana, you first need to add an index pattern for Filebeat according to the following steps:

1. Goto the `Management` tab
2. Select `Index Patterns`
3. On the first step define as index pattern:
    `filebeat-*`
    Click next.
4. Configure the time filter field if desired by selecting `@timestamp`. This field represents the time that events occurred or were processed. You can choose not to have a time field, but you will not be able to narrow down your data by a time range.

This filter pattern can now be used to query the Elasticsearch indices.

By default Kibana adjusts the UTC time in `@timestamp` to the browser's local timezone. This can be changed in `Management` > `Advanced Settings` > `Timezone for date formatting`.

## How to configure Prometheus alerts

In order to send messages from Prometheus add monitoring block to your data.yaml similar to the one below:

```yaml
  monitoring:
    alerts:
      enable: true
      handlers:
        mail:
          smtp_from: 'some-sender@example.com'
          smtp_host: 'somesmtp.example.com:587'
          smtp_auth_username: 'someusername'
          smtp_auth_password: 'somepassword'
          smtp_require_tls: true
          recipients: ['recipient1@example.com', 'recipient2@example.com']
      rules:
      - name: "disk"
        expression: ((node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes) < 99
        duration: 1m #1s, 1m, 1h, 1d, 1w, ...
        severity: critical
        message: "Disk space Exceeded"
      - name: "updown"
        expression: up == 0
        duration: 1m #1s, 1m, 1h, 1d, 1w, ...
        severity: critical
        message: "Instance down"
```

    monitoring: - this covers whole monitoring section and is needed to define alerts
      alerts: - this covers whole alerts section and is needed to define alerts
        enable: true - global switch to turn off/on alerts. Set to true enable alerts.
        handlers: - this section covers email handlers, right now only email is supported
          mail: - global configuration for smtp and email
            smtp_from: 'some-sender@example.com' - name of email sender
            smtp_host: 'somesmtp.example.com:port' - address of your smtp server with port
            smtp_auth_username: 'someusername' - name of your smtp server username
            smtp_auth_password: 'somepassword' - password for your smtp server user
            smtp_require_tls: true - enabling/disabling tls. Set to true to enable TLS support.
            recipients: ['recipient1@example.com', 'recipient2@example.com'] - list of recipients in form
             ['recipient1@example.com', 'recipient2@example.com']. At least one recipient has to be declared.
        rules: - this section covers rules for Prometheus to enable monitoring. Each of rule have to follow pattern defined below.
        - name: "disk" - name of file for Prometheus where rule will be stored. Permitted are alphanumerical characters only.
          expression: ((node_filesystem_avail_bytes * 100) / node_filesystem_size_bytes) < 99 - rule in format of Prometheus queries
          duration: 1m #1s, 1m, 1h, 1d, 1w, ... - duration of event after which notification will be sent, follow Prometheus convention
          severity: critical - severity label, that will be showed in email sent to users
          message: "Disk space Exceeded" - email topic that will be showed in email sent to users

More information about Prometheus queries you can find under links provided below:

https://prometheus.io/docs/prometheus/latest/querying/basics/

https://prometheus.io/docs/prometheus/latest/querying/examples/

Right now we are only supporting email messages, but we are working heavily on introducing integration with Slack and Pager Duty.

## How to configure scalable Prometheus setup

If you want to create scalable Prometheus setup you can use federation. Federation lets you scrape metrics from different Prometheus
instances on one Prometheus instance.

In order to create federation of Prometheus add to your configuration (for example to prometheus.yaml
file) of previously created Prometheus instance (on which you want to scrape data from other
Prometheus instances) to `scrape_configs` section:

```yaml
scrape_configs:
  - job_name: federate
    metrics_path: /federate
    params:
      'match[]':
        - '{job=~".+"}'
    honor_labels: true
    static_configs:
    - targets:
      - your-prometheus-endpoint1:9090
      - your-prometheus-endpoint2:9090
      - your-prometheus-endpoint3:9090
      ...
      - your-prometheus-endpointn:9090
```

To check if Prometheus from which you want to scrape data is accessible, you can use a command
like below (on Prometheus instance where you want to scrape data):

`curl -G --data-urlencode 'match[]={job=~".+"}' your-prometheus-endpoint:9090/federate`  

If everything is configured properly and Prometheus instance from which you want to gather data is up
and running, this should return the metrics from that instance.  

## How to configure Azure additional monitoring and alerting

Setting up addtional monitoring on Azure for redundancy is good practice and might catch issues the Epiphany monitoring might miss like:

- Azure issues and resource downtime
- Issues with the VM which runs the Epiphany monitoring and Alerting (Prometheus)

More information about Azure monitoring and alerting you can find under links provided below:

https://docs.microsoft.com/en-us/azure/azure-monitor/overview

https://docs.microsoft.com/en-us/azure/monitoring-and-diagnostics/monitoring-overview-alerts

## How to do Kubernetes RBAC

Kubernetes that comes with Epiphany has an admin account created, you should consider creating more roles and accounts - especially when having many deployments running on different namespaces.

To know more about RBAC in Kubernetes use this [link](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

## How to create an Epiphany cluster on premise

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

## How to create an Epiphany cluster on Azure

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

## How to create production environment on Azure

Keep this in mind that Epiphany will create public IPs for each of the machines, you can remove it but running Epiphany again on the same cluster will recreate public IPs.

There are no manual steps required when you finished with [How to create an Epiphany cluster on Azure](#how-to-create-an-epiphany-cluster-on-azure) until you decide to move to `production environment` where cluster's virtual machines `must not` be exposed to internet (except load balancer - HAProxy role).

Production environment on cloud should be composed of two elements:

1. Demilitarized (`DMZ`) group that contains only load balancer (HAProxy role)
2. Applications (`APPS`) group that contains all other roles

Both elements are deployed independently (for now) that is why some manual steps, that will be described in this chapter, are required.

### 1. DMZ group

DMZ group should contain HAProxy role that is used for load balancing and TLS termination. VM that hosts HAProxy should be `the only one` accessible from internet. You can see DMZ implementation with VPN for Epiphany build cluster `repository_path/data/azure/infrastructure/epiphany-bld-dmz`.

### 2. APPS group

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

## How to run an example app

Here we will get a simple app to run using Docker through Kubernetes. We assume you are using Windows 10, have an Epiphany cluster on Azure ready and have an Azure Container Registry ready (might not be created in early version Epiphany clusters - if you don't have one you can skip to point no 11 and test the cluster using some public app from the original Docker Registry). Steps with asterisk can be skipped.

1. Install [Chocolatey](https://chocolatey.org/install)

2. Use Chocolatey to install:

    - Docker-for-windows (`choco install docker-for-windows`, requires Hyper-V)
    - Azure-cli (`choco install azure-cli`)

3. Make sure Docker for Windows is running (run as admin, might require a restart)

4. Run `docker build -t sample-app:v1 .` in examples/dotnet/epiphany-web-app.

5. *For test purposes, run your image locally with `docker run -d -p 8080:80 --name myapp sample-app:v1` and head to `localhost:8080` to check if it's working.

6. *Stop your local docker container with: `docker stop myapp` and run `docker rm myapp` to delete the container.

7. *Now that you have a working docker image we can proceed to the deployment of the app on the Epiphany Kubernetes cluster.

8. Run `docker login myregistry.azurecr.io -u myUsername -p myPassword` to login into your Azure Container Registry. Credentials are in the `Access keys` tab in your registry.

9. Tag your image with: `docker tag sample-app:v1 myregistry.azurecr.io/samples/sample-app:v1`

10. Push your image to the repo: `docker push myregistry.azurecr.io/samples/sample-app:v1`

11. SSH into your Epiphany clusters master node.

12. *Run `kubectl cluster-info` and `kubectl config view` to check if everything is okay.

13. Run `kubectl create secret docker-registry myregistry --docker-server myregistry.azurecr.io --docker-username myusername --docker-password mypassword` to create k8s secret with your registry data.

14. Create `sample-app.yaml` file with contents:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: sample-app
    spec:
      selector:
        matchLabels:
          app: sample-app
      replicas: 2
      template:
        metadata:
          labels:
            app: sample-app
        spec:
          containers:
          - name: sample-app
            image: myregistry.azurecr.io/samples/sample-app:v1
            ports:
            - containerPort: 80
            resources:
              requests:
                cpu: 100m
                memory: 64Mi
              limits:
                memory: 128Mi
          imagePullSecrets:
          - name: myregistry
    ```

15. Run `kubectl apply -f sample-app.yaml`, and after a minute run `kubectl get pods` to see if it works.

16. Run `kubectl expose deployment sample-app --type=NodePort --name=sample-app-nodeport`, then run `kubectl get svc sample-app-nodeport` and note the second port.

17. Run `kubectl get pods -o wide` and check on which node is the app running.

18. Access the app through [AZURE_NODE_VM_IP]:[PORT] from the two previous points - firewall changes might be needed.

## How to set resource requests and limits for Containers

When Kubernetes schedules a Pod, it’s important that the Containers have enough resources to actually run. If you schedule a large application on a node with limited resources, it is possible for the node to run out of memory or CPU resources and for things to stop working! It’s also possible for applications to take up more resources than they should.

When you specify a Pod, it is strongly recommended to specify how much CPU and memory (RAM) each Container needs. Requests are what the Container is guaranteed to get. If a Container requests a resource, Kubernetes will only schedule it on a node that can give it that resource. Limits make sure a Container never goes above a certain value. For more details about the difference between requests and limits, see [Resource QoS](https://git.k8s.io/community/contributors/design-proposals/node/resource-qos.md).

For more information, see the links below:

- [Kubernetes best practices: Resource requests and limits](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-resource-requests-and-limits)
- [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)

## How to run CronJobs

1. Follow the previous point using examples/dotnet/Epiaphany.SampleApps/Epiphany.SampleApps.CronApp

2. Create `cronjob.yaml` file with contents:

    ```yaml
    apiVersion: batch/v1beta1
    kind: CronJob
    metadata:
      name: sample-cron-job
    spec:
      schedule: "*/1 * * * *"   # Run once a minute
      failedJobsHistoryLimit: 5
      jobTemplate:
        spec:
          template:
            spec:
              containers:
              - name: sample-cron-job
                image: myregistry.azurecr.io/samples/sample-cron-app:v1
              restartPolicy: OnFailure
              imagePullSecrets:
              - name: myregistrysecret
    ```

3. Run `kubectl apply -f cronjob.yaml`, and after a minute run `kubectl get pods` to see if it works.

4. Run `kubectl get cronjob sample-cron-job` to get status of our cron job.

5. Run `kubectl get jobs --watch` to see job scheduled by the “sample-cron-job” cron job.

## How to test the monitoring features

Prerequisites: Epiphany cluster on Azure with at least a single VM with `prometheus` and `grafana` roles enabled.

1. Copy ansible inventory from `build/epiphany/*/inventory/` to `examples/monitoring/`

2. Run `ansible-playbook -i NAME_OF_THE_INVENTORY_FILE grafana.yml` in `examples/monitoring`

3. In the inventory file find the IP adress of the node of the machine that has grafana installed and head over to `https://NODE_IP:3000` - you might have to head over to Portal Azure and allow traffic to that port in the firewall, also ignore the possible certificate error in your browser.

4. Head to `Dashboards/Manage` on the side panel and select `Kubernetes Deployment metrics` - here you can see a sample kubernetes monitoring dashboard.

5. Head to `http://NODE_IP:9090` to see Prometheus UI - there in the dropdown you have all of the metrics you can monitor with Prometheus/Grafana.

## How to run chaos on Epiphany Kubernetes cluster and monitor it with Grafana

1. SSH into the Kubernetes master.

2. Copy over `chaos-sample.yaml` file from the example folder and run it with `kubectl apply -f chaos-sample.yaml` - it takes code from `github.com/linki/chaoskube` so normal security concerns apply.

3. Run `kubectl create clusterrolebinding chaos --clusterrole=cluster-admin --user=system:serviceaccount:default:default` to start the chaos - random pods will be terminated with 5s ferquency, configurable inside the yaml file.

4. Head over to Grafana at `https://NODE_IP:3000`, open a new dashboard, add a panel, set Prometheus as a data source and put `kubelet_running_pod_count` in the query field - now you can see how Kubernetes is replacing killed pods and balancing them between the nodes.

5. Run `kubectl get svc nginx-service` and note the second port. You can access the nginx page via `[ANY_CLUSTER_VM_IP]:[PORT]` - it is accessible even though random pods carrying it are constantly killed at random, unless you have more vms in your cluster than deployed nginx instances and choose IP of one not carrying it.

## How to test the central logging features

Prerequisites: Epiphany cluster on Azure with at least a single VM with `elasticsearch`, `kibana` and `filebeat` roles enabled.

1. Connect to kubectl using kubectl proxy or directly from Kubernetes master server

2. Apply from epiphany repository `extras/kubernetes/pod-counter` `pod-counter.yaml` with command: `kubectl apply -f yourpath_to_pod_counter/pod-counter.yaml`

    Paths are system dependend so please be aware of applying correct separator for your operatins system.

3. In the inventory file find the IP adress of the node of the machine that has kibana installed and head over to `http://NODE_IP:5601` - you might have to head over to Portal Azure and allow traffic to that port in the firewall.

4. You can right now search for data from logs in Discover section in Kibana after creating filebeat-* index pattern. To create index pattern click Discover, then in Step 1: Define index pattern as filebeat-*. Then click Next step. In Step 2: Configure settings click Create index pattern. Right now you can go to Discover section and look at output from your logs.

5. You can verify if CounterPod is sending messages correctly and filebeat is gathering them correctly querying for `CounterPod` in search field in Discover section.

6. For more informations refer to documentation: <https://www.elastic.co/guide/en/kibana/current/index.html>

## How to tunnel kubernetes dashboard from remote kubectl to your PC

1. SSH into server, and forward port 8001 to your machine `ssh -i epi_keys/id_rsa operations@40.67.255.155 -L 8001:localhost:8001` NOTE: substitute IP with your cluster master's IP.

2. On **remote** host: get admin token bearer: `kubectl describe secret $(kubectl get secrets --namespace=kube-system | grep admin-user | awk '{print $1}') --namespace=kube-system | grep -E '^token' | awk '{print $2}' | head -1` NOTE: save this token for next points.

3. On **remote** host, open proxy to the dashboard `kubectl proxy`

4. Now on your **local** machine navigate to `http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/#!/overview?namespace=default`

5. When prompted to put in credentials, use admin token from the previous point.

## How to setup Azure VM as docker machine for development

0. Make sure you have docker-machine installed `(choco install docker-machine)`

1. Run the following:

    ```bash
    docker-machine create --driver azure --azure-subscription-id <visual-studio-subscription-id> --azure-resource-group <resource-group> --azure-vnet <vnet> --azure-subnet default --azure-location westeurope <name-of-the-vm>
    ```

2. When the creation succeedes go ahead and connect to your docker-machine using `docker-machine env <name-of-the-vm>` and later invoke commands as instructed by docker-machine

3. Check if everything is working with `docker run hello-world`

Now your docker containers are running on a separate system without you having to worry about overhead.  
Source: <https://docs.docker.com/machine/drivers/azure/#options>

# How to use Kubernetes Secrets

Prerequisites: Epiphany Kubernetes cluster

1. SSH into the Kubernetes master.

2. Run `echo -n 'admin' > ./username.txt`, `echo -n 'VeryStrongPassword!!1' > ./password.txt` and  `kubectl create secret generic mysecret --from-file=./username.txt --from-file=./password.txt`

3. Copy over `secrets-sample.yaml` file from the example folder and run it with `kubectl apply -f secrets-sample.yaml`

4. Run `kubectl get pods`, copy the name of one of the ubuntu pods and run `kubectl exec -it POD_NAME -- /bin/bash` with it.

5. In the pods bash run `printenv | grep SECRET` - Kubernetes secret created in point 2 was attached to pods during creation (take a look at `secrets-sample.yaml`) and are availiable inside of them as an environmental variables.

## How to authenticate to Azure AD app

1. Register you application. Go to Azure portal to `Azure Active Directory => App registrations` tab.

2. Click button `New application registration` fill the data and confirm.

3. Deploy app from `examples/dotnet/Epiphany.SampleApps/Epiphany.SampleApps.AuthService`.

    This is a test service for verification Azure AD authentication of registered app. ([How to deploy app](#how-to-run-an-example-app))

4. Create secret key for your app `settings => keys`. Remember to copy value of key after creation.

5. Try to authenticate (e.g. using postman) calling service api `<service-url>/api/auth/` with following Body application/json type parameters :

    ```json
    {
      "TenantId": "<tenant-id>",
      "ClientId": "<client-id>",
      "Resource": "https://graph.windows.net/",
      "ClientSecret": "<client-secret>"
    }
    ```

    - TenantId - Directory ID, which you find in `Azure active Directory => Properties` tab.

    - ClientId - Application ID, which you find in details of previously registered app `Azure Active Directory => App registrations => your app`

    - Resource - <https://graph.windows.net> is the service root of Azure AD Graph API. The Azure Active Directory (AD) Graph API provides programmatic access to Azure AD through OData REST API endpoints. You can construct your own Graph API URL. ([How to construct a Graph API URL](https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-graph-api-quickstart))

    - ClientSecret - Created secret key from 4. point.

6. The service should return Access Token.

## How to expose service through HA Proxy load balancer

1. Add haproxy role to your data.yaml
2. Create a folder repository_path/core/src/ansible/roles/haproxy/vars/
3. Create a file repository_path/core/src/ansible/roles/haproxy/vars/main.yml:
4. Add to repository_path/core/src/ansible/roles/haproxy/vars/main.yml content:

    ```yaml
    ---
    service_port: your_service_port
    ```

    Where `your_service_port` is a port where your service is exposed using NodePort.

## How to set HA Proxy load balancer to minimize risk of Slowloris like attacks

1. Add haproxy_tls_termination role to your data.yaml
2. If you want to minimize risk of Slowloris like attacks add to your data.yaml in section for haproxy:

    ```yaml
      haproxy:
        http_request_timeout: 5s
    ```

    Where http_request_timeout is the number_of_seconds with s after which connection to HAProxy will be terminated by HAProxy.
    This parameter is optional, if is not present no timeout http-request in global section of HAProxy configuration will be set.

## How to use TLS/SSL certificate with HA Proxy

If you want to use HAProxy with TLS/SSL certificate follow the instruction below.

1. Add haproxy_tls_termination role to your data.yaml
2. If you want to use your certificates, you can add to section core to your data.yaml:

    ```yaml
      haproxy:
        haproxy_certs_dir: your_path_to_certificates
    ```

    Your certificates will be copied and applied automatically to HA Proxy configuration.

    Please be aware that `your_path_to_certificates` cannot contain variables (`$HOME`) or tilde (`~`) as this will make deployment of Epiphany fail. Additionally if you need more than one DNS name for your frontend you need to provide certificates on your own, as there is only one self-signed certificate generated by this role with CN localhost. For multiple backends you need to provide also mapping as described in later part of this document.

3. If you don't want to apply your certificates that will be generated automatically, then just don't put any certificate in `your_path_to_certificates` or don't put section with `haproxy: haproxy_certs_dir` in your data.yaml

4. Below you can find example of configuration:
    ```yaml
    haproxy:
      haproxy_certs_dir: /home/epiphany/certs/
      frontend:
        - name: https_front
          port: 443
          https: yes
          backend:
          - http_back1
          - http_back2
          domain_backend_mapping:
            - domain: backend1.domain.com
              backend: http_back1
            - domain: backend2.domain.com
              backend: http_back2
        - name: http_front1
          port: 80
          https: no
          backend:
          - http_back2
        - name: http_front2
          port: 8080
          https: no
          backend:
          - http_back1
          - http_back2
          domain_backend_mapping:
            - domain: http-backend1.domain.com
              backend: http_back1
            - domain: http-backend2.domain.com
              backend: http_back2
      backend:
        - name: http_back1
          server_groups:
          - worker
          port: 30001
        - name: http_back2
          server_groups:
          - worker
          - kibana
          port: 30002
    ```

5. Parameters description:

    `haproxy_certs_dir` - (Optional) Path on machine from which you run Epiphany installer where certificates generated by you are stored. If not one certificate with CN localhost will be generated, works only with one frontend definition, in other cases it won't be able to redirect you to correct backend on HAProxy.

    `frontend` - (Mandatory) At least one frontend configuration must exist, if more than one domain must be supported than `domain_backend_mapping` section is mandatory, as this will make fail. This is a list of frontend, each position has to start with `-`.

      - `name` - (Mandatory) Name of each configuration for frontend.
      - `port` - (Mandatory) Port to which frontend should be binding. Must be unique for all frontends in other case it will make HAProxy fail.
      - `https` - (Mandatory) Information if https will be used - options `yes`/`no`. If `no`, only http part of configuration for frontend will be generated.
      - `backend` - (Mandatory) At least one backend configuration must exist. If `domain_backend_mapping` exists this must match configuration in `domain_backend_mapping` backend section. It always has to match configuration from backend name section. This is a list of backend, each position has to start with `-`. This parameter shows to which backend configuration forward traffic from frontend to backend.

      - `domain_backend_mapping` - (Optional) If this exist at least one domain to backend mapping must exist. Must be provided if more than one domain has to be supported.

          - `domain` - (Mandatory if `domain_backend_mapping` used for each mapping) Domain that matches SSL certificate CN for https configuration and domain name. For http, domain that will be mapped using http header.
          - `backend` - (Mandatory if `domain_backend_mapping` used for each mapping) Must match name from backend section

    `backend` - (Mandatory) This is a list of backend, each position has to start with `-`. At least one backend used by frontend must exist. If there won't be a match with each frontend configuration HAProxy will fail to start.
      - `name` - (Mandatory) Name of each configuration for backend, must match frontend backend configuration and `domain_backend_mapping` backend part in frontend section.
      - `server_groups` - (Mandatory) This is a list of server groups, each position has to start with `-`. At least one `server_group` used by backend must exist. It must match Epiphany role e.g. `kibana`, `worker` etc.
      - `port` - (Mandatory) Port on which backend service is exposed.

## How to upgrade Kubernetes cluster

Upgrade procedure might be different for each Kubernetes version. Upgrade shall be done only from one minor version to next minor version. For example, upgrade from 1.9 to 1.11 looks like this:

```text
1.9.x -> 1.9.y
1.9.y -> 1.10
1.10  -> 1.11
```

Each version can be upgraded in a bit different way, to find information how to upgrade your version of Kubernetes please use this [guide](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/#kubeadm-upgrade-guidance).

Epiphany uses kubeadm to boostrap a cluster and the same tool is also used to upgrade it.

Upgrading Kubernetes cluster with running applications shall be done step by step. To prevent your applications downtime you should use at least **two Kubernetes worker nodes** and at least **two instances of each of your service**.

Start cluster upgrade with upgrading master node. Detailed instructions how to upgrade each node, including master, are described in guide linked above. When Kubernetes master is down it does not affect running applications, at this time only control plane is not operating. **Your services will be running but will not be recreated nor scaled when control plane is down.**

Once master upgrade finished successfully, you shall start upgrading nodes - **one by one**. Kubernetes master will notice when worker node is down and it will instatiate services on existing operating node, that is why it is essential to have more than one worker node in cluster to minimize applications downtime.

## How to upgrade Kubernetes cluster from 1.13.0 to 1.13.1

Detailed instruction can be found in [Kubernetes upgrade to 1.13 documentation](https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade-1-13/)

### Ubuntu Server

#### Upgrade Master

```bash
# RUN ON MASTER

1. sudo kubeadm version # should show v1.13.0
2. sudo kubeadm upgrade plan v1.13.1

3. apt update
4. apt-cache policy kubeadm


5. sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm=1.13.1-00 && \
sudo apt-mark hold kubeadm

6. sudo kubeadm version # should show v1.13.1
7. sudo kubeadm upgrade plan v1.13.1

8. sudo kubeadm upgrade apply v1.13.1

9. sudo apt-mark unhold kubelet && \
sudo apt-get update && sudo apt-get install -y kubelet=1.13.1-00 && \
sudo apt-mark hold kubelet
```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Worker nodes will be upgraded one by one - it will prevent application downtime.

```bash

# RUN ON WORKER NODE - $NODE

1. sudo apt-mark unhold kubectl && \
sudo apt-get update && sudo apt-get install -y kubectl=1.13.1-00 && \
sudo apt-mark hold kubectl

# RUN ON MASTER

2. kubectl drain $NODE --ignore-daemonsets

# RUN ON WORKER NODE - $NODE

3. sudo kubeadm upgrade node config --kubelet-version v1.13.1

4. sudo apt-get update
5. sudo apt-get install -y kubelet=1.13.1-00 kubeadm=1.13.1-00

6. sudo systemctl restart kubelet
7. sudo systemctl status kubelet # should be running

# RUN ON MASTER

8. kubectl uncordon $NODE

9. # go to 1. for next node

# RUN ON MASTER
10. kubectl get nodes # should return nodes in status "Ready" and version 1.13.1

```

### RHEL

#### Upgrade Docker version

Upgrading Kubernetes to 1.13.1 on RHEL requires Docker upgrade. Newer Docker packages exist in docker-ce repository but you can use newer Docker-ee if you need. Verified Docker versions for Kubernetes are: 1.11.1, 1.12.1, 1.13.1, 17.03, 17.06, 17.09, 18.06. [Go to K8s docs](https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG-1.13.md#external-dependencies)

```bash

# Remove previous docker version
1 sudo yum remove docker \
                  docker-common \
                  container-selinux \
                  docker-selinux \
                  docker-engine
2. sudo rm -rf /var/lib/docker
3. sudo rm -rf /run/docker
4. sudo rm -rf /var/run/docker
5. sudo rm -rf /etc/docker

# Add docker-ce repository
6. sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
7. sudo yum makecache fast
8. sudo yum -y install docker-ce-18.06.3.ce-3.el7

```

#### Upgrade Master

```bash
# RUN ON MASTER

1. sudo kubeadm version # should show v1.13.0
2. sudo kubeadm upgrade plan v1.13.1

3. sudo yum install -y kubeadm-1.13.1-0 --disableexcludes=kubernetes

4. sudo kubeadm version # should show v1.13.1
5. sudo kubeadm upgrade plan v1.13.1

6. sudo kubeadm upgrade apply v1.13.1

7. sudo yum install -y kubelet-1.13.1-0 --disableexcludes=kubernetes

```

#### Upgrade Worker Nodes

Commands below should be run in context of each node in the cluster. Variable `$NODE` represents node name (node names can be retrieved by command `kubectl get nodes` on master)

Worker nodes will be upgraded one by one - it will prevent application downtime.

```bash

# RUN ON WORKER NODE - $NODE

1. yum install -y kubectl-1.13.1-0 --disableexcludes=kubernetes

# RUN ON MASTER

2. kubectl drain $NODE --ignore-daemonsets

# RUN ON WORKER NODE - $NODE

3. # Upgrade Docker version using instruction from above

4. sudo kubeadm upgrade node config --kubelet-version v1.13.1

5. sudo yum install -y kubelet-1.13.1-0 kubeadm-1.13.1-0 --disableexcludes=kubernetes

6. sudo systemctl restart kubelet
7. sudo systemctl status kubelet # should be running

# RUN ON MASTER

8. kubectl uncordon $NODE

9. # go to 1. for next node

# RUN ON MASTER
10. kubectl get nodes # should return nodes in status "Ready" and version 1.13.1

```

## How to upgrade Kafka cluster

### Kafka upgrade

No downtime upgrades are possible to achieve when upgrading Kafka, but before you start thinking about upgrading you have to think about your topics configuration. Kafka topics are distributed accross partitions with replication. Default value for replication is 3, it means each partition will be replicated to 3 brokers. You should remember to enable redundancy and keep **at least two replicas all the time**, it is important when upgrading Kafka cluser. When one of your Kafka nodes will be down during upgrade ZooKeeper will direct your producers and consumers to working instances - having replicated partitions on working nodes will ensure no downtime and no data loss work.

Upgrading Kafka could be different for every Kafka release, please refer to [Apache Kafka documentation](https://kafka.apache.org/documentation/#upgrade). Important point to remember during Kafka upgrade is the rule: **only one broker at the time** - to prevent downtime you should uprage you Kafka brokers one by one.

### ZooKeeper upgrade

ZooKeeper redundancy is also recommended, since service restart is required during upgrade - it can cause ZooKeeper unavailability. Having at **least two ZooKeeper services** in *ZooKeepers ensemble* you can upgrade one and then start with the rest **one by one**.

More detailed information about ZooKeeper you can find in  [ZooKeeper documentation](https://cwiki.apache.org/confluence/display/ZOOKEEPER).

## How to enable or disable network traffic

### VM Firewall

Epiphany 1.0 supports firewalld on host machines (RedHat only). You can enable firewall setting `.../security/firewall/enable` to `true` in data.yaml. Remember to allow port 22 to be open in ports_open (`.../security/firewall/ports_open`) dictionary in order to configuration can do its job.

### Azure specific - Network Security Group

Security for internet facing infrastructure is extremely important thing - remember to configure `Network Security Group` rules to allow network traffic only on required ports and directions. You can do it using Azure specific data.yaml in section `.../network_security_group/rules`. Remember to allow port 22 (you can/should remove this rule after deployment) in order to configuration can do its job.

## Client certificate for Azure VPN connection

Epiphany will create point to site configuration (if you enable VPN in `.../security/vpn/enable` and specify public key of your certificate, in base64 format, in `public_cert_data` field). For production environments you have to use root certificate from `trusted provider`.
For development purposes you can use self signed certificate which can be generated using powershell: <https://docs.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-certificates-point-to-site>

When you get root certificate you should generate child certificate(s) that will be distributed to the team that should have VPN access to clusters.
Configuration of client config in data.yaml (`.../security/vpn/client_configuration/root_certificate`) looks like following:

```yaml
...
root_certificate:
  # name is the name of the cert that was created for you by a trusted party OR a name you give a self-signed cert
  name: NAME-OF-YOUR-CERTIFICATE
  revoked_certificate:
    name: NAME-OF-REVOKED-CERTIFICATE
    thumbprint: THUMBPRINT-OF-REVOKED-CERTIFICATE
  # public_cert_data is the actual base64 public key from your cert. Put it in 'as is'. The '|' tells yaml to use 'as is'.
  public_cert_data: |
    YOUR-BASE64-CLIENT-AUTH-PUBLIC-KEY
...
```

Configuration requires to have revoked certificate filled in (for now).

## Build artifacts

Epiphany engine produce build artifacts during each deployment. Those artifacts contains:

- Generated terraform files.
- Generated terraform state files.
- Generated cluster manifest file.
- Generated ansible files.
- Azure login credentials for `service principal` if deploying to Azure.

Artifacts contains sensitive data so it is important to keep it in safe place like `private GIT repository` or `storage with limited access`. Generated build is also important in case of scaling or updating cluster - you will it in build folder in order to edit your cluster.

Epiphany creates (or use if you don't specified it to create) service principal account which can manage all resources in subscription, please store build artifacts securely.

## How to scale Kubernetes and Kafka

### Scaling Kubernetes

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

### Scaling Kafka

Scaling Kafka looks exactly the same like scaling Kubernetes. Once changed `count:` property from `1` to `n` and executed Epiphany you will have `n` Kafka machines.

To add new Kafka broker to non-Azure deployment looks the same as adding new Kubernetes node.

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

To install RabbitMQ in single mode just add rabbitmq role to your data.yaml for your sever and in general roles section. All configuration on RabbitMQ - e.g. user other than guest creation should be performed manually.

## Single machine cluster

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

## Data and log retention

An Epiphany cluster has a number of components which log, collect and retain data. To make sure that these do not exceed the usable storage of the machines there running on the following configurations are available.

### Elasticsearch

For managing the data storage that Elasticsearch consumes we use [Elasticsearch Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.5/about.html). To use it one needs to make sure the elasticsearch-curator is enabled. This role will install and configure the [Elasticsearch Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.5/about.html) to run in a cronjob to clean up older indices which are older then a certain treshold.

In the default configuration `/core/src/ansible/roles/elasticsearch-curator/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# Rentention time of Elasticsearch indices in days.
indices_retention_days: 30
```

The size of the storage consumed by Elasticsearch is depenedant on the clustersize and how much logging the deployed application will generate.

### Grafana

In the default configuration `/core/src/ansible/roles/grafana/defaults/main.yml` the following values can be tweaked to control the ammount of storage used by Grafana:

```yaml
# The path where Grafana stores its logs
grafana_logs_dir: "/var/log/grafana"

# The path where Grafana stores it's (Dashboards DB (SQLLite), sessions, etc)
grafana_data_dir: "/var/lib/grafana"

grafana_logging:
# Enable or disable log rotation
log_rotate: true

# Enable or disable daily log rotation
daily_rotate: true

# Number of days to retain the logs
max_days: 7
```

While logs can be rotated and have a retention time, the ammount of storage used by Grafana is dependant on user usage and dashboard count and cannot be directly controlled.

### Kafka

In the default configuration `/core/src/ansible/roles/kafka/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where kafka stores its data
data_dir: /var/lib/kafka

# The path where kafka stores its logs
log_dir: /var/log/kafka

# The minimum age of a log file to be eligible for deletion due to age
log_retention_hours: 168

# Offsets older than this retention period will be discarded
offset_retention_minutes: 10080
```

The ammount of storage Kafka consumes is dependant on the application running on Epiphany, how many messages producers create and how fast the consumers can consume them. It's up to the application developer to configure a `log_retention_hours` and `offset_retention_minutes` to suite the applications need.

Since Kafka does not have a mechanism for log rotation we use [logrotate](https://linux.die.net/man/8/logrotate) for this. The template for logrotate can be found here:

`/core/src/ansible/roles/kafka/templates/logrotate.conf.j2`

On the system the configuration can be found here:

`/etc/logrotate.d/kafka`

### Kibana

In the default configuration `/core/src/ansible/roles/kibana/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where Kibana stores its logs
kibana_log_dir: /var/log/kibana
```

Since Kibana does not have a mechanism for log rotation we use [logrotate](https://linux.die.net/man/8/logrotate) for this. The template for logrotate can be found here:

`/core/src/ansible/roles/kibana/templates/logrotate.conf.j2`

On the system the configuration can be found here:

`/etc/logrotate.d/kibana`

Besides logs any other data is depenedant on user usage (Dashboards, queries etc). Kibana stores that kind of data in ElasticSearch under the `.kibana` index.

### Kubernetes

The kubelet and container runtime (Docker) do not run in containers. On machines with systemd they write to journald.

Everything a containerized application writes to stdout and stderr is redirected to the Docker logging driver (`json-file`), which is configured to rotate logs automatically.

In the default configuration `/core/src/ansible/roles/docker/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
docker_logging:
  log_opts:
    # The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g).
    max_file_size: "10m"
    # The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed.
    max_files: 2
```

On the system the configuration can be found here:

`/etc/docker/daemon.json`

### Prometheus

In the default configuration `/core/src/ansible/roles/prometheus/defaults/main.yml` the following values can be tweaked to control the amount of storage used by Prometheus:

```yaml
# The path where Prometheus stores its data
prometheus_db_dir: /var/lib/prometheus

# The time it will retain the data before it gets deleted
prometheus_storage_retention: "30d"

prometheus_global:
# The interval it will use to scrape the data from the sources
scrape_interval: 15s
```

The size of the data which Prometheus will scrape and retain is dependant on the cluster size (Kafka/Kubernetes nodes) and the scrape interval. The [Prometheus storage documentation](https://prometheus.io/docs/prometheus/latest/storage/) will help you determine how much data might be generated with a certain scrape interval and clustersize. This can then be used to determine a storage retention time in days. Note that one should not plan to use the entire disk space for data retention since it might also be used by other components like Grafana which might be deployed on the same system.

### Zookeeper

In the default configuration `core/src/ansible/roles/zookeeper/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where Zookeeper stores its logs
zookeeper_log_dir: /var/log/zookeeper

# The max size a logfile can have
zookeeper_rolling_log_file_max_size: 10MB

# How many logfiles can be retained before rolling over
zookeeper_max_rolling_log_file_count: 10
```
