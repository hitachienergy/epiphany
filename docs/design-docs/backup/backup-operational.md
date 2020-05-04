# Epiphany Platform backup design document with details

Affected version: 0.7.x

## Goals

This document is extension of high level design doc: [Epiphany Platform backup design document](https://github.com/epiphany-platform/epiphany/blob/develop/docs/design-docs/backup/backups.md) and describes more detailed, operational point-of-view of this case.
Document does not include Kubernetes and Kafka stack

## Components

### Epibackup application
 Example use:
```bash
epicli backup -b build_dir -t target_path
```

Where `-b` is path to build folder that contains Ansible inventory and `-t` contains target path to store backup.

`backup` runs tasks from ansible backup role

`build_dir` contains cluster's ansible inventory

`target_path` location to store backup, see [Storage](#-Storage) section below.

Consider to add disclaimer for user to check whether backup location has enough space to store whole backup.

### Storage

Location created on master node to keep backup files. This location might be used to mount external storage, like:
- Amazon S3
- Azure blob
- NFS
- Any external disk mounted by administrator

In cloud configuration blob or S3 storage might be mounted directly on every machine in cluster and can be configured by epiphany. For on-prem installation it's up to administrator to attach external disk to backup location on master node. This location should be shared with other machines in cluster as NFS.

### Backup scripts structure:

#### Role backup

Main role for `backup` contains ansible tasks to run backups on cluster components.

#### Tasks:

1. Elasticsearch & Kibana

    1.1. Create local location where snapshot will be stored: /tmp/snapshots
    1.2. Update elasticsearch.yml file with backup location

        ```bash
        path.repo: ["/tmp/backup/elastic"]
        ```
    1.3. Reload configuration
    1.4. Register repository:
    ```bash
    curl -X PUT "https://host_ip:9200/_snapshot/my_backup?pretty" \n
    -H 'Content-Type: application/json' -d '
    {
        "type": "fs",
        "settings": {
        "location": "/tmp/backup/elastic"
        }
    }
    '
    ```
    1.5. Take snapshot:
    ```bash
    curl -X GET "https://host_ip:9200/_snapshot/my_repository/1" \n 
    -H 'Content-Type: application/json'
    ```

    This command will create snapshot in location sent in step 1.2

    1.5. Backup restoration:
    ```bash
    curl -X POST "https://host_ip:9200/_snapshot/my_repository/2/_restore" -H 'Content-Type: application/json'
    ```

    Consider options described in opendistro [documentation](https://opendistro.github.io/for-elasticsearch-docs/docs/elasticsearch/snapshot-restore/#shared-file-system)
    
    1.6. Backup configuration files:
    ```bash
    /etc/elasticsearch/elasticsearch.yml
    /etc/kibana/kibana.yml
     ```   

2. Monitoring
    
    2.1.1 Prometheus data
    
     `Prometheus` delivers solution to create data snapshot. Admin access is required to connect to application api with admin privileges. By default admin access is disabled, and needs to be enabled before snapshot creation.
    To enable admin access `--web.enable-admin-api` needs to be set up while starting service:

    ```bash
    service configuration:
    /etc/systemd/system/prometheus.service

    systemctl daemon-reload
    systemctl restart prometheus
    ```
    Snapshot creation:
    ```bash
    curl -XPOST http://localhost:9090/api/v1/admin/tsdb/snapshot
    ```
    By default snapshot is saved in data directory, which is configured in Prometheus service configuration file as flag:
    ```bash
    --storage.tsdb.path=/var/lib/prometheus
    ```
    Which means that snapshot directory is creted under:
    ```bash
    /var/lib/prometheus/snapshots/yyyymmddThhmmssZ-*
    ```

    After snapshot admin access throuh API should be reverted.

    Snapshot restoration process is just pointing `--storage.tsdb.path` parameter to snaphot location and restart Prometheus.

    2.1.2. Prometheus configuration
    
    Prometheus configurations are located in:
    ```bash
    /etc/prometheus
    ```

    2.2. Grafana backup and restore

    Copy files from grafana home folder do desired location and set up correct permissions:

    ```bash
    location: /var/lib/grafana
    content:
    - dashboards
    - grafana.db
    - plugins
    - png (contains renederes png images - not necessary to back up)
    ```

    2.3 Alert manager

    Configuration files are located in:
    ```bash
    /etc/prometheus
    ```
    File `alertmanager.yml` should be copied in step 2.1.2 if exists
3. PostgreSQL

    3.1. Basically PostgreSQL delivers two main tools for backup creation: pg_dump and pg_dumpall

    `pg_dump` create dump of selected database:

    ```bash
    pg_dump dbname > dbname.bak
    ```
    `pg_dumpall` - create dump of all databases of a cluster into one script. This dumps also global objects that are common to all databases like: users, groups, tablespaces and properties such as access permissions (pg_dump does not save these objects)
    ```bash
    pg_dumpall > pg_backup.bak
    ```
    3.2. Database resotre: psql or pg_restore:
    ```bash
    psql < pg_backup.bak
    pgrestore -d dbname db_name.bak
    ```

    3.3. Copy configuration files:
    ```bash
    /etc/postgresql/10/main/* - configuration files
    .pgpass - authentication credentials

    ```

4. RabbitMQ

    4.1. RabbitMQ definicions might be exported using API (rabbitmq_management plugins need to be enabled):

    ```bash
    rabbitmq-plugins enable rabbitmq_management
    curl -v -X GET http://localhost:15672/api/definitions -u guest:guest -H "content-type:application/json" -o json
    ```

    Import backed up definitions:
    ```bash
    curl -v -X POST http://localhost:15672/api/definitions -u guest:guest -H "content-type:application/json" --data backup.json
    ```
    or add backup location to configuration file and restart rabbitmq:
    ```bash
    management.load_definitions = /path/to/backup.json
    ```
    4.2 Backing up RabbitMQ messages
    To back up messages RabbitMQ must be stopped. Copy content of rabbitmq mnesia directory:
    ```bash
    RABBITMQ_MNESIA_BASE

    ubuntu:
    /var/lib/rabbitmq/mnesia
    ```
    Restoration: place these files to similar location

    4.3 Backing up configuration:

    Copy `/etc/rabbitmq/rabbitmq.conf` file

5. HAProxy

Copy ```/etc/haproxy/``` to backup location

Copy certificates stored in ``` /etc/ssl/haproxy/``` location.

