# Hostnames

There is an ability to modify host names with Epiphany only in Azure.

## Limitations

- Linux host name cannot exceed 64 characters in length.
- Kubernetes names must be no more than 63 characters.

Due to the statements above, `azure` provider verifies whether host names exceed limitation of 63 characters.

## Generation rule

By default, host name is generated automatically using the following rules:

1. If `hostname_domain_extension` is set in `epiphany-cluster` configuration:
`<cluster_prefix>-<cluster_name>-<component_name>-vm-<index>.<hostname_domain_extension>`

2. If `hostname_domain_extension` is not set in `epiphany-cluster` configuration:
`<cluster_prefix>-<cluster_name>-<component_name>-vm-<index>`.

## Changing component name

---
**NOTE**

Changing this configuration leads to replacement of component's virtual machines during re-apply.

---

Usually component names are predefined, but there is an ability to change them in host names.
There might be such a need when `hostname_domain_extension` is set, and it results in exceeding the length limit.
For example, to change `kubernetes-master` to `k8s-cp`, use following config:

```yaml
---
kind: epiphany-cluster
title: Epiphany cluster Config
provider: azure
name: default
specification:
  ...
  components:
    kubernetes_master:
      count: 1
      alt_component_name: k8s-cp
```
