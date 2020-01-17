## Centralized logging setup

For centralized logging Epiphany uses [OpenDistro for Elasticsearch](https://opendistro.github.io/for-elasticsearch/). In order to enable centralized logging, there is required to use `logging` role on feature mapping level - as of 0.5.0 this is a default configuration.

```yaml
    ...
    logging:
      - logging
      - kibana
      - filebeat
      - firewall
    ...
```

The `logging` role replaced `elasticsearch` role in logging feature. This change was done to enable Elasticsearch usage for data storage - not only for logs as it was till 0.5.0.

Default configuration of `logging` role is the same as [opendistro_for_elasticsearch](./DATABASES.md#how-to-start-working-with-opendistro-for-elasticsearch) which is used for logs storage. In order to modify centralized logging configuration adjust and use following defaults:

```yaml
kind: configuration/logging
title: Logging Config
name: default
specification:
  opendistro_version_redhat: "1.3.0"
  elasticsearch_oss_version_debian: "7.3.2"
  opendistro_version_debian: "1.3.0*"
  cluster_name: EpiphanyElastic
  clustered: True
  paths:
    data: /var/lib/elasticsearch
    logs: /var/log/elasticsearch
```