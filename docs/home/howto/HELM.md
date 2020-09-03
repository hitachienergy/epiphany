## Helm charts in repository


System Helm charts are stored in the following location:

`roles/helm_charts/files/system`

There is also dedicated Helm charts location for users

`roles/helm_charts/files/user`

- Currently user part has no automation implemented. It will need some additional "options" via epi client but it needs discussion with wider audience about the needs.

Implementator/developer maintain system path content.
All chart should be added in directories (not archived)

Repository role is responsible for retrieving mentioned Helm charts. It copies all the directories, archive them (`.tgz`), generates helm index file and serve in apache server.



## Installing Helm charts from repository

Installation of particular Helm charts is performed in separate role. Each other particular role that needs to install Helm chart has to trigger separate single helm chart installation task:
`roles/helm/tasks/install-chart.yml`



Single Helm installation task is responsible for installing already existing charts from repository.

It is possible to overwrite chart values within the specification config.
Single helm chart task expects 3 parameters to be passed:

```yaml
    disable_helm_chart:
    helm_chart_name: 
    helm_chart_values:
```

Example usage:

```yaml
---
- name: Set Helm chart values from custom configuration
  set_fact:
    _helm_chart_values: "{{ specification.helm_chart_values }}"
  when: specification.helm_chart_values is defined
- name: Set Helm chart name from custom configuration
  set_fact:
    _helm_chart_name: "{{ specification.helm_chart_name }}"
  when: specification.helm_chart_name is defined
- name: Set Helm chart disable flag from custom configuration
  set_fact:
    _disable_helm_chart: "{{ specification.disable_helm_chart }}"
  when: specification.disable_helm_chart is defined
- name: Mychart
  include_role:
    name: helm
    tasks_from: install-chart
  vars:
    disable_helm_chart: "{{ _disable_helm_chart }}"
    helm_chart_name: "{{ _helm_chart_name }}"
    helm_chart_values:  "{{ _helm_chart_values }}"
```

Example config:

```yaml
kind: configuration/helm-mychart
title: "Helm mychart"
name: default
specification:
  helm_chart_name: mychart
  disable_helm_chart: false
  helm_chart_values:
    service:
      port: 8080
    nameOverride: mychart_custom_name
```