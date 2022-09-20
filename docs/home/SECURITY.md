# Security related information

You are strongly advised use encrypted over unencrypted communication between Epiphany components where possible. Please
consider this during planning your Epiphany deployment and configuration.

We strongly advise changing default passwords wherever Epiphany configuration let you do so.

We strongly advise using antivirus/antimalware software wherever possible to prevent security risks. Please consider
this during planning your Epiphany deployment and test if Epiphany components are installing correctly with necessary
changes made in settings of your antivirus/antimalware solution.

## Contents

- [Security related information](#security-related-information)
  - [Contents](#contents)
    - [Users and roles created by epiphany](#users-and-roles-created-by-epiphany)
    - [Ports used by components in Epiphany](#ports-used-by-components-in-epiphany)
    - [Connection protocols and ciphers used by components in Epiphany](#connection-protocols-and-ciphers-used-by-components-in-epiphany)
      - [Notes](#notes)

### Users and roles created by epiphany

By default, Epiphany creates user 'operations' that is used to connect to machines with admin rights on every machine.
This setting can be changed in Epiphany yaml configuration files.

Additional to users created by each component Epiphany creates also users and groups:

- kafka_exporter/kafka_exporter
- node_exporter/node_exporter
- jmx-exporter/jmx-exporter
- prometheus/prometheus
- rabbitmq/rabbitmq
- zookeeper/zookeeper
- kafka/kafka

Other accounts created by each component you can find in the documentation of these components.

### Ports used by components in Epiphany

Below you can find list of ports used by default in Epiphany on per component basis. Some of them can be changed to
different values. The list does not include ports that are bound to the loopback interface (localhost).

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

5. OpenSearch:

    - 9200 - OpenSearch REST communication
    - 9300 - OpenSearch nodes communication
    - 9600 - Performance Analyzer (REST API)

6. OpenSearch Dashboards:

    - 5601 - OpenSearch Dashboards web UI

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
    - 15692 - rabbitmq-exporter for Prometheus
    - 25672 - distribution server

11. PostgreSQL:

    - 5432 - PostgreSQL server

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

    - 30103,30104 - Keycloak
    - 30672,31672 - RabbitMQ (AMQP, management)

14. HAProxy:

    - 443 - HTTPS frontend
    - 9000 - stats page
    - 9101 - metrics
    - unconfigurable random UDP port from ephemeral range* - local connection to rsyslog UDP server (remote access not needed), see note [[3]](#notes)

    **NOTE:** Not applicable for Ubuntu where UNIX socket is used (deb package's default).

15. Repository:

    - 80 - deb/rpm package repository (httpd is stopped at the end of installation)
    - 5000 - Docker image registry

### Connection protocols and ciphers used by components in Epiphany

Below you can find list of cipersuites and protocols used for communication set in Epiphany on per component basis.

1. OS services:

    - SSH
        - ciphersuites:  
          chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
        - macs:  
          hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umac-128-etm@openssh.com,hmac-sha2-512,hmac-sha2-256,umac-128@openssh.com
        - kexalgorithms:  
          curve25519-sha256@libssh.org,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256

2. HAProxy:

    - protocols:  
      TLSv1.2

    - ciphersuites:  
      ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:
      ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:
      DHE-RSA-AES256-GCM-SHA384

3. Kafka:

    - protocols:  
      TLSv1.2,TLSv1.1,TLSv1

    - ciphersuites:  
      Depends on version of Java and for Java versions older than 8u161 on JCE policy file. From update 8u161 JCE policy
      file is not needed to enable restricted ciphers as all ciphers are enabled by default. Documentation about ciphers
      is available under [link](https://docs.oracle.com/javase/8/docs/technotes/guides/security/SunProviders.html).

4. Open Distro:

    - protocols:  
      TLSv1.1,TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-GCM-SHA256 DHE-RSA-AES256-GCM-SHA384 DHE-RSA-AES128-GCM-SHA256
      ECDHE-RSA-AES256-SHA384 ECDHE-RSA-AES128-SHA256 DHE-RSA-AES256-SHA256 DHE-RSA-AES128-SHA256 ECDHE-RSA-AES256-SHA
      ECDHE-RSA-AES128-SHA DHE-RSA-AES256-SHA DHE-RSA-AES128-SHA

5. Kibana:

    - protocols:  
      TLSv1.1,TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES256-SHA384
      ECDHE-RSA-AES256-SHA ECDHE-RSA-AES128-SHA AES256-GCM-SHA384 AES128-GCM-SHA256 AES256-SHA256 AES128-SHA256
      AES256-SHA AES128-SHA

6. Grafana:

    - protocols:  
      TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA
      AES128-GCM-SHA256 AES256-GCM-SHA384 AES128-SHA AES256-SHA

7. RabbitMQ:

    - protocols:  
      TLSv1.3, TLSv1.2

    - ciphersuites:  
      ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-GCM-SHA384 ECDH-ECDSA-AES256-GCM-SHA384 ECDH-RSA-AES256-GCM-SHA384
      DHE-RSA-AES256-GCM-SHA384 DHE-DSS-AES256-GCM-SHA384 ECDHE-ECDSA-AES128-GCM-SHA256 ECDHE-RSA-AES128-GCM-SHA256
      ECDH-ECDSA-AES128-GCM-SHA256 ECDH-RSA-AES128-GCM-SHA256 DHE-RSA-AES128-GCM-SHA256 DHE-DSS-AES128-GCM-SHA256

8. Kubernetes:

    - protocols:  
      TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-SHA AES256-GCM-SHA384 AES256-SHA ECDHE-RSA-AES128-GCM-SHA256
      ECDHE-RSA-AES128-SHA AES128-GCM-SHA256 AES128-SHA ECDHE-RSA-DES-CBC3-SHA DES-CBC3-SHA

9. Kubernetes apps:

    - Keycloak:

        - protocols:  
          TLSv1.2

        - ciphers:  
          ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES256-SHA384 ECDHE-RSA-AES256-SHA DHE-RSA-AES256-GCM-SHA384
          DHE-RSA-AES256-SHA256 DHE-RSA-AES256-SHA AES256-GCM-SHA384 AES256-SHA256 AES256-SHA
          ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES128-SHA DHE-RSA-AES128-GCM-SHA256
          DHE-RSA-AES128-SHA256 DHE-RSA-AES128-SHA AES128-GCM-SHA256 AES128-SHA256 AES128-SHA

#### Notes

1. JMX:

    - [JDK-8035404](https://bugs.openjdk.java.net/browse/JDK-8035404) - Java opens random 3-d port when JMX is
      configured
    - [JDK-8234484](https://bugs.openjdk.java.net/browse/JDK-8234484) - Add ability to configure third port for remote
      JMX

   The effective ephemeral port range is accessible via `/proc/sys/net/ipv4/ip_local_port_range`.

2. rpcbind:

    - Bug [411761](https://bugzilla.redhat.com/show_bug.cgi?id=411761) - rpcbind listens on random, possibly reserved
      UDP port
    - Bug [1595170](https://bugzilla.redhat.com/show_bug.cgi?id=1595170) - rpcbind sometimes uses port 749/UDP, which
      breaks Kerberos admin and FreeIPA

3. HAProxy:

    - Stack Overflow:
      [What is the purpose of haproxy random udp listening port?](https://stackoverflow.com/questions/52306468/what-is-the-purpose-of-haproxy-random-udp-listening-port)
    - HAProxy source code:
      [__send_log()](https://github.com/haproxy/haproxy/blob/0b78792bbe61fec420e4e7298d145ec7d498f8f2/src/log.c#L1088)
      function

   The use of UNIX socket was not implemented because it
   is [not recommended](https://www.haproxy.com/documentation/hapee/1-8r2/onepage/management/#8).
