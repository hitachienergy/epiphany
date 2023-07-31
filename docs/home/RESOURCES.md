# Resources

Here are some materials concerning Epiphany tooling and cluster components - both on what we use in the background and on what's available for you to use with your application/deployment.

## Tooling

1. [Visualstudio Code](https://code.visualstudio.com/)
    - [Devcontainers](https://code.visualstudio.com/docs/remote/containers)
2. [Python 3.7](https://docs.python.org/3.7/)
    - [Docs and tutorials](https://docs.python.org/3/tutorial/)
3. [Terraform](https://www.terraform.io/)
    - AWS use case [example](https://learn.hashicorp.com/terraform/getting-started/build.html)
    - Azure use case [example](https://learn.hashicorp.com/terraform?track=azure#azure)
4. [Ansible](https://www.ansible.com/)
    - [Introduction to playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html)
5. [Azure-cli](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
6. [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Cluster Components

1. Monitoring
    1. [Prometheus](https://prometheus.io/)
        - Query [examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
        - [Integration with Grafana](https://prometheus.io/docs/visualization/grafana/)
        - Included [OS mectric collector](https://github.com/prometheus/node_exporter)
        - Kafka monitoring with [JMX exporter](https://github.com/prometheus/jmx_exporter)
        - Alertmanager [Alerts from Prometheus](https://prometheus.io/docs/alerting/alertmanager/)
    2. [Grafana](https://grafana.com/)
        - Community supplied, ready to use [dashboards](https://grafana.com/dashboards)
2. Messaging
    1. [Kafka](http://kafka.apache.org/)
        - [Kafka introduction](http://kafka.apache.org/intro)
        - (Pluralsight) [Getting Started with Apache Kafka](https://app.pluralsight.com/library/courses/apache-kafka-getting-started/table-of-contents)
3. Central logging
    1. [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/index/)
    2. [OpenSearch](https://opensearch.org/docs/latest)
    3. [Filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/index.html)
        - Beats platform reference(https://www.elastic.co/guide/en/beats/libbeat/current/index.html)
