## Epiphany backup and restore

### Introduction

Epiphany provides solution to create full or partial backup and restore for some components, like:

- [Load Balancer](#load-balancer)
- [Logging](#logging)
- [Monitoring](#monitoring)
- [Postgresql](#postgresql)
- [RabbitMQ](#rabbitmq)
- [Kubernetes (only backup)](#kubernetes)

Backup is created directly on machine where component is running, and is moved to ``repository`` host rsync. On ``repository`` host backup files are stored in location ``/epibackup/mounted`` on local. 
See [How to store backup](#2.-How-to-store-backup) chapter.

## 1. How to perform backup

#### Run one-line epicli:

Run epicli backup with option ``-c`` passing component to back up :
```
epicli backup -f cluster-config.yml -b build_folder -c list,of,components
```
where ``-c`` might be list one or more comma separated components:
```
- c load_balancer,logging,monitoring,postgresql,rabbitmq
```

#### Create static configuration

Enalbe backup for chosen components by setting up ``enabled`` parameter according your needs. Copy default configuration for backup from ``defaults/configuration/backup.yml`` into basic data yaml and modify ``enabled`` value.

```
kind: configuration/backup
title: Backup Config
name: default
specification:
  components:
    load_balancer:
      enabled: true
    logging:
      enabled: false
    monitoring:
      enabled: true
    postgresql:
      enabled: true
    rabbitmq:
      enabled: false
#Kubernes backup and recovery is not supported by Epiphany.
#You may create backup by enabling this below, but recovery should be done manually according Kubernetes documentation.
    kubernetes:
      enabled: false
```

Run ``epicli backup`` command:

``epicli backup -f cluster-config.yml -b build_folder``

In this case no need to pass parameter ``-c`` but if provided this will overwrite state from cluster-config.yml

## 2. How to store backup

Backup location is defined in ``backup`` role as ``backup_destination_host`` and ``backup_destination_dir``.
Default backup location is defined on ``repository`` host in location ``/epibackup/mounted/``.
Use ``mounted`` location as mount point and mount storage you want to use. This might be:
- Azure Blob Storage
- Amazon S3
- NAS
- Any other attached storage

Ensure that mounted location has enought space, is reliable and is well protected against disaster.

### If you don't attach any storage into mount point location be aware thet backups will be store on local machine. This is not recommended.

## 3. How to perform recovery

Similar to backup, recovery might be run two ways:

### One-line epicli recovery command

Run one-liner with option ``-c`` and pass component to recover:
```
epicli recovery -f cluster-config.yml -b build_folder -c list,of,components
```
where ``-c`` might be list one or more comma separated components:
```
- c load_balancer,logging,monitoring,postgresql,rabbitmq
```
Command above will restore atest backup for selected component

### Create static recovery configuration

Enable recovery for chosen components by setting up ``enabled`` parameter according your needs. Copy default configuration for backup from ``defaults/configuration/recovery.yml`` into basic data yaml and enable components to recover. It's possible to choose snapshot name according by passing date and time part of snaphot name. If snapshot name is not provided, the latest one will be restored.

```
kind: configuration/recovery
title: Recovery Config
name: default
specification:
  components:
    load_balancer:
      enabled: true
      snapshot_name: latest           #restore latest backup
    logging:
      enabled: true
      snapshot_name: 20200604-150829  #restore selected backup
    monitoring:
      enabled: false
      snapshot_name: latest
    postgresql:
      enabled: false
      snapshot_name: latest
    rabbitmq:
      enabled: false
      snapshot_name: latest
```

Run ``epicli recovery`` command:

``epicli recovery -f cluster-config.yml -b build_folder``

In this case no need to pass parameter ``-c`` but if provided this will overwrite state from cluster-config.yml

## 4. How backup and recovery work

### Load Balancer

Load balancer backup includes:
- Configuration files: ``/etc/haproxy/``
- SSL certificates: ``/etc/ssl/haproxy/``

Recovery includes all backed up files


### Logging

Logging backup includes:
- Elasticsearch database snapshot
- Elasticsearch configuration ``/etc/elasticsearch/``
- Kibana configuration ``/etc/kibana/``

Only single-node Elasticsearch backup is supported. Solution for multi-node Elasticsearch cluster will be added in future release.

### Monitoring
Monitoring backup includes:
- Prometheus data snapshot
- Prometheus configuration ``/etc/prometheus/``
- Grafana data snapshot

Recovery includes all backed up configurations and snapshots.

### Postgresql
Postgresql backup includes:
- Database data and metadata dump using ``pg_dumpall``
- Configuration files: ``*.conf``

When multinode configuration is used, and faileover action has changed database cluster status (one node down, switchover) it's still possible to create backup. But before database restore, cluster needs to be recovered by run ``epicli apply`` and next ``epicli recovery`` to restore database data.
By default we don't support recovery database configuration from backup since this needs to be done using ``epicli apply`` or manually by copying backed up files accordingly to cluster state. The reason of this is that is very risky to restore configuration files among different database cluster configurations.

### RabbitMQ
RabbitMQ backup includes:
- Messages definitions
- Configuration files ``/etc/rabbitmq/

Backup does not include RabbitMQ messages.

Recovery includes all backed up files and configurations.

### Kubernetes
- Etcd snapshot
- Public Key Infrastructure ``/etc/kubernetes/pki``
- Kubeadm configuration files

Epiphany does not support Kubernetes cluster recovery. Use Kubernetes documentation for manual recovery.