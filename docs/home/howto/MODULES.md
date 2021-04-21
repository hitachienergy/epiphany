# Modules

## Introduction

In version 0.8 of Epiphany we introduced modules. Modularization of Epiphany environment will result in:

* smaller code bases for separate areas,
* simpler and faster test process,
* interchangeability of elements providing similar functionality (eg.: different Kubernetes providers),
* faster and more focused release cycle.

Those and multiple other factors (eg.: readability, reliability) influence this direction of changes.

## User point of view

From a user point of view, there will be no significant changes in the nearest future as it will be still possible to install Epiphany "classic way" so with a single `epicli` configuration using a whole codebase as a monolith.

For those who want to play with new features, or will need newly introduced possibilities, there will be a short transition period which we consider as a kind of "preview stage". In this period there will be a need to run each module separately by hand in the following order:

* moduleA init
* moduleA plan
* moduleA apply
* moduleB init
* moduleB plan
* moduleB apply
* ...

Init, plan and apply phases explanation you'll find in next sections of this document. Main point is that dependent modules have to be executed one after another during this what we called "preview stage". Later, with next releases there will be separate mechanism introduced to orchestrate modules dependencies and their consecutive execution.

## New scenarios

In 0.8 we offer the possibility to use AKS or EKS as Kubernetes providers. That is introduced with modules mechanism, so we launched the first four modules:

