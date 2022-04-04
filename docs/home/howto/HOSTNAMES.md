# Hostnames

Epiphany manages hostnames only for Azure as this is
[required](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_machine#computer_name) by Terraform.

## Limitations

Linux host name cannot exceed 64 characters in length.

## Generation rule

By default, it generates automatically using following rules:

1. If `hostname_domain_extension` is set in `epiphany-cluster` configuration:
`<cluster_prefix>-<cluster_name>-<component_name>-vm-<index>.<hostname_domain_extension>`

2. If `hostname_domain_extension` is no set in `epiphany-cluster` configuration:
`<cluster_prefix>-<cluster_name>-<component_name>-vm-<index>`.

## Changing component name

---
**NOTE**

Changing this configuration leads to replacement of component's virtual machines during re-apply.

---

Usually component names are predefined, but there is an ability to change that.
There might be such need when `hostname_domain_extension` is set and it results to exceeding the length limit.
For example, to change `kubernetes-master` to `k8s-master` following config:

```yaml
---
kind: infrastructure/virtual-machine
provider: azure
specification:
  alt_component_name: k8s-master
```
