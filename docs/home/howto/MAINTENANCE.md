## Maintenance

### Verification of service state

This part of the documentations covers the topic how to check if each component is working properly.

#### - Kubernetes

Verify status of Kubernetes kubelet service with the command:

```shell
systemctl status kubelet
```

##### - kubectl

Check state of Kubernetes nodes using the `kubectl` command:

```shell
root@primary01:~# kubectl get nodes --kubeconfig=/etc/kubernetes/admin.conf
NAME                                         STATUS   ROLES                  AGE   VERSION
primary01                                    Ready    control-plane,master   23h   vx.xx.x
node01                                       Ready    <none>                 23h   vx.xx.x
node02                                       Ready    <none>                 23h   vx.xx.x
```

Get additional information about Kubernetes components:

```shell
root@primary01:~# kubectl cluster-info --kubeconfig=/etc/kubernetes/admin.conf
Kubernetes control plane is running at https://primary01:6443
CoreDNS is running at https://primary01:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

Check status of pods in all namespaces using the command:

```shell
kubectl get pods -A --kubeconfig=/etc/kubernetes/admin.conf
```

For more detailed information please refer
to [the official documentation](https://kubernetes.io/docs/reference/kubectl/overview/).

##### - crictl

You can also check state of Kubernetes components using the `crictl` command:

List all pods:

```shell
crictl pods
```

List all images:

```shell
crictl images
```

List all containers:

```shell
crictl ps -a
```

The crictl tool provides the possibility to run a sandbox container which may be useful for debugging purposes.
For more information, refer to [the official documentation](https://kubernetes.io/docs/tasks/debug-application-cluster/crictl).

#### - Keycloak

To check the if a Keycloak service deployed on Kubernetes is running with the command:

```shell
kubectl get pods --kubeconfig=/etc/kubernetes/admin.conf --namespace=keycloak_service_namespace --field-selector=status.phase=Running | grep keycloak_service_name
```

#### - HAProxy

To check status of HAProxy you can use the command:

```shell
systemctl status haproxy
```

Additionally, you can check if the application is listening on ports defined in the file haproxy.cfg running netstat
command.

#### - Prometheus

To check status of Prometheus you can use the command:

```shell
systemctl status prometheus
```

You can also check if Prometheus service is listening at the port 9090:

```shell
netstat -antup | grep 9090
```

#### - Grafana

To check status of Grafana you can use the command:

```shell
systemctl status grafana-server
```

You can also check if Grafana service is listening at the port 3000:

```shell
netstat -antup | grep 3000
```

#### - Prometheus Node Exporter

To check status of Node Exporter you can use the command:

```shell
status prometheus-node-exporter
```

#### - Elasticsearch

To check status of Elasticsearch you can use the command:

```shell
systemct status elasticsearch
```

You can check if service is listening on 9200 (API communication port):

```shell
netstat -antup | grep 9200
```

You can also check if service is listening on 9300 (nodes communication port):

```shell
netstat -antup | grep 9300
```

You can also check status of Elasticsearch cluster:

```shell
<IP>:9200/_cluster/health
```

You can do this using curl or any other equivalent tool.

#### - Kibana

To check status of Kibana you can use the command:

```shell
systemctl status kibana
```

You can also check if Kibana service is listening at the port 5601:

```shell
netstat -antup | grep 5601
```

#### - Filebeat

To check status of Filebeat you can use the command:

```shell
systemctl status filebeat
```

#### - PostgreSQL

To check status of PostgreSQL you can use commands:

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

You can also check if PostgreSQL service is listening at the port 5432:

```shell
netstat -antup | grep 5432
```

You can also use the pg_isready command, to get information if the PostgreSQL server is running and accepting connections
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
