# Epiphany Platform backup design document

Affected version: 0.10.x/0.11.x

## Goals

This document outlines an aproach to add (partial) ARM support to Epicli. Not finalized requirements so far:

- ARMv8/ARM64 architecture
- Centos 7 as operating system
- "any" provider as we do not want to provide ARM infrastructure on any cloud providers jet through Terraform
- Epiphany components: K8s, Kafka, ELK, Grafana, Prometheus, Kibana, HAProxy, Keycloak, PostgreSQL

## Approach

The 2 high level approaches that have been opted so far:

1. Add “architecture” flag when using Epicli
2. Add new OS (CentosARM64 fe.)

Have 2 big disadvanges from the start:

1. Will require an additional input which makes things more confusing as they will need supply not only the OS but also Architecture for (offline) install. This should not be needed as we can detect the architecture we are working on, on all required levels.
2. Does not require additional input but this will lead to code duplication in the ```requirements``` role as we need to maintain ```download-requirements.sh``` for each OS and architecture then.

That is why I opt for an approach where we don't add any architecture flag or new additional OS. The architecture we can handle on the code level and on the OS level only the ```requirements.txt``` might be different for each as indicated by initial research [here.](./centos-arm-analysis.md).


## Changes required

### Repostitory role

In the repository role we need to change the download of the requirements to support additional architectures as download requirements might be different as:

- Some components/roles might not have packages/binaries/containers that support ARM
- Some filenames for binaries will be different per architecture

Hence we should make a requirements.txt for each architecture we want to support, for example:


- requirements_x86_64.txt (Should be the default and present)
- requirements_aarch64.txt

The ```download-requirements.sh``` script should be able to figure out which one to select based on the output of:

```shell
uname -a
```

or

```shell
arch
```

As fallback we could just use ```requirements.txt``` and asume its ```x86_64```.

### Download role

In the download role, which is used to download plain files from the repository, we should add support for filenames with aliases for different architectures:

For example select between:

- haproxy_exporter-0.12.0.linux-```amd64```.tar.gz
- haproxy_exporter-0.12.0.linux-```arm64```.tar.gz

Based on ```ansible_architecture```.

**Note that this should be optional as some packages dont require the use of an alias like Java bases ones for example.**

### Artitecture support for each component/role

As per current requirements not every Epiphany component is required to support ARM and there might be cases that a component/role can`t support ARM as indicated by initial research [here.](./centos-arm-analysis.md).

Thats why every component/role should be marked which architecture it supports. Maybe something in ```<rolename>/defaults/main.yml``` like:

```yml
supported_architectures:
  - all ?
  - x86_64
  - aarch64
```

We can assume the role/component will support everyting if ```all``` is defined or if ```supported_architectures``` is not present.

### Pre-flight check

The ```preflight``` should be expended to check if all the components/roles we want to install from the inventory actually support the architecture we want to use. We should be able todo this with the definition from the above point. This way we will make sure people can only install components on ARM which we actually support.
