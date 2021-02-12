An Epiphany cluster has a number of components which log, collect and retain data. To make sure that these do not exceed
the usable storage of the machines there running on the following configurations are available.

## Elasticsearch

TODO

## Grafana

TODO

## Kafka

There are two types of retention policies that can be configured at the broker or topic levels: based on time or size.
Epiphany defines the same default value for broker size retention policy as Kafka, -1, which means that no
size limit is applied.

To define new log retention values following configuration can be used:

```yaml
kind: configuration/kafka
title: "Kafka"
name: default
specification:
    kafka_var:
        partitions: 8
        log_retention_hours: 168
        log_retention_bytes: -1
```

### Configuration parameters

#### specification.kafka_var.partitions

Sets [num.partitions](https://kafka.apache.org/documentation/#brokerconfigs_num.partitions) parameter

#### specification.kafka_var.log_retention_hours

Sets [log.retention.hours](https://kafka.apache.org/documentation/#brokerconfigs_log.retention.bytes) parameter

#### specification.kafka_var.log_retention_bytes

Sets [log.retention.bytes](https://kafka.apache.org/documentation/#brokerconfigs_log.retention.bytes) parameter

---
**NOTE**

Since this limit is enforced at the partition level, multiply it by the number of partitions to compute the topic
retention in bytes.

---

## Kibana

TODO

## Kubernetes

TODO

## Prometheus

TODO

## Zookeeper

TODO
