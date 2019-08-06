# Security related information

## Contents

- [Users and roles created by Epiphany](#users-and-roles-created-by-epiphany)
- [Ports used by components in Epiphany](#ports-used-by-components-in-epiphany)


### Users and roles created by epiphany

By default Epiphany is creating user operations that is used to connect to machines with admin rights. This setting can 
be changed in Epiphany yaml configuration files. 

Additional to users created by each component Epiphany creates also users and groups:

  - haproxy_exporter/haproxy_exporter
  - kafka_exporter/kafka_exporter
  - node_exporter/node_exporter
  - jmx-exporter/jmx-exporter
  - prometheus/prometheus
  - rabbitmq/rabbitmq
  - zookeeper/zookeeper
  - kafka/kafka
  
Other accounts created by each component you can find in these components documentation.


### Ports used by components in Epiphany

Below you can find list of ports used in Epiphany on per component basis:

1. OS services:
 
    - 22 - ssh

2. Prometheus exporters:

    - 9100 - Node exporter
    - 9101 - HAProxy exporter
    - 9308 - Kafka exporter

3. Zookeeper:

    - 2181 - Zookeeper client
    - 2888 - Zookeeper nodes
    - 3888 - Zookeper inter nodes

4. Kafka:

    - 9092 - Kafka broker

5. Elasticsearch:

    - 9200 - Elasticsearch REST communication
    - 9300 - Elasticsearch nodes communication

6. Kibana:

    - 5601 -  Kibana web UI

7. Prometheus:

    - 9090 - Prometheus server

8. Alertmanager:

    - 9093 - Alertmanager service

9. Grafana:

    - 3000 - Grafana web UI

10. RabbitMQ:

    - 5672 - RabbitMQ server

11. Postgresql:

    - 5432 - Postgresql server

12. Kubernetes:

    - 4149 - kubelet
    - 6443 - kube-apiserver
    - 9099 - calico-felix
    - 10250 - kubelet
    - 10255 - kubelet
    - 10256 - kube-proxy
