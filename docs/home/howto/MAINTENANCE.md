## Maintenance

### Verification of service state

This part of the documentations covers the topic how to check if each component is working properly.

#### - Docker

To verify that Docker services are up and running you can first check the status of the Docker service with the
following command:

```shell
systemctl status docker
```

Additionally, you can check also if the command:

```shell
docker info
```

doesn't return any error. You can also find there useful information about your Docker configuration.

#### - Kubernetes

First to check if everything is working fine we need to check verify status of Kubernetes kubelet service with the
command:

```shell
systemctl status kubelet
```

We can also check state of Kubernetes nodes using the command:

```shell
root@primary01:~# kubectl get nodes --kubeconfig=/etc/kubernetes/admin.conf
NAME                                         STATUS   ROLES                  AGE   VERSION
primary01                                    Ready    control-plane,master   23h   vx.xx.x
node01                                       Ready    <none>                 23h   vx.xx.x
node02                                       Ready    <none>                 23h   vx.xx.x
```

We can get additional information about Kubernetes components:

```shell
root@primary01:~# kubectl cluster-info --kubeconfig=/etc/kubernetes/admin.conf
Kubernetes control plane is running at https://primary01:6443
CoreDNS is running at https://primary01:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

We can also check status of pods in all namespaces using the command:

```shell
kubectl get pods -A --kubeconfig=/etc/kubernetes/admin.conf
```

For more detailed information please refer
to [official documentation](https://kubernetes.io/docs/reference/kubectl/overview/)

#### - Keycloak

To check the if a Keycloak service deployed on Kubernetes is running with the command:

```shell
kubectl get pods --kubeconfig=/etc/kubernetes/admin.conf --namespace=keycloak_service_namespace --field-selector=status.phase=Running | grep keycloak_service_name
```

#### - HAProxy

To check status of HAProxy we can use the command:

```shell
systemctl status haproxy
```

Additionally, we can check if the application is listening on ports defined in the file haproxy.cfg running netstat
command.

#### - Prometheus

To check status of Prometheus we can use the command:

```shell
systemctl status prometheus
```

We can also check if Prometheus service is listening at the port 9090:

```shell
netstat -antup | grep 9090
```

#### - Grafana

To check status of Grafana we can use the command:

```shell
systemctl status grafana-server
```

We can also check if Grafana service is listening at the port 3000:

```shell
netstat -antup | grep 3000
```

#### - Prometheus Node Exporter

To check status of Node Exporter we can use the command:

```shell
status prometheus-node-exporter
```

#### - opensearch

To check status of Elasticsearch we can use the command:

```shell
systemct status opensearch
```

We can check if service is listening on 9200 (API communication port):

```shell
netstat -antup | grep 9200
```

We can also check if service is listening on 9300 (nodes communication port):

```shell
netstat -antup | grep 9300
```

We can also check status of Elasticsearch cluster:

```shell
<IP>:9200/_cluster/health
```

We can do this using curl or any other equivalent tool.

#### - Kibana

To check status of Kibana we can use the command:

```shell
systemctl status kibana
```

We can also check if Kibana service is listening at the port 5601:

```shell
netstat -antup | grep 5601
```

#### - Filebeat

To check status of Filebeat we can use the command:

```shell
systemctl status filebeat
```

#### - PostgreSQL

To check status of PostgreSQL we can use commands:

- on Ubuntu:

```shell
systemctl status postgresql
```

- on Red Hat:

```shell
systemctl status postgresql-10
```

where postgresql-10 is only an example, because the number differs from version to version. Please refer to your version
number in case of using this command.

We can also check if PostgreSQL service is listening at the port 5432:

```shell
netstat -antup | grep 5432
```

We can also use the pg_isready command, to get information if the PostgreSQL server is running and accepting connections
with command:

- on Ubuntu:

```shell
[user@postgres01 ~]$ pg_isready
/var/run/postgresql:5432 - accepting connections
```

- on Red Hat:

```shell
[user@postgres01 ~]$ /usr/pgsql-10/bin/pg_isready
/var/run/postgresql:5432 - accepting connections
```

where the path /usr/pgsql-10/bin/pg_isready is only an example, because the number differs from version to version.
Please refer to your version number in case of using this command.
