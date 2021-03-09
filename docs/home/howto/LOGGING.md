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
## How to manage Opendistro for Elasticsearch data

Elasticsearch stores data using JSON documents, and an Index is a collection of documents. As in every database it's crutial to correctly maintain data in this one. It's almost impossible to deliver database configuration which will fit to every type of project and data stored in. Epiphany deploys preconfigured Opendistro Elasticsearch, but this configuration may not meet user requirements. Before going to production configuration shoud be tailor to project needs. All configuration tips and tricks are available in [official documentation](https://opendistro.github.io/for-elasticsearch-docs/).

The main and most importand decisions to take before you deploy cluster are:

1) How many Nodes are needed
2) How big machines and/or storage data disks need to be used

These parameters are defined in yaml file and it's important to create big enough cluster.

```
specification:
  components:
    logging:
      count: 1    #  Choose number of nodes
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
name: logging-machine
specification:
  size: Standard_DS2_v2    #  Choose machine size
```

If it's required to have Elasticsearch which works in cluster formation configuration, except setting up more than one machine in yaml config file please acquaint dedicated support [article](https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/cluster/) and adjust Elasticseach configuration file.

At this moment Opendistro for Elasticsearch does not support [ILM](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html) (like it was in OSS Elasticsearch), log rotation is possible only by configuration created in Index State Management.

`ISM - Index State Management` - is a plugin that provides users and administrative panel to monitor the indices and apply policies at different index stages. ISM lets users automate periodic, administrative operations by triggering them besed on index age, size, or number of documents. Using the ISM plugin, can define policies that automatically handle index rollovers or deletions. ISM is installed with Opendistro by default - user does not have to enable this.
Official documentation is available in [Opendistro for Elasticsearch website](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/).

To reduce the consumption of disk resources, every index you created should use well designed [policy](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/).

Among others these two index actions might save machine from filling up disk space:

[`Index Rollover`](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/#rollover) - rolls an alias to a new index. Set up correctly max index size / age or minimum number of documents to keep index size in requirements framework.

[`Index Deletion`](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/#delete) - deletes indexes managed by policy

Combining these actions, adapting them to data amount and specification users are able to create policy which will maintain data in cluster  for example: to secure node from fullfilling disk space.

There is example of policy below. Be aware that this is only example, and it needs to be adjust to environment needs.

```
{
    "policy": {
        "policy_id": "epi_policy",
        "description": "Safe setup for logs management",
        "last_updated_time": 1615201615948,
        "schema_version": 1,
        "error_notification": null,
        "default_state": "keep",
        "states": [
            {
                "name": "keep",
                "actions": [],
                "transitions": [
                    {
                        "state_name": "delete",
                        "conditions": {
                            "min_index_age": "14d"
                        }
                    },
                    {
                        "state_name": "rollover_by_size",
                        "conditions": {
                            "min_size": "1gb"
                        }
                    },
                    {
                        "state_name": "rollover_by_time",
                        "conditions": {
                            "min_index_age": "1d"
                        }
                    }
                ]
            },
            {
                "name": "delete",
                "actions": [
                    {
                        "delete": {}
                    }
                ],
                "transitions": []
            },
            {
                "name": "rollover_by_size",
                "actions": [
                    {
                        "rollover": {}
                    }
                ],
                "transitions": []
            },
            {
                "name": "rollover_by_time",
                "actions": [
                    {
                        "rollover": {}
                    }
                ],
                "transitions": []
            }
        ]
    }
}
```
Example above shows configuration with rollover daily or when index achieve 1GB size. Indexes older than 14 days will be deleted. States and condionals could be cobined. Please see [policies](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/) documentation for more details.

`Apply Policy`

To apply policy use similar API request as presented below:
```
PUT _template/template_01
{
  "index_patterns": ["filebeat*"],
  "settings": {
    "opendistro.index_state_management.rollover_alias": "filebeat"
    "opendistro.index_state_management.policy_id": "epi_policy"
  }
}
```
After applying this policy every new index created under this one will apply to it. There is also possibility to apply policy to already existing policies by assigning them to policy in Index Management Kibana panel.

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