* [Azure Basic Infrastructure](https://github.com/epiphany-platform/m-azure-basic-infrastructure) (AzBI) module
* [Azure AKS](https://github.com/epiphany-platform/m-azure-kubernetes-service) (AzKS) module
* [AWS Basic Infrastructure](https://github.com/epiphany-platform/m-aws-basic-infrastructure) (AwsBI) module
* [AWS EKS](https://github.com/epiphany-platform/m-aws-kubernetes-service) (AwsKS) module

Those 4 modules together with the classic Epiphany used with `any` provider allow replacing of on-prem Kubernetes cluster with managed Kubernetes services.

As it might be already visible there are 2 paths provided:

* Azure related, using AzBI and AzKS modules,
* AWS related, using AwsBI and AwsKS modules.

Those "... Basic Infrastructure" modules are responsible to provide basic cloud resources (eg.: resource groups, virtual networks, subnets, virtual machines, network security rules, routing, ect.) which will be used by next modules. So in this case, those are "... KS modules" meant to provide managed Kubernetes services. They use resources provided by basic infrastructure modules (eg.: subnets or resource groups) and instantiate managed Kubernetes services provided by cloud providers. The last element in both those cloud provider related paths is classic Epiphany installed on top of resources provided by those modules using `any` provider.

## Hands-on

In each module, we provided a guide on how to use the module. Please refer:

* [Azure Basic Infrastructure](https://github.com/epiphany-platform/m-azure-basic-infrastructure/blob/develop/README.md) (AzBI) module
* [Azure AKS](https://github.com/epiphany-platform/m-azure-kubernetes-service/blob/develop/README.md) (AzKS) module
* [AWS Basic Infrastructure](https://github.com/epiphany-platform/m-aws-basic-infrastructure/blob/develop/README.md) (AwsBI) module
* [AWS EKS](https://github.com/epiphany-platform/m-aws-kubernetes-service/blob/develop/README.md) (AwsKS) module

After deployment of EKS or AKS, you can perform Epiphany installation on top of it.

### Install Epiphany on top of AzKS or AwsKS

NOTE - Default OS users:

```yaml
Azure:
    redhat: ec2-user
    ubuntu: operations
AWS:
    redhat: ec2-user
    ubuntu: ubuntu
```

* Create Epiphany cluster config file in `/tmp/shared/epi.yml`
  Example:

  ```yaml
  kind: epiphany-cluster
  title: Epiphany cluster Config
  name: your-cluster-name # <----- make unified with other places and build directory name
  provider: any # <----- use "any" provider
  specification:
    name: your-cluster-name # <----- make unified with other places and build directory name
    admin_user:
      name: operations # <----- make sure os-user is correct
      key_path: /tmp/shared/vms_rsa # <----- use generated key file
    cloud:
      k8s_as_cloud_service: true # <----- make sure that flag is set, as it indicates usage of a managed Kubernetes service
    components:
      repository:
        count: 1
        machines:
          - default-epiphany-modules-test-all-0 # <----- make sure that it is correct VM name
      kubernetes_master:
        count: 0
      kubernetes_node:
        count: 0
      logging:
        count: 0
      monitoring:
        count: 0
      kafka:
        count: 0
      postgresql:
        count: 1
        machines:
          - default-epiphany-modules-test-all-1 # <----- make sure that it is correct VM name
      load_balancer:
        count: 0
      rabbitmq:
        count: 0
  ---
  kind: configuration/feature-mapping
  title: Feature mapping to roles
  name: your-cluster-name # <----- make unified with other places and build directory name
  provider: any
  specification:
    roles_mapping:
      repository:
        - repository
        - image-registry
        - firewall
        - filebeat
        - node-exporter
        - applications
  ---
  kind: infrastructure/machine
  name: default-epiphany-modules-test-all-0
  provider: any
  specification:
    hostname: epiphany-modules-test-all-0
    ip: 12.34.56.78 # <----- put here public IP attached to machine
  ---
  kind: infrastructure/machine
  name: default-epiphany-modules-test-all-1
  provider: any
  specification:
    hostname: epiphany-modules-test-all-1
    ip: 12.34.56.78 # <----- put here public IP attached to machine
  ---
  kind: configuration/repository
  title: "Epiphany requirements repository"
  name: default
  specification:
    description: "Local repository of binaries required to install Epiphany"
    download_done_flag_expire_minutes: 120
    apache_epirepo_path: "/var/www/html/epirepo"
    teardown:
      disable_http_server: true
      remove:
        files: false
        helm_charts: false
        images: false
        packages: false
  provider: any
  ---
  kind: configuration/postgresql
  title: PostgreSQL
  name: default
  specification:
    config_file:
      parameter_groups:
        - name: CONNECTIONS AND AUTHENTICATION
          subgroups:
            - name: Connection Settings
              parameters:
                - name: listen_addresses
                  value: "'*'"
                  comment: listen on all addresses
            - name: Security and Authentication
              parameters:
                - name: ssl
                  value: 'off'
                  comment: to have the default value also on Ubuntu
        - name: RESOURCE USAGE (except WAL)
          subgroups:
            - name: Kernel Resource Usage
              parameters:
                - name: shared_preload_libraries
                  value: AUTOCONFIGURED
                  comment: set by automation
        - name: ERROR REPORTING AND LOGGING
          subgroups:
            - name: Where to Log
              parameters:
                - name: log_directory
                  value: "'/var/log/postgresql'"
                  comment: to have standard location for Filebeat and logrotate
                - name: log_filename
                  value: "'postgresql.log'"
                  comment: to use logrotate with common configuration
        - name: WRITE AHEAD LOG
          subgroups:
            - name: Settings
              parameters:
                - name: wal_level
                  value: replica
                  when: replication
            - name: Archiving
              parameters:
                - name: archive_mode
                  value: 'on'
                  when: replication
                - name: archive_command
                  value: "'test ! -f /dbbackup/{{ inventory_hostname }}/backup/%f &&\
                      \ gzip -c < %p > /dbbackup/{{ inventory_hostname }}/backup/%f'"
                  when: replication
        - name: REPLICATION
          subgroups:
            - name: Sending Server(s)
              parameters:
                - name: max_wal_senders
                  value: 10
                  comment: maximum number of simultaneously running WAL sender processes
                  when: replication
                - name: wal_keep_segments
                  value: 34
                  comment: number of WAL files held for standby servers
                  when: replication
    extensions:
      pgaudit:
        enabled: false
        shared_preload_libraries:
          - pgaudit
        config_file_parameters:
          log_connections: 'off'
          log_disconnections: 'off'
          log_statement: 'none'
          log_line_prefix: "'%m [%p] %q%u@%d,host=%h '"
          pgaudit.log: "'write, function, role, ddl' # 'misc_set' is not supported for\
              \ PG 10"
          pgaudit.log_catalog: 'off # to reduce overhead of logging'
          pgaudit.log_relation: 'on # separate log entry for each relation'
          pgaudit.log_statement_once: 'off'
          pgaudit.log_parameter: 'on'
      pgbouncer:
        enabled: false
      replication:
        enabled: false
        replication_user_name: epi_repmgr
        replication_user_password: PASSWORD_TO_CHANGE
        priviledged_user_name: epi_repmgr_admin
        priviledged_user_password: PASSWORD_TO_CHANGE
        use_repmgr: true
        repmgr_database: epi_repmgr
        shared_preload_libraries:
          - repmgr
    logrotate:
      config: |-
        /var/log/postgresql/postgresql*.log {
            maxsize 10M
            daily
            rotate 6
            copytruncate
        # delaycompress is for Filebeat
            delaycompress
            compress
            notifempty
            missingok
            su root root
            nomail
        # to have multiple unique filenames per day when dateext option is set
            dateformat -%Y%m%dH%H
        }
  provider: any
  ---
  kind: configuration/applications
  title: "Kubernetes Applications Config"
  name: default
  specification:
    applications:
      - name: ignite-stateless
        enabled: false
        image_path: "apacheignite/ignite:2.5.0"
        use_local_image_registry: false
        namespace: ignite
        service:
          rest_nodeport: 32300
          sql_nodeport: 32301
          thinclients_nodeport: 32302
        replicas: 1
        enabled_plugins:
          - ignite-kubernetes
          - ignite-rest-http
      - name: rabbitmq
        enabled: false
        image_path: rabbitmq:3.8.3
        use_local_image_registry: false
        service:
          name: rabbitmq-cluster
          port: 30672
          management_port: 31672
          replicas: 2
          namespace: queue
        rabbitmq:
          plugins:
            - rabbitmq_management
            - rabbitmq_management_agent
          policies:
            - name: ha-policy2
              pattern: ".*"
              definitions:
                ha-mode: all
          custom_configurations:
            - name: vm_memory_high_watermark.relative
              value: 0.5
          cluster:
      - name: auth-service
        enabled: false
        image_path: jboss/keycloak:9.0.0
        use_local_image_registry: false
        service:
          name: as-testauthdb
          port: 30104
          replicas: 2
          namespace: namespace-for-auth
          admin_user: auth-service-username
          admin_password: PASSWORD_TO_CHANGE
        database:
          name: auth-database-name
          user: auth-db-user
          password: PASSWORD_TO_CHANGE
      - name: pgpool
        enabled: true
        image:
          path: bitnami/pgpool:4.1.1-debian-10-r29
          debug: false
        use_local_image_registry: false
        namespace: postgres-pool
        service:
          name: pgpool
          port: 5432
        replicas: 3
        pod_spec:
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
                - weight: 100
                  podAffinityTerm:
                    labelSelector:
                      matchExpressions:
                        - key: app
                          operator: In
                          values:
                            - pgpool
                    topologyKey: kubernetes.io/hostname
          nodeSelector: {}
          tolerations: {}
        resources:
          limits:
            memory: 176Mi
          requests:
            cpu: 250m
            memory: 176Mi
        pgpool:
          env:
            PGPOOL_BACKEND_NODES: autoconfigured
            PGPOOL_POSTGRES_USERNAME: epi_pgpool_postgres_admin
            PGPOOL_SR_CHECK_USER: epi_pgpool_sr_check
            PGPOOL_ADMIN_USERNAME: epi_pgpool_admin
            PGPOOL_ENABLE_LOAD_BALANCING: true
            PGPOOL_MAX_POOL: 4
            PGPOOL_POSTGRES_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_postgres_password
            PGPOOL_SR_CHECK_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_sr_check_password
            PGPOOL_ADMIN_PASSWORD_FILE: /opt/bitnami/pgpool/secrets/pgpool_admin_password
          secrets:
            pgpool_postgres_password: PASSWORD_TO_CHANGE
            pgpool_sr_check_password: PASSWORD_TO_CHANGE
            pgpool_admin_password: PASSWORD_TO_CHANGE
          pgpool_conf_content_to_append: |
            #------------------------------------------------------------------------------
            # CUSTOM SETTINGS (appended by Epiphany to override defaults)
            #------------------------------------------------------------------------------
            # num_init_children = 32
            connection_life_time = 900
            reserved_connections = 1
          pool_hba_conf: autoconfigured
      - name: pgbouncer
        enabled: true
        image_path: brainsam/pgbouncer:1.12
        init_image_path: bitnami/pgpool:4.1.1-debian-10-r29
        use_local_image_registry: false
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
            LISTEN_ADDR: "*"
            LISTEN_PORT: 5432
            AUTH_FILE: "/etc/pgbouncer/auth/users.txt"
            AUTH_TYPE: md5
            MAX_CLIENT_CONN: 150
            DEFAULT_POOL_SIZE: 25
            RESERVE_POOL_SIZE: 25
            POOL_MODE: transaction
  provider: any
  ```

* Run `epicli` tool to install Epiphany:

  ```shell
  epicli --auto-approve apply --file='/tmp/shared/epi.yml' --vault-password='secret'
  ```

  This will install PostgreSQL on one of the machines and configure PgBouncer, Pgpool and additional services to manage database connections.

  Please make sure you disable applications that you don't need. Also, you can enable standard Epiphany services like Kafka or RabbitMQ, by increasing the number of virtual machines in the basic infrastructure config and assigning them to Epiphany components you want to use.

  If you would like to deploy custom resources into managed Kubernetes, then the standard kubeconfig yaml document can be found inside the shared state file (you should be able to use vendor tools as well to get it).

  We highly recommend using the `Ingress` resource in Kubernetes to allow access to web applications inside the cluster. Since it's managed Kubernetes and fully supported by the cloud platform, the classic HAProxy load-balancer solution seems to be deprecated here.
