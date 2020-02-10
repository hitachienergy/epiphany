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
title: PostgreSQL
name: default
specification:
  ...
  extensions:
    pgaudit:
      enabled: false
      shared_preload_libraries:
        - pgaudit
      config_file_parameters:
        pgaudit.log: 'all, -misc'
        log_connections: 'on'
        log_disconnections: 'on'
        log_line_prefix: "'%m [%p] %q%u@%d,host=%h '"
        log_statement: 'none'
  ...
```

## Design proposal

Add to PostgreSQL configuration additional settings, that would install and configure pgaudit extension.
For RHEL we use PostgreSQL installed from Software Collections repository, which doesn't provide pgaudit package for PostgreSQL
versions older than 12. For this reason, on RHEL pgaudit will be installed from PostgreSQL repository.
