# Centralized logging setup

For centralized logging Epiphany uses [Open Search](https://opensearch.org/) stack - an opensource successor<sup>[1]</sup> of Elasticsearch & Kibana projects.

In order to enable centralized logging, be sure to set `count` property for `logging` feature to the value greater than 0 in your
configuration manifest.

```yaml
kind: epiphany-cluster
[...]
specification:
  [...]
  components:
    kubernetes_master:
      count: 1
    kubernetes_node:
      count: 0
    [...]
    logging:
      count: 1  # <<------
    [...]
```

## Default feature mapping for logging

Below example shows a default feature mapping for logging:
```yaml
[...]
roles_mapping:
[...]
  logging:
    - logging
    - opensearch-dashboards
    - node-exporter
    - filebeat
    - firewall
...
```

The `logging` role has replaced `elasticsearch` role. This change was done to enable Elasticsearch usage also for data
storage - not only for logs as it was till 0.5.0.

Default configuration of `logging` and `opensearch` roles is identical ( more info [here](./DATABASES.md#how-to-start-working-with-opensearch) ). To modify configuration of centralized logging
adjust to your needs the following default values in your manifest:

```yaml
[...]
kind: configuration/logging
title: Logging Config
name: default
specification:
  cluster_name: EpiphanyOpensearch
  clustered: True
  paths:
    data: /var/lib/opensearch
    repo: /var/lib/opensearch-snapshots
    logs: /var/log/opensearch
```

## How to manage OpenSearch data

OpenSearch stores data using JSON documents, and an Index is a collection of documents. As in every database, it's crucial to correctly maintain data in this one. It's almost impossible to deliver database configuration which will fit to every type of project and data stored in. Epiphany deploys preconfigured OpenSearch instance but this configuration may not meet any single user requirements. That's why, before going to production, stack configuration should be tailored to the project needs. All configuration tips and tricks are available in [official documentation](https://opensearch.org/docs/latest).

The main and most important decisions to take before you deploy the cluster are:

- how many nodes are needed
- how big machines and/or storage data disks need to be used

These parameters can be defined in manifest yaml file. It is important to create a big enough cluster.

```yaml
specification:
  [..]
  components:
    logging:
      count: 1    #  Choose number of nodes that suits your needs
      machines:
      - logging-machine-n
  [..]
---
kind: infrastructure/virtual-machine
title: "Virtual Machine Infra"
name: logging-machine-n
specification:
  size: Standard_DS2_v2    #  Choose a VM size that suits your needs
```

If it's required to have OpenSearch instance which works in cluster formation configuration, except setting up more than one machine in yaml config file please acquaint dedicated
support [article](https://opensearch.org/docs/latest/troubleshoot/index/) and adjust
OpenSearch configuration file.

We also want to strongly encourage you to get familiar with a bunch of plugins and policies available along with OpenSearch with the following ones among them:

`ISM - Index State Management` - is a plugin that allows users and administrative panel to monitor the indices and apply policies at different index stages. ISM lets users automate periodic, administrative operations by triggering them based on index age, size, or number of documents. Using the ISM plugin, can define policies that automatically handle index rollovers or deletions. Official plugin documentation is available [here](https://opensearch.org/docs/latest/im-plugin/ism/index/).

To reduce the consumption of disk resources, every index you created should use
well-designed [policy](https://opensearch.org/docs/latest/im-plugin/ism/policies/).

Among others these two index actions might save machine from filling up disk space:

[`Index Rollover`](https://opensearch.org/docs/latest/im-plugin/ism/policies/#rollover) - rolls an alias
to a new index. Set up correctly max index size / age or minimum number of documents to keep index size in requirements
framework.

[`Index Deletion`](https://opensearch.org/docs/latest/im-plugin/ism/policies/#delete) - deletes indexes
managed by policy

Combining these actions and adapting them to data amount and specification, users are able to create policy which will
maintain their data in cluster for example to secure node from fulfilling disk space.

There is an example of such policy below. Be aware that this is only example and as avery example it needs to be adjusted to actual environment needs.

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

Example above shows configuration with rollover index policy on a daily basis or when the index achieve 1 GB size. Indexes older than 14 days will
be deleted. States and conditionals could be combined. Please
see [policies](https://opensearch.org/docs/latest/im-plugin/ism/policies/) documentation for more
details.

#### Apply Policy

To apply a policy you can use similar API request as presented below:

```sh
PUT _index_template/ism_rollover
```

```json
{
  "index_patterns": ["filebeat*"],
  "settings": {
    "plugins.index_state_management.rollover_alias": "filebeat"
    "plugins.index_state_management.policy_id": "epi_policy"
  }
}
```

After applying this policy, every new index created under this one will apply to it. There is also possibility to apply
policy to already existing policies by assigning them to policy in dashboard Index Management panel.

## How to export Dashboards reports

Since v1.0 Epiphany provides the possibility to export reports from Kibana to CSV, PNG or PDF using the Open Distro for Elasticsearch Kibana reports feature. And after migrating from Elastic stack to OpenSearch stack you can make use of the OpenSearch Reporting feature to achieve this and more.

Check more details about the OpenSearch Reports plugin and how to export reports in the
[documentation](https://github.com/opensearch-project/dashboards-reports/blob/main/README.md#opensearch-dashboards-reports).

Notice: Currently in the OpenSearch stack the following plugins are installed and enabled by default: security, alerting, anomaly detection, index management, query workbench, notebooks, reports, alerting, gantt chart plugins.

You can easily check enabled default plugins for Dashboards component using the following command on the logging machine:
`./bin/opensearch-dashboards-plugin list` in directory where you've installed _opensearch-dashboards_.

---

## How to add multiline support for Filebeat logs

In order to properly handle multiline outputs in files harvested by Filebeat you have to provide `multiline` definition in the cluster configuration manifest. Using the following code you will be able to specify which lines are part of a single event.

By default, postgresql block is provided, you can use it as example:

```yaml
[..]
postgresql_input:
  multiline:
    pattern: >-
      '^\d{4}-\d{2}-\d{2} '
    negate: true
    match: after
[..]
```

Supported inputs: `common_input`,`postgresql_input`,`container_input`.
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

## How to use default OpenSearch dashboards

---
This feature is not working in current version of OpenSearch and so the `setup.dashboards.enabled` is set with value _false_ as a workaround.

---
It is possible to configure `setup.dashboards.enabled` and `setup.dashboards.index` Filebeat settings using `specification.kibana.dashboards` key in `configuration/filebeat` doc.
When `specification.kibana.dashboards.enabled` is set to `auto`, the corresponding setting in Filebeat configuration file will be set to `true` only if OpenSearch Dashboards component is configured to be present on the host.
Other possible values are `true` and `false`.

Default configuration:
```yaml
specification:
[..]
  opensearch:
    dashboards:
      enabled: auto
      index: filebeat-*
```

Notice: Setting `specification.kibana.dashboards.enabled` to `true` not providing Kibana will result in a Filebeat crash.

<br>

---
<sup>[1] More information about migrating from Elasticsearch & Kibana to OpenSearch & OpenSearch Dashboards can be found [here](./UPGRADE.md#migration-from-open-distro-for-elasticsearch--kibana-to-opensearch-and-opensearch-dashboards).</sup>

## Audit logs

There is an [option](https://opensearch.org/docs/latest/security-plugin/audit-logs/) to enable
OpenSearch audit logs which is switched on in Epiphany by default using the following configuration part:

```yaml
kind: configuration/logging
specification:
  opensearch_security:
    audit:
      type: internal_opensearch
```

Use the empty string value to switch audit logging off.
