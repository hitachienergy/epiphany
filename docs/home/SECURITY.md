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

10. Repository:

    - 80 - deb/rpm package repository (httpd is stopped at the end of installation)

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

2. Kafka:

    - protocols:  
      TLSv1.2,TLSv1.1,TLSv1

    - ciphersuites:  
      Depends on version of Java and for Java versions older than 8u161 on JCE policy file. From update 8u161 JCE policy
      file is not needed to enable restricted ciphers as all ciphers are enabled by default. Documentation about ciphers
      is available under [link](https://docs.oracle.com/javase/8/docs/technotes/guides/security/SunProviders.html).

3. Open Distro:

    - protocols:  
      TLSv1.1,TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-GCM-SHA256 DHE-RSA-AES256-GCM-SHA384 DHE-RSA-AES128-GCM-SHA256
      ECDHE-RSA-AES256-SHA384 ECDHE-RSA-AES128-SHA256 DHE-RSA-AES256-SHA256 DHE-RSA-AES128-SHA256 ECDHE-RSA-AES256-SHA
      ECDHE-RSA-AES128-SHA DHE-RSA-AES256-SHA DHE-RSA-AES128-SHA

4. OpenSearch Dashboards:

    - protocols:  
      TLSv1.1,TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-SHA256 ECDHE-RSA-AES256-SHA384
      ECDHE-RSA-AES256-SHA ECDHE-RSA-AES128-SHA AES256-GCM-SHA384 AES128-GCM-SHA256 AES256-SHA256 AES128-SHA256
      AES256-SHA AES128-SHA

5. Grafana:

    - protocols:  
      TLSv1.2

    - ciphersuites:  
      ECDHE-RSA-AES128-GCM-SHA256 ECDHE-RSA-AES256-GCM-SHA384 ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA
      AES128-GCM-SHA256 AES256-GCM-SHA384 AES128-SHA AES256-SHA

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
