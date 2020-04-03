## How to configure Prometheus alerts

More information about Prometheus queries you can find under links provided below:

https://prometheus.io/docs/prometheus/latest/querying/basics/

https://prometheus.io/docs/prometheus/latest/querying/examples/

Right now we are only supporting email messages, but we are working heavily on introducing integration with Slack and Pager Duty.

TODO

## How to setup default admin password and user in Grafana

To use other default user than admin/admin created automatically after Grafana installation please follow official Grafana 
documentation accessible at https://grafana.com/docs/grafana/latest/installation/configuration/#security address. You can also find
there other useful configuration options for Grafana security.

## Import and create of Grafana dashboards

Epiphany uses Grafana for monitoring data visualization. Epiphany installation creates Prometheus datasource in Grafana, so the only additional step you have to do is to create your dashboard.

### Creating dashboards

You can create your own dashboards [Grafana getting started](http://docs.grafana.org/guides/getting_started/) page will help you with it.
Knowledge of Prometheus will be really helpful when creating diagrams since it use [PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/) to fetch data.

### Importing dashboards

There are also many ready to take [Grafana dashboards](https://grafana.com/dashboards) created by community - remember to check license before importing any of those dashboards.
To import existing dashboard:

1. If you have found dashboard that suits your needs you can import it directly to Grafana going to menu item `Dashboards/Manage` in your Grafana web page.
2. Click `+Import` button.
3. Enter dashboard id or load json file with dashboard definition
4. Select datasource for dashboard - you should select `Prometheus`.
5. Click `Import`

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

## How to configure default user password to Kibana - Open Distro and Open Distro for Elasticsearch

To configure default user and password please follow documentation accessible at this: https://aws.amazon.com/blogs/opensource/change-passwords-open-distro-for-elasticsearch/ address.

## How to configure scalable Prometheus setup

If you want to create scalable Prometheus setup you can use federation. Federation lets you scrape metrics from different Prometheus
instances on one Prometheus instance.

In order to create federation of Prometheus add to your configuration (for example to prometheus.yaml
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

## How to configure Azure additional monitoring and alerting

Setting up addtional monitoring on Azure for redundancy is good practice and might catch issues the Epiphany monitoring might miss like:

- Azure issues and resource downtime
- Issues with the VM which runs the Epiphany monitoring and Alerting (Prometheus)

More information about Azure monitoring and alerting you can find under links provided below:

https://docs.microsoft.com/en-us/azure/azure-monitor/overview

https://docs.microsoft.com/en-us/azure/monitoring-and-diagnostics/monitoring-overview-alerts

## How to configure AWS additional monitoring and alerting

TODO
