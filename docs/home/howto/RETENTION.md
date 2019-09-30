An Epiphany cluster has a number of components which log, collect and retain data. To make sure that these do not exceed the usable storage of the machines there running on the following configurations are available.

## Epicli

TODO

## Legacy

### Elasticsearch

For managing the data storage that Elasticsearch consumes we use [Elasticsearch Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.5/about.html). To use it one needs to make sure the elasticsearch-curator is enabled. This role will install and configure the [Elasticsearch Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/5.5/about.html) to run in a cronjob to clean up older indices which are older then a certain treshold.

In the default configuration `/core/src/ansible/roles/elasticsearch-curator/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# Rentention time of Elasticsearch indices in days.
indices_retention_days: 30
```

The size of the storage consumed by Elasticsearch is depenedant on the clustersize and how much logging the deployed application will generate.

### Grafana

In the default configuration `/core/src/ansible/roles/grafana/defaults/main.yml` the following values can be tweaked to control the ammount of storage used by Grafana:

```yaml
# The path where Grafana stores its logs
grafana_logs_dir: "/var/log/grafana"

# The path where Grafana stores it's (Dashboards DB (SQLLite), sessions, etc)
grafana_data_dir: "/var/lib/grafana"

grafana_logging:
# Enable or disable log rotation
log_rotate: true

# Enable or disable daily log rotation
daily_rotate: true

# Number of days to retain the logs
max_days: 7
```

While logs can be rotated and have a retention time, the ammount of storage used by Grafana is dependant on user usage and dashboard count and cannot be directly controlled.

## Kafka

In the default configuration `/core/src/ansible/roles/kafka/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where kafka stores its data
data_dir: /var/lib/kafka

# The path where kafka stores its logs
log_dir: /var/log/kafka

# The minimum age of a log file to be eligible for deletion due to age
log_retention_hours: 168

# Offsets older than this retention period will be discarded
offset_retention_minutes: 10080
```

The ammount of storage Kafka consumes is dependant on the application running on Epiphany, how many messages producers create and how fast the consumers can consume them. It's up to the application developer to configure a `log_retention_hours` and `offset_retention_minutes` to suite the applications need.

Since Kafka does not have a mechanism for log rotation we use [logrotate](https://linux.die.net/man/8/logrotate) for this. The template for logrotate can be found here:

`/core/src/ansible/roles/kafka/templates/logrotate.conf.j2`

On the system the configuration can be found here:

`/etc/logrotate.d/kafka`

### Kibana

In the default configuration `/core/src/ansible/roles/kibana/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where Kibana stores its logs
kibana_log_dir: /var/log/kibana
```

Since Kibana does not have a mechanism for log rotation we use [logrotate](https://linux.die.net/man/8/logrotate) for this. The template for logrotate can be found here:

`/core/src/ansible/roles/kibana/templates/logrotate.conf.j2`

On the system the configuration can be found here:

`/etc/logrotate.d/kibana`

Besides logs any other data is depenedant on user usage (Dashboards, queries etc). Kibana stores that kind of data in ElasticSearch under the `.kibana` index.

### Kubernetes

The kubelet and container runtime (Docker) do not run in containers. On machines with systemd they write to journald.

Everything a containerized application writes to stdout and stderr is redirected to the Docker logging driver (`json-file`), which is configured to rotate logs automatically.

In the default configuration `/core/src/ansible/roles/docker/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
docker_logging:
  log_opts:
    # The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (k, m, or g).
    max_file_size: "10m"
    # The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed.
    max_files: 2
```

On the system the configuration can be found here:

`/etc/docker/daemon.json`

### Prometheus

In the default configuration `/core/src/ansible/roles/prometheus/defaults/main.yml` the following values can be tweaked to control the amount of storage used by Prometheus:

```yaml
# The path where Prometheus stores its data
prometheus_db_dir: /var/lib/prometheus

# The time it will retain the data before it gets deleted
prometheus_storage_retention: "30d"

prometheus_global:
# The interval it will use to scrape the data from the sources
scrape_interval: 15s
```

The size of the data which Prometheus will scrape and retain is dependant on the cluster size (Kafka/Kubernetes nodes) and the scrape interval. The [Prometheus storage documentation](https://prometheus.io/docs/prometheus/latest/storage/) will help you determine how much data might be generated with a certain scrape interval and clustersize. This can then be used to determine a storage retention time in days. Note that one should not plan to use the entire disk space for data retention since it might also be used by other components like Grafana which might be deployed on the same system.

### Zookeeper

In the default configuration `core/src/ansible/roles/zookeeper/defaults/main.yml` the following values can be tweaked regarding storage:

```yaml
# The path where Zookeeper stores its logs
zookeeper_log_dir: /var/log/zookeeper

# The max size a logfile can have
zookeeper_rolling_log_file_max_size: 10MB

# How many logfiles can be retained before rolling over
zookeeper_max_rolling_log_file_count: 10
```
