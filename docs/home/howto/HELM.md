## Helm "system" chart repository

Epiphany provides Helm repository for internal usage inside our Ansible codebase. Currently only the "system" repository is available, but it's not designed to be used by regular users. __In fact, regular users must not reuse it for any purpose.__

Epiphany developers can find it inside this location `roles/helm_charts/files/system`. To add a chart to the repository it's enough just to put unarchived chart directory tree inside the location (in a separate directory) and re-run `epcli apply`.

When the `repository` Ansible role is run it copies all unarchived charts to the repository host, creates Helm repository (`index.yaml`) and serves all these files from Apache HTTP server.

## Installing Helm charts from the "system" repository

Epiphany developers can reuse the "system" repository from any place inside the Ansible codebase. Moreover, it's a responsibility of a particular role to call the `helm upgrade --install` command.

There is a helpler task file that can be reused for that purpose `roles/helm/tasks/install-system-release.yml`. __It's only responsible for installing already existing "system" Helm charts from the "system" repository.__

This helper task expects such parameters/facts:

```yaml
- set_fact:
    helm_chart_name: <string>
    helm_chart_values: <map>
    helm_release_name: <string>
```

- `helm_chart_values` is a standard yaml map, values defined there replace default config of the chart (`values.yaml`).

Our standard practice is to place those values inside the `specification` document of the role that deploys the Helm release in Kubernetes.

Example config:

```yaml
kind: configuration/<mykind-used-by-myrole>
name: default
specification:
  helm_chart_name: mychart
  helm_release_name: myrelease
  helm_chart_values:
    service:
      port: 8080
    nameOverride: mychart_custom_name
```

Example usage:

```yaml
- name: Mychart
  include_role:
    name: helm
    tasks_from: install-system-release.yml
  vars:
    helm_chart_name: "{{ specification.helm_chart_name }}"
    helm_release_name: "{{ specification.helm_release_name }}"
    helm_chart_values: "{{ specification.helm_chart_values }}"
```

__By default all installed "system" Helm releases are deployed inside the `epi-charts` namespace in Kubernetes.__

## Uninstalling "system" Helm releases

To uninstall Helm release `roles/helm/tasks/delete-system-release.yml` can be used. For example:

```yaml
- include_role:
    name: helm
    tasks_from: delete-system-release.yml
  vars:
    helm_release_name: myrelease
```
