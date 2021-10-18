# Kubernetes

## Supported CNI plugins

Epiphany supports following CNI plugins:

- [Flannel](https://github.com/flannel-io/flannel/blob/master/README.md)
- [Calico](https://docs.projectcalico.org/about/about-calico)
- [Canal](https://docs.projectcalico.org/getting-started/kubernetes/flannel/flannel)

Flannel is a default setting in Epiphany configuration.

---
**NOTE**

Calico is [not supported](https://docs.projectcalico.org/reference/public-cloud/azure) on Azure. To have an ability to
use network policies, use Canal.

---

Use the following configuration to set up an appropriate CNI plugin:

   ```yaml
    kind: configuration/kubernetes-master
    name: default
    specification:
    advanced:
      networking:
      plugin: flannel
   ```

## Kubernetes applications - overview

Currently, Epiphany provides the following predefined applications which may be deployed with epicli:

- ignite
- rabbitmq
- auth-service (Keycloak)
- pgpool
- pgbouncer
- istio

All of them
have [default configuration](https://github.com/epiphany-platform/epiphany/blob/develop/data/common/defaults/configuration/applications.yml)
. The common parameters are: name, enabled, namespace, image_path and use_local_image_registry.  
If you set `use_local_image_registry` to `false` in configuration manifest, you have to provide a valid docker image
path in `image_path`. Kubernetes will try to pull image from `image_path` value externally.  
To see what version of the application image is in local image registry please refer
to [components list](../COMPONENTS.md).

*Note: The above link points to develop branch. Please choose the right branch that suits to Epiphany version you are
using.*

## How to expose service through HA Proxy load balancer

1. Create `NodePort` service type for your application in Kubernetes.

2. Make sure your service has statically assigned `nodePort` (a number between 30000-32767), for example 31234. More
   info [here](https://kubernetes.io/docs/concepts/services-networking/service/#nodeport).

3. Add configuration document for `load_balancer`/`HAProxy` to your main config file.

   ```yaml
   kind: configuration/haproxy
   title: "HAProxy"
   name: haproxy
   specification:
     frontend:
       - name: https_front
         port: 443
         https: yes
         backend:
           - http_back1
     backend:
       - name: http_back1
         server_groups:
           - kubernetes_node
         port: 31234
   provider: <your-provider-here-replace-it>
   ```

4. Run `epicli apply`.

## How to do Kubernetes RBAC

Kubernetes that comes with Epiphany has an admin account created, you should consider creating more roles and accounts -
especially when having many deployments running on different namespaces.

To know more about RBAC in Kubernetes use this [link](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

## How to run an example app

Here we will get a simple app to run using Docker through Kubernetes. We assume you are using Windows 10, have an
Epiphany cluster on Azure ready and have an Azure Container Registry ready (might not be created in early version
Epiphany clusters. If you don't have one you can skip to point no 11 and test the cluster using some public app from the
original Docker Registry). Steps with asterisk can be skipped.

1. Install [Chocolatey](https://chocolatey.org/install)

2. Use Chocolatey to install:

    - Docker-for-windows (`choco install docker-for-windows`, requires Hyper-V)
    - Azure-cli (`choco install azure-cli`)

3. Make sure Docker for Windows is running (run as admin, might require a restart)

4. Run `docker build -t sample-app:v1 .`
   in [example](https://github.com/epiphany-platform/examples/tree/develop/dotnet/epiphany-web-app).

5. *For test purposes, run your image locally with `docker run -d -p 8080:80 --name myapp sample-app:v1` and head
   to `localhost:8080` to check if it's working.

6. *Stop your local docker container with: `docker stop myapp` and run `docker rm myapp` to delete the container.

7. *Now that you have a working docker image we can proceed to the deployment of the app on the Epiphany Kubernetes
   cluster.

8. Run `docker login myregistry.azurecr.io -u myUsername -p myPassword` to login into your Azure Container Registry.
   Credentials are in the `Access keys` tab in your registry.

9. Tag your image with: `docker tag sample-app:v1 myregistry.azurecr.io/samples/sample-app:v1`

10. Push your image to the repo: `docker push myregistry.azurecr.io/samples/sample-app:v1`

11. SSH into your Epiphany clusters master node.

12. *Run `kubectl cluster-info` and `kubectl config view` to check if everything is okay.

13.

Run `kubectl create secret docker-registry myregistry --docker-server myregistry.azurecr.io --docker-username myusername --docker-password mypassword`
to create k8s secret with your registry data.

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

16. Run `kubectl expose deployment sample-app --type=NodePort --name=sample-app-nodeport`, then
    run `kubectl get svc sample-app-nodeport` and note the second port.

17. Run `kubectl get pods -o wide` and check on which node is the app running.

18. Access the app through [AZURE_NODE_VM_IP]:[PORT] from the two previous points - firewall changes might be needed.

## How to set resource requests and limits for Containers

When Kubernetes schedules a Pod, it’s important that the Containers have enough resources to actually run. If you
schedule a large application on a node with limited resources, it is possible for the node to run out of memory or CPU
resources and for things to stop working! It’s also possible for applications to take up more resources than they
should.

When you specify a Pod, it is strongly recommended specifying how much CPU and memory (RAM) each Container needs.
Requests are what the Container is guaranteed to get. If a Container requests a resource, Kubernetes will only schedule
it on a node that can give it that resource. Limits make sure a Container never goes above a certain value. For more
details about the difference between requests and limits,
see [Resource QoS](https://git.k8s.io/community/contributors/design-proposals/node/resource-qos.md).

For more information, see the links below:

- [Kubernetes best practices: Resource requests and limits](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-resource-requests-and-limits)
- [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)

## How to run CronJobs

1. Follow the previous point
   using [example](https://github.com/epiphany-platform/examples/tree/develop/dotnet/Epiphany.SampleApps/Epiphany.SampleApps.CronApp)

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

1. Copy ansible inventory from `build/epiphany/*/inventory/`
   to [example](https://github.com/epiphany-platform/examples/tree/develop/monitoring) folder

2. Run `ansible-playbook -i NAME_OF_THE_INVENTORY_FILE grafana.yml`
   in [example](https://github.com/epiphany-platform/examples/tree/develop/monitoring) folder

3. In the inventory file find the IP address of the node of the machine that has grafana installed. Then head over
   to `https://NODE_IP:3000` - you might have to head over to Portal Azure and allow traffic to that port in the
   firewall, also ignore the possible certificate error in your browser.

4. Head to `Dashboards/Manage` on the side panel and select `Kubernetes Deployment metrics` - here you can see a sample
   kubernetes monitoring dashboard.

5. Head to `http://NODE_IP:9090` to see Prometheus UI - there in the dropdown you have all the metrics you can monitor
   with Prometheus/Grafana.

## How to run chaos on Epiphany Kubernetes cluster and monitor it with Grafana

1. SSH into the Kubernetes master.

2. Copy over `chaos-sample.yaml` file from the example folder and run it with `kubectl apply -f chaos-sample.yaml` - it
   takes code from `github.com/linki/chaoskube` so normal security concerns apply.

3.

Run `kubectl create clusterrolebinding chaos --clusterrole=cluster-admin --user=system:serviceaccount:default:default`
to start the chaos - random pods will be terminated with 5s frequency, configurable inside the yaml file.

4. Head over to Grafana at `https://NODE_IP:3000`, open a new dashboard, add a panel, set Prometheus as a data source
   and put `kubelet_running_pod_count` in the query field. Now you can see how Kubernetes is replacing killed pods and
   balancing them between the nodes.

5. Run `kubectl get svc nginx-service` and note the second port. You can access the nginx page
   via `[ANY_CLUSTER_VM_IP]:[PORT]`. It is accessible even though random pods carrying it are constantly killed at
   random, unless you have more vms in your cluster than deployed nginx instances and choose IP of one not carrying it.

## How to test the central logging features

Prerequisites: Epiphany cluster on Azure with at least a single VM with `elasticsearch`, `kibana` and `filebeat` roles
enabled.

1. Connect to kubectl using kubectl proxy or directly from Kubernetes master server

2. Apply from epiphany repository `extras/kubernetes/pod-counter` `pod-counter.yaml` with
   command: `kubectl apply -f yourpath_to_pod_counter/pod-counter.yaml`

   Paths are system dependent so please be aware of applying correct separator for your operating system.

3. In the inventory file find the IP address of the node of the machine that has kibana installed and head over
   to `http://NODE_IP:5601`. You might have to head over to Portal Azure and allow traffic to that port in the firewall.

4. You can right now search for data from logs in Discover section in Kibana after creating filebeat-* index pattern. To
   create index pattern click Discover, then in Step 1: Define index pattern as filebeat-*. Then click Next step. In
   Step 2: Configure settings click Create index pattern. Right now you can go to Discover section and look at output
   from your logs.

5. You can verify if CounterPod is sending messages correctly and filebeat is gathering them correctly querying
   for `CounterPod` in search field in Discover section.

6. For more information refer to documentation: <https://www.elastic.co/guide/en/kibana/current/index.html>

## How to tunnel Kubernetes Dashboard from remote kubectl to your PC

1. SSH into server, and forward port 8001 to your
   machine `ssh -i epi_keys/id_rsa operations@40.67.255.155 -L 8001:localhost:8001` NOTE: substitute IP with your
   cluster master's IP.

2. On **remote** host: get admin token
   bearer: `kubectl describe secret $(kubectl get secrets --namespace=kube-system | grep admin-user | awk '{print $1}') --namespace=kube-system | grep -E '^token' | awk '{print $2}' | head -1`
   NOTE: save this token for next points.

3. On **remote** host, open proxy to the dashboard `kubectl proxy`

4. Now on your **local** machine navigate
   to `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`

5. When prompted to put in credentials, use admin token from the previous point.

## How to run Keycloak on Kubernetes

1. Enable Kubernetes master & node, repository and postgresql components in initial configuration manifest (yaml) by
   increasing `count` value.

``` yaml
kind: epiphany-cluster
title: Epiphany cluster Config
provider: azure
name: default
specification:
 components:
    repository:
      count: 1
    kubernetes_master:
      count: 1
    kubernetes_node:
      count: 2
    postgresql:
      count: 2
```

2. Enable `applications` in feature-mapping in initial configuration manifest.

``` yaml
---
kind: configuration/feature-mapping
title: Feature mapping to roles
name: default
specification:
  available_roles:
  - _merge: true
  - name: applications
    enabled: true
```

3. Enable required applications by setting `enabled: true` and adjust other parameters in `configuration/applications`
   kind.

The default applications configuration
available [here](https://github.com/epiphany-platform/epiphany/blob/develop/data/common/defaults/configuration/applications.yml)

Note: To get working with Pgbouncer, Keycloak requires Pgbouncer configuration parameter `POOL_MODE` set to `session`,
see [Installing Pgbouncer and Pgpool](DATABASES.md#installing-pgbouncer-and-pgpool) section. The reason is that Keycloak
uses SET SQL statements. For details see [SQL feature map for pooling modes](https://www.pgbouncer.org/features.html).

``` yaml
---
kind: configuration/applications
title: Kubernetes Applications Config
name: default
specification:
  applications:
  - _merge: true
  - name: auth-service
    enabled: true
    image_path: epiphanyplatform/keycloak:14.0.0
    use_local_image_registry: true
    service:
      name: as-testauthdb
      port: 30104
      replicas: 2
      namespace: namespace-for-auth
      admin_user: auth-service-username
      admin_password: PASSWORD_TO_CHANGE
    database:
      name: auth-database-name
      user: auth-db-user
      password: PASSWORD_TO_CHANGE
```

To set specific database host IP address for Keycloak you have to provide additional parameter `address`:

``` yaml
    database:
      address: 10.0.0.2
```

Note: If `database address` is not specified, epicli assumes that database instance doesn't exist and will create it.

By default, if `database address` is not specified and if Postgres is HA mode, Keycloak uses PGBouncer ClusterIP service
name as database address.  
If Postgres is in standalone mode, and `database address` is not specified, then it uses first Postgres host address
from `inventory`.

4. Run `epicli apply` on your configuration manifest.

5. Log into GUI

Note: Accessing the Keycloak GUI depends on your configuration.

By default, Epiphany provides the following K8s Services for Keycloak: Headless and NodePort. The simplest way for
reaching GUI is to use ssh tunnel with forwarding NodePort.  
Example:  
`ssh -L 30104:localhost:30104 user@target_host -i ssh_key`

If you need your GUI accessible outside, you would have to change your firewall rules.

GUI should be reachable at: https://localhost:30104/auth
