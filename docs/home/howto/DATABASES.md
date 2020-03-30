## How to migrate from PostgreSQL installed from Software Collections to installed from PostgreSQL repository

This operation is only required for RedHat/CentOS installations with PostgreSQL 10 installed from Software Collections.

This change is required due to additional modules added by Epiphany that are not supported by PostgreSQL installed from Software
Collections, but are supported by PostgreSQL installed from official PostgreSQL repository. That's why PostgreSQL 10 installed from RedHat/CentOS Software Collections needs to be replaced with PostgreSQL 10 installed from PostgreSQL repository.

### PostgreSQL servers

0). Check if package rh-postgresql10-postgresql-server is installed. You can check this with command:

```bash
rpm -qa | grep rh-postgresql10-postgresql-server
```

1). Stop instance of PostgreSQL installed from Software Collections database with command:

```bash
systemctl stop postgresql
```

2). Prepare backup of your PostgreSQL data directory - e.g. with tar command:

```bash
tar -cf backup.tar /var/opt/rh/rh-postgresql10/lib/pgsql/data/
```

But any other tool that will provide you reliable backup that will prevent you from data loss can be chosen.

3). Create new directory for your PostgreSQL with command:

```bash
mkdir -p /var/lib/pgsql/10/data/
```

4). Copy/move content of whole data folder to previously created directory:

```bash
cp -R /var/opt/rh/rh-postgresql10/lib/pgsql/data/* /var/lib/pgsql/10/data/
```

5). Remove unnecessary packages with command:

```bash
yum erase rh-postgresql10-postgresql-server rh-postgresql10-postgresql-contrib rh-postgresql10-postgresql \
rh-postgresql10-postgresql-libs \
rh-postgresql10-runtime yum erase postgresql10-libs
```

6). Change ownership of folder /var/lib/pgsql/ and all folders below to user and group postgres with command:

```bash
chown -R postgres:postgres -R /var/lib/pgsql
```

7). Provide configuration to PostgreSQL component with Epiphany configuration. Please refer to Epiphany HOWTO.md for more details.

### Online mode - Repository server

1). Ensure that on repository server file /tmp/epi-download-requirements/download-requirements-done.flag doesn't exist to force downloading new packages.

### Offline mode - machine to which you want to download packages for airgapped deployment:

1).  Ensure that you have downloaded package that name stars with postgresql10-server. Refer to documentation about airgapped 
installation HOWTO.md(https://github.com/epiphany-platform/epiphany/blob/develop/docs/home/howto/CLUSTER.md#how-to-create-an-epiphany-cluster-on-existing-airgapped-infrastructure)
for more details. If package doesn't exist re-run download-requirements.sh script again.

## How to configure PostgreSQL

To configure PostgreSQL, login to server using ssh and switch to `postgres` user with command:

```bash
sudo -u postgres -i
```

Then configure database server using psql according to your needs and
[PostgreSQL documentation](https://www.postgresql.org/docs/).

## How to configure PostgreSQL replication

In order to configure PostgreSQL replication, add to your data.yaml a block similar to the one below to core section:

```yaml
kind: configuration/postgresql
name: default
title: PostgreSQL
version: 0.4.1
provider: aws
specification:
  replication:
    enabled: yes
    user: your_postgresql_replication_user
    password: your_postgresql_replication_password
    max_wal_senders: 10 # (optional) - default value 5
    wal_keep_segments: 34 # (optional) - default value 32
```
If `enabled` is set to `yes` in `replication`, then Epiphany will automatically create cluster of master and slave server
with replication user with name and password specified in data.yaml.

## How to set up PostgreSQL connection pooling

PostgreSQL connection pooling in Epiphany is served by PGBouncer application. This might be added as a feature if needed.
Simplest configuration runs PGBouncer on PostgreSQL master node. This needs to be enabled in configuration yaml file:

```yaml
kind: configuration/postgresql
...
specification:
  additional_components:
    pgbouncer:
      enabled: yes
  ...
```
PGBouncer listens on standard port 6432. Basic configuration is just template, with very limited access to database. This is because security reasons. [Configuration needs to be tailored according component documentation and stick to security rules and best practices](http://www.pgbouncer.org/).

## How to register database standby in repmgr cluster

If one of database nodes has been recovered to desired state you may want to re-attach it to database cluster. Execute these steps on node which will be attached as standby:

1). Clone data from current primary node:

```bash
repmgr -h current_primary_address -U epi_repmgr_admin -d epi_repmgr standby clone -F
```

2). Register node as stanby

```bash
repmgr -f /etc/repmgr/10/repmgr.conf standby register
```
You may use option --force if this node was registered in cluster before.
For more options see repmgr manual:
https://repmgr.org/docs/4.0/repmgr-standby-register.html

## How to switchover database nodes

For some reason you may want to switchover database nodes (promote standby to primary and demote existing primary to standby).

1). Configure passwordless comunication for postgres user between database nodes using ssh key.

