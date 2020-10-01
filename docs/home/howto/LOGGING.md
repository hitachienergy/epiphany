# Centralized logging setup

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

## Default feature mapping for logging

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
>Optional feature (role) available for logging: **logstash**
>more details here: [link](https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/howto/LOGGING.md#how-to-export-elasticsearch-data-to-csv-format)

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

## How to export Elasticsearch data to csv format

Since v0.8 Epiphany provide posibility to export data from Elasticsearch to CSV using Logstash *(logstash-oss v7.8.1*) along with *logstash-input-elasticsearch (v4.6.2)* and *logstash-output-csv (v3.0.8)* plugin.

To install Logstash in your cluster add **logstash** to feature mapping for *logging, opendistro_for_elasticsearch* or *elasticsearch* group.

Epiphany provides a basic configuration file `(logstash-export.conf.template)` as template for your data export.
This file has to be modified according to your Elasticsearch configuration and data you want to export.

`Note: Exporting data is not automated. It has to be invoked manually. Logstash daemon is disabled by default after installation.`

Run Logstash to export data:  
`/usr/share/logstash/bin/logstash -f /etc/logstash/logstash-export.conf`

More details about configuration of input plugin:  
https://www.elastic.co/guide/en/logstash/current/plugins-inputs-elasticsearch.html

More details about configuration of output plugin:  
https://www.elastic.co/guide/en/logstash/current/plugins-outputs-csv.html

Note: Currently input plugin doesn't officialy support skipping certificate validation for secure connection to Elasticsearch.

For non-production environment you can easly disable it by adding new line:  
`ssl_options[:verify] = false` right after other ssl_options definitions in file:  
`/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-input-elasticsearch-4.6.2/lib/logstash/inputs/elasticsearch.rb`

## How to add multiline support for Filebeat logs

In order to properly handle multilines in files harvested by Filebeat you have to provide `multiline` definition in the configuration manifest. Using the following code you will be able to specify which lines are part of a single event.

By default postgresql block is provided, you can use it as example:  
```yaml
  postgresql_input:
    multiline:
      pattern: >-
        '^\d{4}-\d{2}-\d{2} '
      negate: true
      match: after
```
Currently supported inputs: `common_input`,`postgresql_input`,`container_input`  
More details about multiline options you can find in the [official documentation](https://www.elastic.co/guide/en/beats/filebeat/current/multiline-examples.html)
