## Centralized logging setup

For centralized logging Epiphany uses [OpenDistro for Elasticsearch](https://opendistro.github.io/for-elasticsearch/).
In order to enable centralized logging, be sure that `count` property for `logging` feature is greater than 0 in your configuration manifest.

```yaml
kind: epiphany-cluster
...
specification:
  ...
  components:
    kubernetes_master:
      count: 1
    kubernetes_node:
      count: 0
    ...
    logging:
      count: 1
    ...
```

### Default feature mapping for logging:
```yaml
    ...
    logging:
      - logging
      - kibana
      - node-exporter
      - filebeat
      - firewall
    ...
```
The `logging` role replaced `elasticsearch` role. This change was done to enable Elasticsearch usage also for data storage - not only for logs as it was till 0.5.0.

Default configuration of `logging` and `opendistro_for_elasticsearch` roles is identical (./DATABASES.md#how-to-start-working-with-opendistro-for-elasticsearch). To modify configuration of centralized logging adjust and use the following defaults in your manifest:

```yaml
kind: configuration/logging
title: Logging Config
name: default
specification:
  cluster_name: EpiphanyElastic
  clustered: True
  paths:
    data: /var/lib/elasticsearch
    repo: /var/lib/elasticsearch-snapshots
    logs: /var/log/elasticsearch
```
