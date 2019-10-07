# Epiphany Platform cache storage design document

Affected version: 0.4.x

## Goals

Provide in-memory cache storage that will be capable of store large amount of data with hight performance.

## Use cases

Platform should provide cache storage for key-value stores, latest value taken from queue (Kafka).

## Architectural decision

Considered options are:
- Apache Ignite
- Redis

Description | Apache Ignite | Redis |
--- | ---| --- |
License | Apache 2.0 | three clause BSD license
Partition method | Sharding | Sharding
Replication | Yes | Master-slave - yes, Master - Master - only enterprise version
Transaction concept | ACID | Optimistic lock |
Data Grid | Yes | N/A |
In-memory DB | Distributed key-value store, in-memory distributed SQL database | key-value store
Integration with RDBMS | Can integrate with any relational DB that supports JDBC driver (Oracle, PostgreSQL, Microsoft SQL Server, and MySQL) | Possible using 3rd party software
Integration with Kafka | Using `Streamer` (Kafka Streamer, MQTT Streamer, ...) possible to insert to cache | Required 3rd party service
Machine learning | Apache Ignite Machine Learning - tools for building predictive ML models | N/A

Based on above - Apache Ignite is not just scalable in-memory cache/database but cache and processing platform which can run transactional, analytical and streaming workloads. While Redis is simpler, Apache Ignite offers lot more features with Apache 2.0 licence.

Choice: **Apache Ignite**

## Design proposal

[MVP] Add Ansible role to `epicli` that installs Apache Ignite and sets up cluster if there is more than one instance. Ansible playbook is also responsible for adding more nodes to existing cluster (scaling).

Possible problems while implementing Ignite clustering:
- Ignite uses multicast for node discovery which is not supported on AWS. Ignite distribution comes with `TcpDiscoveryS3IpFinder` so S3-based discovery can be used.

To consider:
- Deploy Apache Ignite cluster in Kubernetes
