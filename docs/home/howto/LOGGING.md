# Centralized logging setup

For centralized logging Epiphany uses [OpenDistro for Elasticsearch](https://opendistro.github.io/for-elasticsearch/).
In order to enable centralized logging, be sure that `count` property for `logging` feature is greater than 0 in your
configuration manifest.

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

The `logging` role replaced `elasticsearch` role. This change was done to enable Elasticsearch usage also for data
storage - not only for logs as it was till 0.5.0.

Default configuration of `logging` and `opensearch` roles is identical (
./DATABASES.md#how-to-start-working-with-opensearch-for-elasticsearch). To modify configuration of centralized logging
adjust and use the following defaults in your manifest:

```yaml
kind: configuration/logging
title: Logging Config
name: default
specification:
  cluster_name: EpiphanyElastic
  clustered: True
  paths:
    data: /var/lib/opensearch
    repo: /var/lib/opensearch-snapshots
    logs: /var/log/opensearch
```

## How to manage Opendistro for Elasticsearch data

Elasticsearch stores data using JSON documents, and an Index is a collection of documents. As in every database, it's
crucial to correctly maintain data in this one. It's almost impossible to deliver database configuration which will fit
to every type of project and data stored in. Epiphany deploys preconfigured Opendistro Elasticsearch, but this
configuration may not meet user requirements. Before going to production, configuration should be tailored to the
project needs. All configuration tips and tricks are available
in [official documentation](https://opendistro.github.io/for-elasticsearch-docs/).

The main and most important decisions to take before you deploy cluster are:

1) How many Nodes are needed
2) How big machines and/or storage data disks need to be used

These parameters are defined in yaml file, and it's important to create a big enough cluster.

```yaml
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

If it's required to have Elasticsearch which works in cluster formation configuration, except setting up more than one
machine in yaml config file please acquaint dedicated
support [article](https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/cluster/) and adjust
Elasticsearch configuration file.

At this moment Opendistro for Elasticsearch does not support plugin similar
to [ILM](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html), log rotation
is possible only by configuration created in Index State Management.

`ISM - Index State Management` - is a plugin that provides users and administrative panel to monitor the indices and
apply policies at different index stages. ISM lets users automate periodic, administrative operations by triggering them
based on index age, size, or number of documents. Using the ISM plugin, can define policies that automatically handle
index rollovers or deletions. ISM is installed with Opendistro by default - user does not have to enable this. Official
documentation is available
in [Opendistro for Elasticsearch website](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/).

To reduce the consumption of disk resources, every index you created should use
well-designed [policy](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/).

Among others these two index actions might save machine from filling up disk space:

[`Index Rollover`](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/#rollover) - rolls an alias
to a new index. Set up correctly max index size / age or minimum number of documents to keep index size in requirements
framework.

[`Index Deletion`](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/#delete) - deletes indexes
managed by policy

Combining these actions, adapting them to data amount and specification users are able to create policy which will
maintain data in cluster for example: to secure node from fulfilling disk space.

There is example of policy below. Be aware that this is only example, and it needs to be adjusted to environment needs.

```json
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

Example above shows configuration with rollover daily or when index achieve 1 GB size. Indexes older than 14 days will
be deleted. States and conditionals could be combined. Please
see [policies](https://opendistro.github.io/for-elasticsearch-docs/docs/im/ism/policies/) documentation for more
details.

`Apply Policy`

To apply policy use similar API request as presented below:

```
PUT _template/template_01
```

```json
{
  "index_patterns": ["filebeat*"],
  "settings": {
    "opendistro.index_state_management.rollover_alias": "filebeat"
    "opendistro.index_state_management.policy_id": "epi_policy"
  }
}
```

After applying this policy, every new index created under this one will apply to it. There is also possibility to apply
policy to already existing policies by assigning them to policy in Index Management Kibana panel.

## How to export Kibana reports to CSV format

Since v1.0 Epiphany provides the possibility to export reports from Kibana to CSV, PNG or PDF using the Open Distro for
Elasticsearch Kibana reports feature.

Check more details about the plugin and how to export reports in the
[documentation](https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/reporting)  

`Note: Currently in Open Distro for Elasticsearch Kibana the following plugins are installed and enabled by default: security, alerting, anomaly detection, index management, query workbench, notebooks, reports, alerting, gantt chart plugins.`

You can easily check enabled default plugins for Kibana using the following command on the logging machine:
`./bin/kibana-plugin list` in Kibana directory.

---

## How to add multiline support for Filebeat logs

In order to properly handle multilines in files harvested by Filebeat you have to provide `multiline` definition in the
configuration manifest. Using the following code you will be able to specify which lines are part of a single event.

By default, postgresql block is provided, you can use it as example:

```yaml
postgresql_input:
  multiline:
    pattern: >-
      '^\d{4}-\d{2}-\d{2} '
    negate: true
    match: after
```

Supported inputs: `common_input`,`postgresql_input`,`container_input`
More details about multiline options you can find in
the [official documentation](https://www.elastic.co/guide/en/beats/filebeat/current/multiline-examples.html)

## How to deploy Filebeat as Daemonset in K8s

There is a possibility to deploy Filebeat as daemonset in K8s. To do that, set `k8s_as_cloud_service` option to `true`:

```yaml
kind: epiphany-cluster
specification:
  cloud:
    k8s_as_cloud_service: true
```

## How to use default Kibana dashboards

It is possible to configure `setup.dashboards.enabled` and `setup.dashboards.index` Filebeat settings using `specification.kibana.dashboards` key in `configuration/filebeat` doc.
When `specification.kibana.dashboards.enabled` is set to `auto`, the corresponding setting in Filebeat configuration file will be set to `true` only if Kibana is configured to be present on the host.
Other possible values are `true` and `false`.

Default configuration:
```
specification:
  kibana:
    dashboards:
      enabled: auto
      index: filebeat-*
```

Note: Setting `specification.kibana.dashboards.enabled` to `true` not providing Kibana will result in a Filebeat crash.
