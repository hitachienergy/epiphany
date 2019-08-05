# Security related information

## Contents

- [Users and roles created by epiphany](#users-and-roles-created-by-epiphany)



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

