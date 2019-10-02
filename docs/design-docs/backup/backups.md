# Epiphany Platform backup design document

Affected version: 0.4.1

## Goals

Provide backup functionality for Epiphany Platform - cluster created using epicli tool.

Backup will cover following areas:

1. Kubernetes cluster backup
1.1 etcd database
1.2 kubeadm config
1.3 certificates
1.4 persistent volumes
1.5 applications deployed on the cluster
2. Kafka
2.1 Kafka topic data 
2.2 Kafka index
2.3 Zookeeper settings and data
3. Elastic stack
3.1 Elasticsearch data
3.2 Kibana settings
4. Monitoring
4.1 Prometheus data
4.2 Prometheus settings (properties, targets)
4.3 Alertmanager settings
4.4 Grafana settings (datasources, dashboards)
5. PostgreSQL
5.1 All databases from DB
6. RabbitMQ settings and user data
7. HAProxy settings

## Use cases

User/background service/job is able to backup whole cluster or backup selected parts and store files in desired location.
There are few options possible to use for storing backup:
- S3
- Azure file storage
- local file
- NFS

Application/tool will create metadata file that will be definition of the backup - information that can be useful for restore tool. This metadata file will be stored within backup file.

Backup is packed to zip/gz/tar.gz file that has timestamp in the name. If name collision occurred `name+'_1'` will be used.  

## Example use

```bash
epibackup -b /path/to/build/dir -t /target/location/for/backup
```

Where `-b` is path to build folder that contains Ansible inventory and `-t` contains target path to store backup.

## Component View

![Epiphany backup component](backup_component.png)

User/background service/job executes `epibackup` (code name) application. Application takes parameters:
- `-b`: build directory of existing cluster. Most important is ansible inventory existing in this directory - so it can be assumed that this should be folder of Ansible inventory file. 
- `-t`: target location of zip/tar.gz file that will contain backup files and metadata file. 

Tool when executed looks for the inventory file in `-b` location and executes backup playbooks. All playbooks are optional, in MVP version it can try to backup all components (it they exists in the inventory). After that, some components can be skipped (by providing additional flag, or parameter to cli).

Tool also produces metadata file that describes backup with time, backed up components and their versions.
 