# Security related information

You are strongly advised use encrypted over unencrypted communication between Epiphany components where possible. Please consider
this during planning your Epiphany deployment and configuration.

## Contents

- [Users and roles created by Epiphany](#users-and-roles-created-by-epiphany)
- [Ports used by components in Epiphany](#ports-used-by-components-in-epiphany)

### Users and roles created by epiphany

By default Epiphany is creating user operations that is used to connect to machines with admin rights on every machine. This setting can be changed in Epiphany yaml configuration files.

Additional to users created by each component Epiphany creates also users and groups:

- haproxy_exporter/haproxy_exporter
- kafka_exporter/kafka_exporter
- node_exporter/node_exporter
- jmx-exporter/jmx-exporter
- prometheus/prometheus
- rabbitmq/rabbitmq
- zookeeper/zookeeper
- kafka/kafka
- vault/vault

Other accounts created by each component you can find in these components documentation.

### Ports used by components in Epiphany

Below you can find list of ports used by default in Epiphany on per component basis. Some of them can be changed to different values.
The list does not include ports that are bound to the loopback interface (localhost).

1. OS services:

    - 22 - SSH

2. Prometheus exporters:

    - 7071 - JMX Kafka exporter
    - 7072 - JMX Zookeeper exporter
    - 9100 - Node exporter
    - 9101 - HAProxy exporter
    - 9308 - Kafka exporter

3. Zookeeper:

    - 2181 - Zookeeper client connections
    - 2888 - Zookeeper peer to peer (follower to leader)
    - 3888 - Zookeeper peer to peer (for leader election)
    - unconfigurable random port from ephemeral range - JMX (for local access only), see note [[1]](#notes)

4. Kafka:

    - 9092 - Kafka broker
    - 9093 - encrypted communication (if TLS/SSL is enabled)
    - unconfigurable random port from ephemeral range - JMX (for local access only), see note [[1]](#notes)

5. Elasticsearch:

    - 9200 - Elasticsearch REST communication
    - 9300 - Elasticsearch nodes communication
    - 9600 - Performance Analyzer (REST API)

6. Kibana:

    - 5601 -  Kibana web UI

7. Prometheus:

    - 9090 - Prometheus server

8. Alertmanager:

    - 9093 - Alertmanager service

9. Grafana:

    - 3000 - Grafana web UI

10. RabbitMQ:

    - 4369 - peer discovery service (epmd)
    - 5671 - AMQP with TLS (if TLS is enabled)
    - 5672 - AMQP
    - 15672 - HTTP API clients, management UI and rabbitmqadmin
    - 25672 - distribution server

11. PostgreSQL:

    - 5432 - PostgreSQL server
    - 6432 - PgBouncer

12. Kubernetes:

    - 111/tcp - rpcbind (NFS)
    - 111/udp - rpcbind (+1 random UDP port, see note [[2]](#notes))
    - 179 - calico networking (BGP) [if Calico CNI plugin is used]
    - 6443 - kube-apiserver
    - 2379 - etcd server clients
    - 2380 - etcd server peers
    - 3446 - haproxy (when using HA control plane)
    - 8472/udp - flannel (vxlan backend) [if flannel or Canal CNI plugin is used]
    - 10250 - kubelet API
    - 10251 - kube-scheduler
    - 10252 - kube-controller-manager
    - 10256 - kube-proxy

13. Kubernetes apps:

    - 30104 - auth-service (Keycloak)
    - 32300-32302 - Ignite (REST API, SQL port, Thin clients)
    - 30672,31672 - RabbitMQ (AMQP, management)

14. HAProxy:

    - 443 - HTTPS frontend
    - 9000 - stats page
    - unconfigurable random UDP port from ephemeral range* - local connection to rsyslog UDP server (remote access not needed), see note [[3]](#notes)

    \* Not applicable for Ubuntu where UNIX socket is used (deb package's default).

15. Ignite:

    - 8080 - REST API
    - 10800-10809* - JDBC Thin Driver
    - 11211-11220* - JDBC Client Driver
    - 47100-47109* - communication SPI
    - 47500-47509* - discovery SPI
    - 49112 - JMX (remote access), limited by Epiphany to be accessible only through SSH tunnel (java.rmi.server.hostname=127.0.0.1)
    - unconfigurable random port from ephemeral range - JMX (for local access only), see note [[1]](#notes)

    \* By default, only the first port from the range is used (port ranges are handy when starting multiple grid nodes on the same machine)

16. Repository:

    - 80 - deb/rpm package repository (httpd is stopped at the end of installation)
    - 5000 - Docker image registry

17. Hashicorp Vault:

    - 8200 - REST API

#### Notes

1. JMX:

    - [JDK-8035404](https://bugs.openjdk.java.net/browse/JDK-8035404) - Java opens random 3-d port when JMX is configured
    - [JDK-8234484](https://bugs.openjdk.java.net/browse/JDK-8234484) - Add ability to configure third port for remote JMX

    The effective ephemeral port range is accessible via `/proc/sys/net/ipv4/ip_local_port_range`.

2. rpcbind:

    - Bug [411761](https://bugzilla.redhat.com/show_bug.cgi?id=411761) - rpcbind listens on random, possibly reserved UDP port
    - Bug [1595170](https://bugzilla.redhat.com/show_bug.cgi?id=1595170) - rpcbind sometimes uses port 749/UDP, which breaks Kerberos admin and FreeIPA

3. HAProxy:

    - Stack Overflow: [What is the purpose of haproxy random udp listening port?](https://stackoverflow.com/questions/52306468/what-is-the-purpose-of-haproxy-random-udp-listening-port)
    - HAProxy source code: [__send_log()](https://github.com/haproxy/haproxy/blob/0b78792bbe61fec420e4e7298d145ec7d498f8f2/src/log.c#L1088) function

    The use of UNIX socket was not implemented because it is [not recommended](https://www.haproxy.com/documentation/hapee/1-8r2/onepage/management/#8).
