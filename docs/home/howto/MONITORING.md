# Table of contents

Prometheus:

- [How to enable provided Prometheus rules](#how-to-enable-provided-prometheus-rules)
- [How to enable Alertmanager](#how-to-enable-alertmanager)
- [How to configure scalable Prometheus setup](#how-to-configure-scalable-prometheus-setup)

Grafana:

- [How to setup default admin password and user in Grafana](#how-to-setup-default-admin-password-and-user-in-grafana)
- [Import and create Grafana dashboards](#import-and-create-grafana-dashboards)

Kibana:

- [How to configure Kibana](#how-to-configure-kibana)
- [How to configure default user password in Kibana](#how-to-configure-default-user-password-in-kibana)

Azure:

- [How to configure Azure additional monitoring and alerting](#how-to-configure-azure-additional-monitoring-and-alerting)

AWS:

- [How to configure AWS additional monitoring and alerting](#how-to-configure-aws-additional-monitoring-and-alerting)

# Prometheus

Prometheus is an open-source monitoring system with a dimensional data model, flexible query language, efficient time series database and modern alerting approach. For more information about the features, components and architecture of Prometheus please refer to [the official documentation](https://prometheus.io/docs/introduction/overview/).

## How to enable provided Prometheus rules

Prometheus role provides the following files with rules:

- common.rules (contain basic alerts like cpu load, disk space, memomory usage etc..)
- container.rules (contain container alerts like container killed, volume usage, volume IO usage etc..)
- kafka.rules (contain kafka alerts like consumer lags,  )
- node.rules (contain node alerts like node status, oom, cpu load, etc..)
- postgresql.rules (contain postgresql alerts like postgresql status, exporter error, dead locks, etc..)
- prometheus.rules (contain additional alerts for monitoring Prometheus itself + Alertmanager)

However, only common rules are enabled by default.
To enable a specific rule you have to meet two conditions:

1. Your infrastructure has to have a specific component enabled (count > 0)
2. You have to set the value to "true" in Prometheus configuration in a manifest:

```shell
kind: configuration/prometheus
...
specification:
  alert_rules:
    common: true
    container: false
    kafka: false
    node: false
    postgresql: false
    prometheus: false
```

For more information about how to setup Prometheus alerting rules, refer to [the official website](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/).

## How to enable Alertmanager

Epiphany provides Alertmanager configuration via configuration manifest. To see default configuration please refer to [default Prometheus configuration file](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/common/defaults/configuration/prometheus.yml).  
To enable Alertmanager you have to modify configuration manifest:

1. Enable Alermanager
2. Enable desired alerting rules
2. Provide at least one receiver

Example:  

```yaml
...
specification:
...
  alertmanager:
    enable: true
    alert_rules:
      common: true
      container: false
      kafka: false
      node: false
      postgresql: false
      prometheus: false
...
    config:
      route:
        receiver: 'email'
      receivers:
        - name: 'email'
          email_configs:
            - to: "test@domain.com"
```

For more details about Alertmanager configuration please refer to [the official documentation](https://prometheus.io/docs/alerting/latest/configuration/)

## How to configure scalable Prometheus setup

If you want to create scalable Prometheus setup you can use federation. Federation lets you scrape metrics from different Prometheus instances on one Prometheus instance.

In order to create a federation of Prometheus add to your configuration (for example to prometheus.yaml
file) of previously created Prometheus instance (on which you want to scrape data from other
Prometheus instances) to `scrape_configs` section:

```yaml
scrape_configs:
  - job_name: federate
    metrics_path: /federate
    params:
      'match[]':
        - '{job=~".+"}'
    honor_labels: true
    static_configs:
    - targets:
      - your-prometheus-endpoint1:9090
      - your-prometheus-endpoint2:9090
      - your-prometheus-endpoint3:9090
      ...
      - your-prometheus-endpointn:9090
```

To check if Prometheus from which you want to scrape data is accessible, you can use a command
like below (on Prometheus instance where you want to scrape data):

`curl -G --data-urlencode 'match[]={job=~".+"}' your-prometheus-endpoint:9090/federate`  

If everything is configured properly and Prometheus instance from which you want to gather data is up
and running, this should return the metrics from that instance.  

# Grafana

Grafana is a multi-platform open source analytics and interactive visualization web application. It provides charts, graphs, and alerts for the web when connected to supported data sources. For more information about Grafana please refer to [the official website](https://grafana.com/).

## How to setup default admin password and user in Grafana

Prior to setup Grafana, please setup in your configuration yaml new password and/or name for your admin user. If not, default
"admin" user will be used with the default password "PASSWORD_TO_CHANGE".

```yaml
kind: configuration/grafana
specification:
  ...
  # Variables correspond to ones in grafana.ini configuration file
  # Security
  grafana_security:
    admin_user: admin
    admin_password: "YOUR_PASSWORD"
  ...
```

More information about Grafana security you can find at https://grafana.com/docs/grafana/latest/installation/configuration/#security address.

## Import and create Grafana dashboards

Epiphany uses Grafana for monitoring data visualization. Epiphany installation creates Prometheus datasource in Grafana, so the only additional step you have to do is to create your dashboard.

### Creating dashboards

You can create your own dashboards [Grafana getting started](https://grafana.com/docs/grafana/latest/getting-started/getting-started/) page will help you with it.
Knowledge of Prometheus will be really helpful when creating diagrams since it use [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) to fetch data.

### Importing dashboards via Grafana GUI

There are also many ready to take [Grafana dashboards](https://grafana.com/dashboards) created by community - remember to check license before importing any of those dashboards.
To import existing dashboard:

1. If you have found dashboard that suits your needs you can import it directly to Grafana going to menu item `Dashboards/Manage` in your Grafana web page.
2. Click `+Import` button.
3. Enter dashboard id or load json file with dashboard definition
4. Select datasource for dashboard - you should select `Prometheus`.
5. Click `Import`

### Importing dashboards via configuration manifest

In order to pull a dashboard from official Grafana website during epicli execution, you have to provide dashboard_id, revision_id and datasource in your manifest:

```yaml
kind: configuration/grafana
specification:
  ...
  grafana_online_dashboards:
    - dashboard_id: '4271'
      revision_id: '3'
      datasource: 'Prometheus'
```

### Enabling predefined Grafana dashboards

Since v1.1.0 Epiphany provides predefined Grafana dashboards. These dashboards are available in online and offline deployment modes.
To enable particular Grafana dashboard, generate configuration manifest with `--full` argument and uncomment desired dashboards:

```yaml
kind: configuration/grafana
specification:
  ...
  grafana_external_dashboards:
  # Kubernetes cluster monitoring (via Prometheus)
    - dashboard_id: '315'
      datasource: 'Prometheus'
  # Node Exporter Server Metrics
    - dashboard_id: '405'
      datasource: 'Prometheus'
```

### Components used for monitoring

There are many monitoring components deployed with Epiphany that you can visualize data from. The knowledge which components are used is important when you look for appropriate dashboard on Grafana website or creating your own query to Prometheus.

List of monitoring components - so called exporters:

- cAdvisor
- HAProxy Exporter
- JMX Exporter
- Kafka Exporter
- Node Exporter
- Zookeeper Exporter

When dashboard creation or import succeeds you will see it on your dashboard list.

`Note: For some dashboards, there is no data to visualize until there is traffic activity for the monitored component.


# Kibana

Kibana is an free and open frontend application that sits on top of the Elastic Stack, providing search and data visualization capabilities for data indexed in Elasticsearch. For more informations about Kibana please refer to [the official website](https://www.elastic.co/what-is/kibana).

## How to configure Kibana - Open Distro

In order to start viewing and analyzing logs with Kibana, you first need to add an index pattern for Filebeat according to the following steps:

1. Goto the `Management` tab
2. Select `Index Patterns`
3. On the first step define as index pattern:
    `filebeat-*`
    Click next.
4. Configure the time filter field if desired by selecting `@timestamp`. This field represents the time that events occurred or were processed. You can choose not to have a time field, but you will not be able to narrow down your data by a time range.

This filter pattern can now be used to query the Elasticsearch indices.

By default Kibana adjusts the UTC time in `@timestamp` to the browser's local timezone. This can be changed in `Management` > `Advanced Settings` > `Timezone for date formatting`.

## How to configure default user passwords for Kibana - Open Distro, Open Distro for Elasticsearch and Filebeat

To configure admin password for Kibana - Open Distro and Open Distro for Elasticsearch you need to follow the procedure below.
There are separate procedures for `logging` and `opendistro-for-elasticsearch` roles since most of the times for `opendistro-for-elasticsearch`, `kibanaserver` and `logstash` users are not required to be present.

### Logging component

#### - Logging role

By default Epiphany removes users that are listed in `demo_users_to_remove` section of `configuration/logging` doc.
By default, `kibanaserver` user (needed by default Epiphany installation of Kibana) and `logstash` (needed by default Epiphany
installation of Filebeat) are not removed. If you want to perform configuration by Epiphany, set `kibanaserver_user_active` to `true`
for `kibanaserver` user or `logstash_user_active` for `logstash` user. For `logging` role, those settings are already set to `true` by default.
We strongly advice to set different password for each user.

To change `admin` user's password, change value for `admin_password` key. For `kibanaserver` and `logstash`, change values
for `kibanaserver_password` and `logstash_password` keys respectively. Changes from logging role will be propagated to Kibana
and Filebeat configuration.

```yaml
kind: configuration/logging
title: Logging Config
name: default
specification:
  ...
  admin_password: YOUR_PASSWORD
  kibanaserver_password: YOUR_PASSWORD
  kibanaserver_user_active: true
  logstash_password: YOUR_PASSWORD
  logstash_user_active: true
  demo_users_to_remove:
  - kibanaro
  - readall
  - snapshotrestore
```

#### - Kibana role

To set password of `kibanaserver` user, which is used by Kibana for communication with Open Distro Elasticsearch backend follow the procedure 
described in [Logging role](#-logging-role).

#### - Filebeat role

To set password of `logstash` user, which is used by Filebeat for communication with Open Distro Elasticsearch backend follow the procedure described 
in  [Logging role](#-logging-role).

### Open Distro for Elasticsearch component

By default Epiphany removes all demo users except `admin` user. Those users are listed in `demo_users_to_remove` section
of `configuration/opendistro-for-elasticsearch` doc. If you want to keep `kibanaserver` user (needed by default Epiphany installation of Kibana),
you need to remove it from `demo_users_to_remove` list and set `kibanaserver_user_active` to `true` in order to change the default password.
We strongly advice to set different password for each user.

To change `admin` user's password, change value for `admin_password` key. For `kibanaserver` and `logstash`, change values for `kibanaserver_password`
and `logstash_password` keys respectively.

```yaml
kind: configuration/opendistro-for-elasticsearch
title: Open Distro for Elasticsearch Config
name: default
specification:
  ...
  admin_password: YOUR_PASSWORD
  kibanaserver_password: YOUR_PASSWORD
  kibanaserver_user_active: false
  logstash_password: YOUR_PASSWORD
  logstash_user_active: false
  demo_users_to_remove:
  - kibanaro
  - readall
  - snapshotrestore
  - logstash
  - kibanaserver
```

### Upgrade of Elasticsearch, Kibana and Filebeat

During upgrade Epiphany takes `kibanaserver` (for Kibana) and `logstash` (for Filebeat) user passwords and re-applies them to upgraded configuration of Filebeat and Kibana. Epiphany upgrade of Open Distro, Kibana or Filebeat will fail if `kibanaserver` or `logstash` usernames were changed in configuration of Kibana, Filebeat or Open Distro for Elasticsearch.

# Azure

## How to configure Azure additional monitoring and alerting

Setting up addtional monitoring on Azure for redundancy is good practice and might catch issues the Epiphany monitoring might miss like:

- Azure issues and resource downtime
- Issues with the VM which runs the Epiphany monitoring and Alerting (Prometheus)

More information about Azure monitoring and alerting you can find under links provided below:

https://docs.microsoft.com/en-us/azure/azure-monitor/overview

https://docs.microsoft.com/en-us/azure/monitoring-and-diagnostics/monitoring-overview-alerts

# AWS

## How to configure AWS additional monitoring and alerting

TODO
