## How to configure PostgreSQL

To configure PostgreSQL login to server using ssh and switch to postgres user with command:

```bash
sudo -u postgres -i
```

And then configure database server using psql according to your needs and
PostgreSQL documentation, to which link you can find at [here](https://www.postgresql.org/docs/)

## How to configure PostgreSQL replication

In order to configure PostgreSQL replication add to your data.yaml a block similar to the one below to core section:

```yaml
kind: configuration/postgresql
name: default
title: Postgresql
version: 0.4.1
provider: aws
specification:
  replication:
    enable: yes
    user: your-postgresql-replication-user
    password: your-postgresql-replication-password
    max_wal_senders: 10 # (optional) - default value 5
    wal_keep_segments: 34 # (optional) - default value 32
  version: '10'
```
If enable is set to yes in replication then Epiphany will automatically create cluster of master and slave server with replication user with name and password
specified in data.yaml.
