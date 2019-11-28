# Epiphany Platform backup design document

Affected version: 0.5.x

## Goals

Provide backup functionality for Epiphany Platform - cluster created using epicli tool.

## Use cases

Creating snapshots of disks for all elements in environment created on cloud.

## Example use

```bash
epibackup --disks-snapshot -f path_to_data_yaml
```

Where `-f` is path to data yaml file with configuration of environment. `--disks-snapshot` informs about option that will create whole disks snapshot.

## Backup Component View

![Epiphany backup component](backup_component.png)

User/background service/job executes `epibackup` (code name) application. Application takes parameters:
- `-f`: path to data yaml file with configuration of environment.
- `--disks-snapshot`: option to create whole disk snapshot

Tool when executed takes resource group from file provided with `-f` flag and create snapshots of all elements in resource group.

Tool also produces metadata file that describes backup with time and the name of disks for which snapshot has been created.
