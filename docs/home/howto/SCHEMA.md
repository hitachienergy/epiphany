## Inheritance

### Named lists

Epiphany uses a concept called **named lists** in the configuration YAML. Every entry in a **named lists**  list will have a ```name``` field to identify it and make it unique for merge operations:

```yaml
...
  list:
  - name: item1
    property1: value1
    property2: value2
  - name: item2
    property1: value3
    property2: value4
...
```

By default, a **named list** in your configuration file will completely overwrite the defaults that Epiphany provides. This behaviour is on purpose so when you, for example, define a list of users for Kafka inside your configuration it completely overwrites the users defined in the [Kafka defaults](https://github.com/epiphany-platform/epiphany/blob/9ff9bb266cd6addf309059a8a5e7a48835daafc3/core/src/epicli/data/common/defaults/configuration/kafka.yml#L34).

In some cases, however, you don't want to overwrite a **named list**. A good example would be the [application configurations](https://github.com/epiphany-platform/epiphany/blob/v1.0.1/core/src/epicli/data/common/defaults/configuration/applications.yml).

You don't want to re-define every entry just to make sure Epiphany has all default entries needed by the Ansible automation. That is where the ```_merge``` metadata tag comes in. It will let you define if you want to ```overwrite``` or ```merge``` sa **named list** by setting it to ```true``` or ```false```.

For example you want to enable the ```auth-service``` application. Instead of defining the whole ```configuration/applications``` configuration you can do the following:

```yaml
kind: configuration/applications
title: "Kubernetes Applications Config"
name: default
provider: azure
specification:
  applications:
  - _merge: true
  - name: auth-service
    enabled: true
```

The ```_merge``` entry with ```true``` will tell Epicli to merge the application list and only change the ```enabled: true``` entry inside the ```auth-service``` and take the rests of the [configuration/applications]((https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/common/defaults/configuration/applications.yml)) configuration from the defaults.