2). Test and tun inistial login between nodes to authenticate host (if host authentication is enabled)

### Execute commands listed below on actual slave node:

3). Confirm that standby you want to promote is registered in repmgr cluster:

```bash
repmgr -f /etc/repmgr/10/repmgr.conf cluster show
```

4). Run command:

```bash
repmgr -f /etc/repmgr/10/repmgr.conf standby switchover
```

5). Run command from step 3 and check status. For more details or troubleshooting see repmgr manual:
https://repmgr.org/docs/4.0/repmgr-standby-switchover.html

## How to set up PostgreSQL audit logging

Audit logging of database activities is available through the PostgreSQL Audit Extension: [pgAudit](https://github.com/pgaudit/pgaudit/blob/REL_10_STABLE/README.md).
It provides session and/or object audit logging via the standard PostgreSQL log.

pgAudit may generate a large volume of logging, which has an impact on performance and log storage.
For this reason, pgAudit is not enabled by default.

To install and configure pgAudit, add to your configuration yaml file a doc similar to the following:

```yaml
kind: configuration/postgresql
title: PostgreSQL
name: default
provider: aws
version: 0.5.2
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

If `specification.extensions.pgaudit.enabled` is set to `yes`, Epiphany will install pgAudit package
and add pgaudit extension to be loaded in [shared_preload_libraries](http://www.postgresql.org/docs/10/static/runtime-config-client.html#GUC-SHARED-PRELOAD-LIBRARIES).
Settings defined in `config_file_parameters` section are populated to Epiphany managed PostgreSQL configuration
file. Using this section, you can also set any additional parameter if needed (e.g. `pgaudit.role`) but keep in mind
that these settings are global.

To configure pgAudit according to your needs, see [pgAudit documentation](https://github.com/pgaudit/pgaudit/blob/REL_10_STABLE/README.md#settings).

Once Epiphany installation is complete, there is one manual action at database level (per each database). Connect to your database
using a client (like psql) and load pgaudit extension into current database by running command:

```sql
CREATE EXTENSION pgaudit;
```

To remove the extension from database, run:

```sql
DROP EXTENSION IF EXISTS pgaudit;
```

## How to start working with OpenDistro for Elasticsearch

OpenDistro for Elasticsearch is [an Apache 2.0-licensed distribution of Elasticsearch enhanced with enterprise security, alerting, SQL](https://opendistro.github.io/for-elasticsearch/). In order to start working with OpenDistro change machines count to value greater than 0 in your cluster configuration:

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

**Default installation will be clustered** - it means, using a configuration like above, Elasticsearch cluster with 2 instances will be created. In order to configure the non-clustered installation of more than one node modify configuration for Open Distro adding:

```yaml
kind: configuration/opendistro-for-elasticsearch
title: OpenDistro for Elasticsearch Config
name: default
specification:
  cluster_name: EpiphanyElastic
  clustered: False
```

Result of this configuration will be one or more independent nodes of OpenDistro.

## How to start working with Apache Ignite Stateful setup

Apache Ignite can be installed in Epiphany if `count` property for `ignite` feature is greater than 0.
Example:

```yaml
    ...
    load_balancer:
      count: 1
    ignite:
      count: 2
    rabbitmq:
      count: 0
    ...
```

Configuration like in this example will create Virtual Machines with Apache Ignite cluster installed.
There is possible to modify configuration for Apache Ignite and plugins used.

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

Property `enabled_plugins` contains list with plugin names that will be enabled.
Property `config` contains xml configuration for Apache Ignite. Important placeholder variable is `IP_LIST_PLACEHOLDER` which will be replaced by automation with list of Apache Ignite nodes for self discovery.

## How to start working with Apache Ignite Stateless setup

Stateless setup of Apache Ignite is done using Kubernetes deployments. This setup uses standard `applications` Epiphany's feature (similar to `auth-service`, `rabbitmq`). To enable stateless Ignite deployment use following document:

```yaml
kind: configuration/applications
title: "Kubernetes Applications Config"
name: default
specification:
  applications:
  - name: ignite-stateless
    image_path: "apacheignite/ignite:2.5.0" # it will be part of the image path: {{local_repository}}/{{image_path}}
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
