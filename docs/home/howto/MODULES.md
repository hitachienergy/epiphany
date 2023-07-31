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

* Azure Basic Infrastructure (AzBI) module
* Azure AKS (AzKS) module
* AWS Basic Infrastructure (AwsBI) module
* AWS EKS (AwsKS) module

Those 4 modules together with the classic Epiphany used with `any` provider allow replacing of on-prem Kubernetes cluster with managed Kubernetes services.

As it might be already visible there are 2 paths provided:

* Azure related, using AzBI and AzKS modules,
* AWS related, using AwsBI and AwsKS modules.

Those "... Basic Infrastructure" modules are responsible to provide basic cloud resources (eg.: resource groups, virtual networks, subnets, virtual machines, network security rules, routing, ect.) which will be used by next modules. So in this case, those are "... KS modules" meant to provide managed Kubernetes services. They use resources provided by basic infrastructure modules (eg.: subnets or resource groups) and instantiate managed Kubernetes services provided by cloud providers. The last element in both those cloud provider related paths is classic Epiphany installed on top of resources provided by those modules using `any` provider.

## Hands-on

In each module, we provided a guide on how to use the module. Please refer:

* Azure Basic Infrastructure (AzBI) module
* Azure AKS (AzKS) module
* AWS Basic Infrastructure (AwsBI) module
* AWS EKS (AwsKS) module

After deployment of EKS or AKS, you can perform Epiphany installation on top of it.

### Install Epiphany on top of AzKS or AwsKS

NOTE - Default OS users:

```yaml
Azure:
    ubuntu: operations
AWS:
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
      logging:
        count: 0
      monitoring:
        count: 0
      kafka:
        count: 0
  ---
  kind: configuration/feature-mappings
  title: "Feature mapping to components"
  name: your-cluster-name # <----- make unified with other places and build directory name
  provider: any
  specification:
    mappings:
      repository:
        - repository
        - firewall
        - filebeat
        - node-exporter
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
  ```

* Run `epicli` tool to install Epiphany:

  ```shell
  epicli --auto-approve apply --file='/tmp/shared/epi.yml' --vault-password='secret'
  ```

  You can enable standard Epiphany services like Kafka, by increasing the number of virtual machines in the basic infrastructure config and assigning them to Epiphany components you want to use.

  If you would like to deploy custom resources into managed Kubernetes, then the standard kubeconfig yaml document can be found inside the shared state file (you should be able to use vendor tools as well to get it).

  We highly recommend using the `Ingress` resource in Kubernetes to allow access to web applications inside the cluster. Since it's managed Kubernetes and fully supported by the cloud platform.
