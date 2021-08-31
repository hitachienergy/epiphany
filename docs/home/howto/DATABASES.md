## How to configure PostgreSQL

To configure PostgreSQL, login to server using ssh and switch to `postgres` user with command:

```bash
sudo -u postgres -i
```

Then configure database server using psql according to your needs and
[PostgreSQL documentation](https://www.postgresql.org/docs/).

## PostgreSQL passwords encryption

Epiphany sets up MD5 password encryption. Although PostgreSQL since version 10 is able to use SCRAM-SHA-256 password encryption, Epiphany does not support this encryption method since recommended production configuration uses more than one database host with HA configuration (repmgr) cooperating with PgBouncer and Pgpool. Pgpool is not able to parse SCRAM-SHA-256 hashes list while this encryption is enabled. Due to limited Pgpool authentication options, it is not possible to refresh the [pool_passwd](https://www.pgpool.net/docs/42/en/html/auth-methods.html#AUTH-SCRAM) file automatically.
For this reason, MD5 password encryption is set up and this is not configurable in Epiphany.

## How to set up PostgreSQL connection pooling

PostgreSQL connection pooling in Epiphany is served by PgBouncer application. It is available as Kubernetes `ClusterIP` or standalone package.
The [Kubernetes based installation](#how-to-set-up-pgbouncer-pgpool-and-postgresql-parameters) works together with PgPool so it supports PostgreSQL HA setup.
The standalone installation (described below) is deprecated and **will be removed** in the next release.

---
**NOTE**

PgBouncer extension is not supported on ARM.

---

PgBouncer is installed only on PostgreSQL primary node. This needs to be enabled in configuration yaml file:

```yaml
kind: configuration/postgresql
specification:
  extensions:
    ...
    pgbouncer:
      enabled: yes
    ...
```

PgBouncer listens on standard port 6432. Basic configuration is just template, with very limited access to database.
This is because of security reasons. [Configuration needs to be tailored according component documentation and stick to security rules and best practices](http://www.pgbouncer.org/).

## How to set up PostgreSQL HA replication with repmgr cluster

---
**NOTE**

Replication (repmgr) extension is not supported on ARM.

---

This component can be used as a part of PostgreSQL clustering configured by Epiphany. In order to configure PostgreSQL
HA replication, add to your configuration file a block similar to the one below to core section:

```yaml
---
kind: configuration/postgresql
name: default
title: PostgreSQL
specification:
  config_file:
    parameter_groups:
      ...
      # This block is optional, you can use it to override default values
    - name: REPLICATION
      subgroups:
      - name: Sending Server(s)
        parameters:
        - name: max_wal_senders
          value: 10
          comment: maximum number of simultaneously running WAL sender processes
          when: replication
        - name: wal_keep_size
          value: 500
          comment: the size of WAL files held for standby servers (MB)
          when: replication
      - name: Standby Servers
        parameters:
        - name: hot_standby
          value: 'on'
          comment: must be 'on' for repmgr needs, ignored on primary but recommended
            in case primary becomes standby
          when: replication
  extensions:
    ...
    replication:
      enabled: true
      replication_user_name: epi_repmgr
      replication_user_password: PASSWORD_TO_CHANGE
      privileged_user_name: epi_repmgr_admin
      privileged_user_password: PASSWORD_TO_CHANGE
      repmgr_database: epi_repmgr
      shared_preload_libraries:
      - repmgr
    ...
```

If `enabled` is set to `true` for `replication` extension, Epiphany will automatically create a cluster of primary and
secondary server with replication user with name and password specified in configuration file. This is only possible for
configurations containing two PostgreSQL servers.

Privileged user is used to perform full backup of primary instance and replicate this at the beginning to secondary
node. After that for replication only replication user with limited permissions is used for WAL replication.

## How to stop PostgreSQL service in HA cluster

In order to maintenance work sometimes PostgreSQL service needs to be stopped. Before this action repmgr service needs to be paused, see [manual page](https://repmgr.org/docs/dev/repmgrd-pausing.html) before. When repmgr service is paused steps from [PostgreSQL manual page](https://www.postgresql.org/docs/current/app-pg-ctl.html) may be applied or stop it as a regular systemd service.

## How to register database standby in repmgr cluster

If one of database nodes has been recovered to desired state, you may want to re-attach it to database cluster. Execute
these steps on node which will be attached as standby:

1. Clone data from current primary node:

```bash
repmgr standby clone -h CURRENT_PRIMARY_ADDRESS -U epi_repmgr_admin -d epi_repmgr --force
```

2. Register node as standby

```bash
repmgr standby register
```

You may use option --force if the node was registered in cluster before. For more options, see repmgr manual:
https://repmgr.org/docs/5.2/repmgr-standby-register.html

## How to switchover database nodes

For some reason you may want to switchover database nodes (promote standby to primary and demote existing primary to
standby).

1. Configure passwordless SSH communication for postgres user between database nodes.

2. Test and run initial login between nodes to authenticate host (if host authentication is enabled).

Execute commands listed below on actual standby node

3. Confirm that standby you want to promote is registered in repmgr cluster:

```bash
repmgr cluster show
```

4. Run switchover:

```bash
repmgr standby switchover
```

5. Run command from step 3 and check status. For more details or troubleshooting, see repmgr manual:
   https://repmgr.org/docs/5.2/repmgr-standby-switchover.html

## How to set up PgBouncer, PgPool and PostgreSQL parameters

This section describes how to set up connection pooling and load balancing for highly available PostgreSQL cluster. The
default configuration provided by Epiphany is meant for midrange class systems but can be customized to scale up or to
improve performance.

To adjust the configuration to your needs, you can refer to the following documentation:

Component | Documentation URL |
--- | --- |
PgBouncer | https://www.pgbouncer.org/config.html |
PgPool: Performance Considerations | https://www.pgpool.net/docs/41/en/html/performance.html |
PgPool: Server Configuration | https://www.pgpool.net/docs/41/en/html/runtime-config.html |
PostgreSQL: connections | https://www.postgresql.org/docs/10/runtime-config-connection.html |
PostgreSQL: resources management | https://www.postgresql.org/docs/10/runtime-config-resource.html |

### Installing PgBouncer and PgPool

---
**NOTE**

PgBouncer and PgPool Docker images are not supported for ARM. If these applications are enabled in configuration,
installation will fail.

---

PgBouncer and PgPool are provided as K8s deployments. By default, they are not installed. To deploy them you need to
add "configuration/applications" document to your configuration yaml file, similar to the example below (`enabled` flags
must be set as `true`):

```yaml
---
kind: configuration/applications
version: 0.6.0
title: "Kubernetes Applications Config"
provider: aws
name: default
specification:
  applications:
  ...

## --- pgpool ---

  - name: pgpool
    enabled: true
    ...
    namespace: postgres-pool
    service:
      name: pgpool
      port: 5432
    replicas: 3
    ...
    resources: # Adjust to your configuration, see https://www.pgpool.net/docs/42/en/html/resource-requiremente.html
      limits:
        # cpu: 900m # Set according to your env
        memory: 176Mi
      requests:
        cpu: 250m # Adjust to your env, increase if possible
        memory: 176Mi
    pgpool:
      # https://github.com/bitnami/bitnami-docker-pgpool#configuration + https://github.com/bitnami/bitnami-docker-pgpool#environment-variables
      env:
        PGPOOL_BACKEND_NODES: autoconfigured # you can use custom value like '0:pg-node-1:5432,1:pg-node-2:5432'
        # Postgres users
        PGPOOL_POSTGRES_USERNAME: epi_pgpool_postgres_admin # with SUPERUSER role to use connection slots reserved for superusers for K8s liveness probes, also for user synchronization
        PGPOOL_SR_CHECK_USER: epi_pgpool_sr_check # with pg_monitor role, for streaming replication checks and health checks
        # ---
        PGPOOL_ADMIN_USERNAME: epi_pgpool_admin # Pgpool administrator (local pcp user)
        PGPOOL_ENABLE_LOAD_BALANCING: false # set to 'false' if there is no replication
        PGPOOL_MAX_POOL: 4
        PGPOOL_CHILD_LIFE_TIME: 0
        PGPOOL_POSTGRES_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_postgres_password
        PGPOOL_SR_CHECK_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_sr_check_password
        PGPOOL_ADMIN_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_admin_password
      secrets:
        pgpool_postgres_password: PASSWORD_TO_CHANGE
        pgpool_sr_check_password: PASSWORD_TO_CHANGE
        pgpool_admin_password: PASSWORD_TO_CHANGE
      # https://www.pgpool.net/docs/42/en/html/runtime-config.html
      pgpool_conf_content_to_append: |
        #------------------------------------------------------------------------------
        # CUSTOM SETTINGS (appended by Epiphany to override defaults)
        #------------------------------------------------------------------------------
        # num_init_children = 32
        connection_life_time = 600
        reserved_connections = 1
      # https://www.pgpool.net/docs/41/en/html/auth-pool-hba-conf.html
      pool_hba_conf: autoconfigured

## --- pgbouncer ---

  - name: pgbouncer
    enabled: true
    ...
    namespace: postgres-pool
    service:
      name: pgbouncer
      port: 5432
    replicas: 2
    resources:
      requests:
        cpu: 250m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 128Mi
    pgbouncer:
      env:
        DB_HOST: pgpool.postgres-pool.svc.cluster.local
        DB_LISTEN_PORT: 5432
        MAX_CLIENT_CONN: 150
        DEFAULT_POOL_SIZE: 25
        RESERVE_POOL_SIZE: 25
        POOL_MODE: transaction
```

### Default setup - main parameters

This chapter describes the default setup and main parameters responsible for the performance limitations. The
limitations can be divided into 3 layers: resource usage, connection limits and query caching. All the configuration
parameters can be modified in the configuration yaml file.

#### Resource usage

Each of the components has hardware requirements that depend on its configuration, in particular on the number of
allowed connections.

##### PgBouncer

```yaml
replicas: 2
resources:
  requests:
    cpu: 250m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 128Mi
```

##### PgPool

```yaml
replicas: 3
resources: # Adjust to your configuration, see https://www.pgpool.net/docs/41/en/html/resource-requiremente.html
  limits:
    # cpu: 900m # Set according to your env
    memory: 176Mi
  requests:
    cpu: 250m # Adjust to your env, increase if possible
    memory: 176Mi
```

By default, each PgPool pod requires 176 MB of memory. This value has been determined based on
PgPool [docs](https://www.pgpool.net/docs/41/en/html/resource-requiremente.html), however after stress testing we need
to add several extra megabytes to
avoid [failed to fork a child](https://github.com/epiphany-platform/epiphany/pull/1123) issue. You may need to
adjust `resources` after changing `num_init_children` or `max_pool` (`PGPOOL_MAX_POOL`) settings. Such changes should be
synchronized with PostgreSQL and PgBouncer configuration.

##### PostgreSQL

Memory related parameters have PostgreSQL default values. If your setup requires performance improvements, you may
consider changing values of the following parameters:

- shared_buffers
- work_mem
- maintenance _work_mem
- effective_cache_size
- temp_buffers

The default settings can be overridden by Epiphany using `configuration/postgresql` doc in the configuration yaml file.

#### Connection limits

##### PgBouncer

There are connection limitations defined in PgBouncer configuration. Each of these parameters is defined per PgBouncer
instance (pod). For example, having 2 pods (with MAX_CLIENT_CONN = 150) allows for up to 300 client connections.

```yaml
    pgbouncer:
      env:
        ...
        MAX_CLIENT_CONN: 150
        DEFAULT_POOL_SIZE: 25
        RESERVE_POOL_SIZE: 25
        POOL_MODE: transaction
```

##### PgPool

By default, PgPool service is configured to handle up to 93 active concurrent connections to PostgreSQL (3 pods x 31).
This is because of the following settings:

```
num_init_children = 32
reserved_connections = 1
```

Each pod can handle up to 32 concurrent connections but one
is [reserved](https://www.pgpool.net/docs/41/en/html/runtime-config-connection.html#GUC-NUM-INIT-CHILDREN). This means
that the 32nd connection from a client will be refused. Keep in mind that canceling a query creates another connection
to PostgreSQL, thus, a query cannot be canceled if all the connections are in use. Furthermore, for each pod, one
connection slot must be available for K8s health checks. Hence, the real number of available concurrent connections is
30 per pod.

If you need more active concurrent connections, you can increase the number of pods (`replicas`), but the total number
of allowed concurrent connections should not exceed the value defined by PostgreSQL parameters: (`max_connections` - `superuser_reserved_connections`).

In order to change PgPool settings (defined in pgpool.conf), you can edit `pgpool_conf_content_to_append` section:

```yaml
pgpool_conf_content_to_append: |
  #------------------------------------------------------------------------------
  # CUSTOM SETTINGS (appended by Epiphany to override defaults)
  #------------------------------------------------------------------------------
  connection_life_time = 900
  reserved_connections = 1
```

The content of pgpool.conf file is stored in K8s `pgpool-config-files` ConfigMap.

For detailed information about connection tuning, see "Performance Considerations" chapter in PgPool documentation.

##### PostgreSQL

PostgreSQL uses `max_connections` parameter to limit the number of client connections to database server. The default is
typically 100 connections. Generally, PostgreSQL on sufficient amount of hardware can support a few hundred connections.

#### Query caching

Query caching is not available in PgBouncer.

##### PgPool

Query caching is disabled by default in PgPool configuration.

##### PostgreSQL

PostgreSQL is installed with default settings.

## How to set up PostgreSQL audit logging

Audit logging of database activities is available through the PostgreSQL Audit
Extension: [PgAudit](https://github.com/pgaudit/pgaudit/blob/REL_10_STABLE/README.md). It provides session and/or object
audit logging via the standard PostgreSQL log.

PgAudit may generate a large volume of logging, which has an impact on performance and log storage. For this reason,
PgAudit is not enabled by default.

To install and configure PgAudit, add to your configuration yaml file a doc similar to the following:

```yaml
kind: configuration/postgresql
title: PostgreSQL
name: default
provider: aws
version: 1.0.0
specification:
  extensions:
    pgaudit:
      enabled: yes
      config_file_parameters:
        ## postgresql standard
        log_connections: 'off'
        log_disconnections: 'off'
        log_statement: 'none'
        log_line_prefix: "'%m [%p] %q%u@%d,host=%h '"
        ## pgaudit specific, see https://github.com/pgaudit/pgaudit/blob/REL_10_STABLE/README.md#settings
        pgaudit.log: "'write, function, role, ddl' # 'misc_set' is not supported for PG 10"
        pgaudit.log_catalog: 'off # to reduce overhead of logging'
        # the following first 2 parameters are set to values that make it easier to access audit log per table
        # change their values to the opposite if you need to reduce overhead of logging
        pgaudit.log_relation: 'on # separate log entry for each relation'
        pgaudit.log_statement_once: 'off'
        pgaudit.log_parameter: 'on'
```

If `enabled` property for PgAudit extension is set to `yes`, Epiphany will install PgAudit package and add PgAudit
extension to be loaded
in [shared_preload_libraries](http://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES)
. Settings defined in `config_file_parameters` section are populated to Epiphany managed PostgreSQL configuration file.
Using this section, you can also set any additional parameter if needed (e.g. `pgaudit.role`) but keep in mind that
these settings are global.

To configure PgAudit according to your needs,
see [PgAudit documentation](https://github.com/pgaudit/pgaudit/blob/REL_10_STABLE/README.md#settings).

Once Epiphany installation is complete, there is one manual action at database level (per each database). Connect to
your database using a client (like psql) and load PgAudit extension into current database by running command:

```sql
CREATE EXTENSION pgaudit;
```

To remove the extension from database, run:

```sql
DROP EXTENSION IF EXISTS pgaudit;
```

## How to work with PostgreSQL connection pooling

PostgreSQL connection pooling is described in [design documentaion page](https://github.com/epiphany-platform/epiphany/blob/develop/docs/design-docs/postgresql/connection-pooling.md).
Properly configured application (kubernetes service) to use fully HA configuration should be set up to connect to pgbouncer service (kubernetes) instead directly to database host. This configuration provides all the benefits of user PostgreSQL in clusteres HA mode (including database failover). Both pgbouncer and pgpool stores database users and passwords in configuration files and needs to be restarted (pods) in case of PostgreSQL authentication changes like: create, alter username or password. Pods during restart process are refreshing stored database credentials automatically.

## How to configure PostgreSQL replication

#### Note

PostgreSQL native replication is now deprecated and removed.
Use [PostgreSQL HA replication with repmgr](#how-to-set-up-postgresql-ha-replication-with-repmgr-cluster) instead.

## How to start working with OpenDistro for Elasticsearch

OpenDistro for Elasticsearch
is [an Apache 2.0-licensed distribution of Elasticsearch enhanced with enterprise security, alerting, SQL](https://opendistro.github.io/for-elasticsearch/).
In order to start working with OpenDistro change machines count to value greater than 0 in your cluster configuration:

```yaml
kind: epiphany-cluster
...
specification:
  ...
  components:
    kubernetes_master:
      count: 1
      machine: aws-kb-masterofpuppets
    kubernetes_node:
      count: 0
    ...
    logging:
      count: 1
    opendistro_for_elasticsearch:
      count: 2
```

**Installation with more than one node will always be clustered** - Option to configure the non-clustered installation of more than one node for Open Distro is not supported.

```yaml
kind: configuration/opendistro-for-elasticsearch
title: OpenDistro for Elasticsearch Config
name: default
specification:
  cluster_name: EpiphanyElastic
```

By default, Kibana is deployed only for `logging` component. If you want to deploy Kibana
for `opendistro_for_elasticsearch` you have to modify feature mapping. Use below configuration in your manifest.

```yaml
kind: configuration/feature-mapping
title: "Feature mapping to roles"
name: default
specification:
  roles_mapping:
    opendistro_for_elasticsearch:
      - opendistro-for-elasticsearch
      - node-exporter
      - filebeat
      - firewall
      - kibana
```

Filebeat running on `opendistro_for_elasticsearch` hosts will always point to centralized logging hosts (./LOGGING.md).

## How to start working with Apache Ignite Stateful setup

Apache Ignite can be installed in Epiphany if `count` property for `ignite` feature is greater than 0. Example:

```yaml
kind: epiphany-cluster
specification:
  components:
    load_balancer:
      count: 1
    ignite:
      count: 2
    rabbitmq:
      count: 0
    ...
```

Configuration like in this example will create Virtual Machines with Apache Ignite cluster installed. There is possible
to modify configuration for Apache Ignite and plugins used.

```yaml
kind: configuration/ignite
title: "Apache Ignite stateful installation"
name: default
specification:
  version: 2.7.6
  file_name: apache-ignite-2.7.6-bin.zip
  enabled_plugins:
  - ignite-rest-http
  config: |
    <?xml version="1.0" encoding="UTF-8"?>

    <!--
      Licensed to the Apache Software Foundation (ASF) under one or more
      contributor license agreements.  See the NOTICE file distributed with
      this work for additional information regarding copyright ownership.
      The ASF licenses this file to You under the Apache License, Version 2.0
      (the "License"); you may not use this file except in compliance with
      the License.  You may obtain a copy of the License at
          http://www.apache.org/licenses/LICENSE-2.0
      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
      See the License for the specific language governing permissions and
      limitations under the License.
    -->

    <beans xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="
          http://www.springframework.org/schema/beans
          http://www.springframework.org/schema/beans/spring-beans.xsd">

        <bean id="grid.cfg" class="org.apache.ignite.configuration.IgniteConfiguration">
          <property name="dataStorageConfiguration">
            <bean class="org.apache.ignite.configuration.DataStorageConfiguration">
              <!-- Set the page size to 4 KB -->
              <property name="pageSize" value="#{4 * 1024}"/>
              <!--
              Sets a path to the root directory where data and indexes are
              to be persisted. It's assumed the directory is on a separated SSD.
              -->
              <property name="storagePath" value="/var/lib/ignite/persistence"/>

              <!--
                  Sets a path to the directory where WAL is stored.
                  It's assumed the directory is on a separated HDD.
              -->
              <property name="walPath" value="/wal"/>

              <!--
                  Sets a path to the directory where WAL archive is stored.
                  The directory is on the same HDD as the WAL.
              -->
              <property name="walArchivePath" value="/wal/archive"/>
            </bean>
          </property>

          <property name="discoverySpi">
            <bean class="org.apache.ignite.spi.discovery.tcp.TcpDiscoverySpi">
              <property name="ipFinder">
                <bean class="org.apache.ignite.spi.discovery.tcp.ipfinder.vm.TcpDiscoveryVmIpFinder">
                  <property name="addresses">
                  IP_LIST_PLACEHOLDER
                  </property>
                </bean>
              </property>
            </bean>
          </property>
        </bean>
    </beans>
```

Property `enabled_plugins` contains list with plugin names that will be enabled. Property `config` contains xml
configuration for Apache Ignite. Important placeholder variable is `IP_LIST_PLACEHOLDER` which will be replaced by
automation with list of Apache Ignite nodes for self discovery.

## How to start working with Apache Ignite Stateless setup

Stateless setup of Apache Ignite is done using Kubernetes deployments. This setup uses standard `applications`
Epiphany's feature (similar to `auth-service`, `rabbitmq`). To enable stateless Ignite deployment use following
document:

```yaml
kind: configuration/applications
title: "Kubernetes Applications Config"
name: default
specification:
  applications:
  - name: ignite-stateless
    image_path: "epiphanyplatform/ignite:2.9.1" # it will be part of the image path: {{local_repository}}/{{image_path}}
    namespace: ignite
    service:
      rest_nodeport: 32300
      sql_nodeport: 32301
      thinclients_nodeport: 32302
    replicas: 1
    enabled_plugins:
    - ignite-kubernetes # required to work on K8s
    - ignite-rest-http
```

Adjust this config to your requirements with number of replicas and plugins that should be enabled.
