# Epiphany PostgreSQL auditing design document

Affected version: 0.5.x

## Goals

Provide functionality to perform auditing of operations performed on PostgreSQL.

## Use cases

For SOX and other regulations compliance platform should provide auditing function for PostgreSQL database.
This should be set via Epiphany automation in Epiphany configuration yaml.

## Example use

In configuration for PostgreSQL we can add additional parameters, that could configure additional properties of PostgreSQL.
Config similar to proposed below can be used to configure auditing with using pgaudit.

```yaml
kind: configuration/postgresql
title: "Postgresql"
name: default
specification:
  ...
  additional_config:
    shared_preload_libraries: 'pgaudit'
    pgaudit.log: 'all, -misc'
    log_connections: on
    log_disconnections: on
    log_line_prefix: '<%m:%r:%u@%d:[%p]:> '
    log_statement: 'none'
  ...
```


## Design proposal 

Add to configuration for PostgreSQL additional parameters, that would enable auditing and install additional modules to enhance PostgreSQL
configuration. In case of auditing this would install pgaudit, which can be configured from Epiphany configuration yaml level. For Red Hat 
this would require to replace PostgreSQL from Software Collections with version from PostgreSQL repository.
