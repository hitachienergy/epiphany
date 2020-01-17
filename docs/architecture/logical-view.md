# Epiphany Logical View

## Overview

Epiphany Platform architecture can be divided into functional modules that realize closely related set of functionality.

![Logical view architecture diagram](diagrams/logical-view/logical-view-diagram.svg)

## Monitoring

### Exporters

Platform monitoring uses set of `exporter` components that the responsibility is to collect metrics. Following table shows which `exporter` is collecting metrics from each Epiphany component.

Exporter | Component | Description
--- | --- | ---
`Node exporter` | OS/Hardware metrics | [description](https://prometheus.io/docs/guides/node-exporter/)
`Kafka exporter` | Kafka metrics | [description](https://github.com/danielqsj/kafka_exporter)
`JMX exporter` | JVM metrics (Kafka, Zookeeper) | [description](https://github.com/prometheus/jmx_exporter)
`HAProxy exporter` | HAProxy metrics | [description](https://github.com/prometheus/haproxy_exporter)
`cAdvisor` | Container metrics (Kubernetes, Docker) | [description](https://prometheus.io/docs/guides/cadvisor/)

### Prometheus

`Prometheus` is open-source system used for monitoring and alerting. Each `exporter` exposes `http://server-name/metrics` endpoint that contains monitoring data, then `Prometheus` collects this data in configured interval. To find more information about `Prometheus` use this [link](https://prometheus.io/docs/introduction/overview/).

### Grafana

Once the data are collected, they can be shown in `Grafana` dashboards. `Grafana` in Epiphany Platform has `Prometheus` datasource configured by default. It uses [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) to query `Prometheus` database. To read more about `Grafana` use this [link](https://grafana.com/).

### Alert Manager

When alert rule is met `Prometheus` generates alert.
The alert is handled by `Alert Manager` and depending on configuration is routed to `Slack`, `PagerDuty`, `Email`, etc. To read more about `Alert Manager` use this [link](https://prometheus.io/docs/alerting/alertmanager/).

## Logging

### Filebeat

Epiphany Platform logging uses `Filebeat` to collect logs. It reads data from following locations:

Source | Purpose  
--- | ---  
/var/log/audit/audit.log | Logs from Linux audit daemon
/var/log/auth.log | System authorization information and user logins
/var/log/firewalld | Firewall logs
/var/log/haproxy.log | HAProxy logs
/var/log/kafka/server.log | Kafka logs
/var/log/messages | Global system messages
/var/log/secure | Logs from authentication and authorization
/var/log/syslog | System logs and events
/var/log/zookeeper/version-2/* | Zookeeper's logs
Docker containers | Kubernetes components that run in a container

`Filebeat`, unlike `Grafana`, pushes data to database (`Elasticsearch`) instead of pulling them.
[Read more](https://www.elastic.co/products/beats/filebeat) about `Filebeat`.

### Elasticsearch

`Elasticsearch` is highly scalable and full-text search enabled analytics engine. Epiphany Platform uses it for storage and analysis of logs.

[Read more](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/index.html)

### Elasticsearch Curator

`Elasticsearch Curator` is component that manages and cleans indices and snapshots. Epiphany uses `Elasticsearch Curator` to ensure that centralized logging will not completely fill disk space.

[Read more](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.8/index.html)

### Kibana

`Kibana` like `Grafana` is used in Epiphany for visualization, in addition it has full text search capabilities. `Kibana` uses `Elasticsearch` as datasource for logs, it allows to create full text queries, dashboards and analytics that are performed on logs.

[Read more](https://www.elastic.co/products/kibana)

## Computing

Epiphany Platform benefits from `Kubernetes` capabilities. Product team creates a `Docker` enabled applications and using [deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) installs them in a `Kubernetes cluster`.

### Kubernetes Master

`Kubernetes Master` is the component that provides control plane for a cluster. It handles an application's deployments and responds for events. Usually `Kubernetes Master` does not run application's pods.

[Read more](https://kubernetes.io/docs/concepts/overview/components/#master-components)

### Kubernetes Nodes

`Kubernetes Node` component maintains running pods that `Kubernetes Master` delegates to work on the node. Usually there are many `Kubernetes Nodes` for single or many `Kubernetes Masters`.

[Read more](https://kubernetes.io/docs/concepts/overview/components/#node-components)

## Messaging

Kafka is a distributed streaming and messaging platform.

### Kafka Brokers

`Kafka Broker` is a synonym for Kafka Server or Kafka Node. Brokers allow producers and consumers to publish and consume messages. `Kafka` is horizontally scalable - in short it means that adding new brokers increases `Kafka` cluster capacity.

[Read more](https://kafka.apache.org/documentation/)

### Zookeeper

`Zookeeper` in Epiphany Platform is used for distributed `Kafka` configuration management. Simplified: From application's perspective it provides information about location of topic/partition that application writes or reads.

Zookeepers are usually deployed in more than one instance - this is called Zookeepers ensemble.

[Read more](https://cwiki.apache.org/confluence/display/ZOOKEEPER/Index)

## Load Balancing

### HAProxy

`HAProxy` is a high performance load balancer. Applications deployed on `Kubernetes` can be exposed through `HAProxy` that supports TLS termination and supports multiple backends.
Epiphany Platform automates the configuration for backend and frontend of `HAProxy`.

[Read more](http://www.haproxy.org/#desc)