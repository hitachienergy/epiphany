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
use network policies, choose Canal.

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

All of them have
[default configuration](https://github.com/epiphany-platform/epiphany/blob/develop/schema/common/defaults/configuration/applications.yml). The common parameters are: name, enabled, namespace, image_path and use_local_image_registry. If you
set `use_local_image_registry` to `false` in configuration manifest, you have to provide a valid docker image path
in `image_path`. Kubernetes will try to pull image from `image_path` value externally.  
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

## How to set resource requests and limits for Containers

When Kubernetes schedules a Pod, it’s important that the Containers have enough resources to actually run. If you
schedule a large application on a node with limited resources, it is possible for the node to run out of memory or CPU
resources and for things to stop working! It’s also possible for applications to take up more resources than they
should.

When you specify a Pod, it is strongly recommended specifying how much CPU and memory (RAM) each Container needs.
Requests are what the Container is guaranteed to get. If a Container requests a resource, Kubernetes will only schedule
it on a node that can give it that resource. Limits make sure a Container never goes above a certain value. For more
details about the difference between requests and limits,
see [Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits)

For more information, see the links below:

- [Kubernetes best practices: Resource requests and limits](https://cloud.google.com/blog/products/gcp/kubernetes-best-practices-resource-requests-and-limits)
- [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)

## How to tunnel Kubernetes Dashboard from remote kubectl to your PC

1. SSH into server, and forward port 8001 to your
   machine `ssh -i epi_keys/id_rsa operations@40.67.255.155 -L 8001:localhost:8001` NOTE: substitute IP with your
   cluster master's IP.

2. On **remote** host: get admin token
   bearer: `kubectl describe secret $(kubectl get secrets --namespace=kube-system | grep admin-token | awk '{print $1}') --namespace=kube-system | grep -E '^token' | awk '{print $2}' | head -1`
   NOTE: save this token for next points.

3. On **remote** host, open proxy to the dashboard `kubectl proxy`

4. Now on your **local** machine navigate
   to `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/`

5. When prompted to put in credentials, use admin token from the previous point.

## How to run Keycloak on Kubernetes

1. Enable Kubernetes master & node, repository and postgresql components in initial configuration manifest (yaml) by
   increasing `count` value.

```yaml
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

```yaml
---
kind: configuration/feature-mapping
title: Feature mapping to roles
name: default
specification:
  available_roles:
    - name: applications
      enabled: true
```

3. Enable required applications by setting `enabled: true` and adjust other parameters in `configuration/applications`
   kind.

The default applications configuration is
available [here](https://github.com/epiphany-platform/epiphany/blob/develop/schema/common/defaults/configuration/applications.yml)

Note: To get working with Pgbouncer, Keycloak requires Pgbouncer configuration parameter `POOL_MODE` set to `session`,
see [Installing Pgbouncer and Pgpool](DATABASES.md#installing-pgbouncer-and-pgpool) section. The reason is that Keycloak
uses SET SQL statements. For details see [SQL feature map for pooling modes](https://www.pgbouncer.org/features.html).

```yaml
---
kind: configuration/applications
title: Kubernetes Applications Config
name: default
specification:
  applications:
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

```yaml
database:
  address: 10.0.0.2
```

Note: If `database address` is not specified, epicli assumes that database instance doesn't exist and will create it.

By default, if `database address` is not specified and if Postgres is HA mode, Keycloak uses PGBouncer `ClusterIP`
service name as database address.  
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
