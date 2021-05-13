# Epiphany Platform ARM design document

Affected version: 1.1.x

## Goals

This document outlines an aproach to add (partial) ARM support to Epicli. The requirements:

- ARMv8/ARM64 architecture
- Centos 7
- "any" provider as we do not want to provide ARM infrastructure on any cloud providers yet through Terraform
- Epiphany components needed ordered by priority:
    1. Kubernetes
    2. Kafka
    3. HAProxy
    5. Keycloak (This is the only deployment we need to support from the ```applications``` role)
    6. PostgreSQL (Would only be used by keycloak and does not needs to support a single deployment)
    7. RabbitMQ
    8. Logging (ELK + filebeat)
    9. Monitoring (Prometheus + Grafana + Exporters)
  Initial research [here](./centos-arm-analysis.md) shows additional information about available packages and effected roles for each component.

## Approach

The 2 high level approaches that have been opted so far:

1. Add “architecture” flag when using Epicli
2. Add new OS (CentosARM64 fe.)

Have 2 big disadvanges from the start:

1. Will require an additional input which makes things more confusing as they will need supply not only the OS but also Architecture for (offline) install. This should not be needed as we can detect the architecture we are working on, on all required levels.
2. Does not require additional input but this will lead to code duplication in the ```repository``` role as we need to maintain ```download-requirements.sh``` for each OS and architecture then.

That is why I opt for an approach where we don't add any architecture flag or new additional OS. The architecture we can handle on the code level and on the OS level only the ```requirements.txt``` might be different for each as indicated by initial research [here](./centos-arm-analysis.md).


## Changes required

### Repostitory role

In the repository role we need to change the download of the requirements to support additional architectures as download requirements might be different as:

- Some components/roles might not have packages/binaries/containers that support ARM
- Some filenames for binaries will be different per architecture
- Some package repositories will have different URLs per architecture

Hence we should make a requirements.txt for each architecture we want to support, for example:

- requirements_x86_64.txt (Should be the default and present)
- requirements_arm64.txt

The ```download-requirements.sh``` script should be able to figure out which one to select based on the output of:

```shell
uname -i

```

### Download role

In the download role, which is used to download plain files from the repository, we should add support for filename patterns and automatically look for current architecture (optionally with regex based suffix like `linux[_-]amd64\.(tar\.gz|tar|zip)`):

For example select between:

- haproxy_exporter-0.12.0.linux-```x86_64```.tar.gz
- haproxy_exporter-0.12.0.linux-```arm64```.tar.gz

based on ```ansible_architecture``` fact.

**Note that this should be optional as some filenames do not contain architecture like Java based packages for example.**

### Artitecture support for each component/role

As per current requirements not every Epiphany component is required to support ARM and there might be cases that a component/role can't support ARM as indicated by initial research [here](./centos-arm-analysis.md).

Thats why every component/role should be marked which architecture it supports. Maybe something in ```<rolename>/defaults/main.yml``` like:

```yml
supported_architectures:
  - all ?
  - x86_64
  - arm64
```

We can assume the role/component will support everything if ```all``` is defined or if ```supported_architectures``` is not present.

### Pre-flight check

The ```preflight``` should be expanded to check if all the components/roles we want to install from the inventory actually support the architecture we want to use. We should be able to do this with the definition from the above point. This way we will make sure people can only install components on ARM which we actually support.

### Replace Skopeo with Crane

Currently we use [Skopeo](https://github.com/containers/skopeo) to download the image requirements. Skopeo however has the following issues with newer versions:

- No support anymore for universal Go binaries. Each OS would need to have each own build version
- Sketchy support for ARM64

That is why we should replace it with [Crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/README.md).

1. This tool can do the same as Skopeo:

```bash
./skopeo --insecure-policy copy docker://kubernetesui/dashboard:v2.0.3 docker-archive:skopeodashboard:v2.0.3
./crane pull --insecure kubernetesui/dashboard:v2.0.3 dashboard.tar
```

The above will produce the same Docker image package.

2. Supports the universal cross distro binary.
3. Has support for both ARM64 and x86_64.
4. Has official [pre-build binaries](https://github.com/google/go-containerregistry/releases/tag/v0.4.0), unlike Skopeo.
