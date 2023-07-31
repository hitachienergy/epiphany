# Epiphany Process View

## Monitoring

Epiphany uses `Prometheus` and related components for gathering data from
different exporters: `Node-exporter`, `Kafka-exporter`. This
data is stored in `Prometheus`. `Grafana` connects to `Prometheus` to display
metrics from different kinds of exporters.

![Monitoring process view](diagrams/process-view/monitoring-process-view.svg)

`Prometheus` calls `Alertmanager` whenever a configured rule is met to send alerts to the configured notification integrations (like `Slack`, `PagerDuty` or `email`).

## Logging

Epiphany uses `OpenSearch` as key-value database with `Filebeat` for gathering logs and `OpenSearch Dashboards` as user interface to write queries and analyze logs.

![Logging process view](diagrams/process-view/logging-process-view.svg)

`Filebeat` gathers OS and application logs and ships them to `OpenSearch`. Queries from `OpenSearch Dashboards` are run against `OpenSearch` key-value database.
