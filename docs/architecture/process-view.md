# Epiphany Process View

## Computing and Load Balancing

Epiphany strongly utilizes the `Kubernetes` platform and follows its rules and principles.
Read more about `Kubernetes architecture` using this [link](https://kubernetes.io/docs/concepts/architecture/).

Epiphany computing modules use standard implementation of `Kubernetes` and combine it with the load balancing capabilities of `HAProxy`.

![Computing and Load Balancing process view](diagrams/process-view/computing-process-view.svg)

Load balancing integration with `Kubernetes` uses backend configurations. The configurations point to created `Kubernetes services` but this traffic goes through `Kube Proxy` to resolve internal IP address of pod that is currently available.  

## Monitoring

Epiphany uses `Prometheus` and related components for gathering data from
different exporters: `Node-exporter`, `Kafka-exporter`, `HAProxy-exporter`. This
data is stored in `Prometheus`. `Grafana` connects to `Prometheus` to display
metrics from different kinds of exporters.

![Monitoring process view](diagrams/process-view/monitoring-process-view.svg)

`Prometheus` calls `Alertmanager` whenever a configured rule is met to send alerts to the configured notification integrations (like `Slack`, `PagerDuty` or `email`).

## Logging

Epiphany uses `Elasticsearch` as key-value database with `Filebeat` for gathering logs and `Kibana` as user interface to write queries and analyze logs.

![Logging process view](diagrams/process-view/logging-process-view.svg)

`Filebeat` gathers OS and application logs and ships them to `Elasticsearch`. Queries from `Kibana` are run against `Elasticsearch` key-value database.