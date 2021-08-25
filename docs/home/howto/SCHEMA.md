## Schema

### Named lists

Epiphany uses a concept called **named lists** in the configuration YAML. Every entry in a **named lists**  list will have a ```name``` field to identify it and make it unique:

```yaml
...
  list:
  - name: entry1
    property1: property1
    property2: property2
  - name: entry2
    property1: property1
    property2: property2
  - name: entry3
    property1: property1
    property2: property2
...
```

By default, when you define a **named list** inside your configuration it will completely overwrite the defaults that Epiphany provides. This behaviour is on purpose so when you, for example, define a list of users for Kafka inside your configuration it completely overwrite the users defined in the [Kafka defaults.](https://github.com/epiphany-platform/epiphany/blob/9ff9bb266cd6addf309059a8a5e7a48835daafc3/core/src/epicli/data/common/defaults/configuration/kafka.yml#L34).

In some cases however you don`t want to overwrite a **named list**. A good example would be the [application configurations.](https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/common/defaults/configuration/applications.yml)

You don`t want to re-define every entry just to make sure Epiphany uses all defaults. That is where the ```_merge_mode``` metadata tag comes in. It will let you define if you want to ```overwrite``` or ```merge``` named list.

For example you want to enable ```auth-service``` application. Instead of defining the whole ```configuration/applications``` configuration you can do the following:

```yaml
kind: configuration/applications
title: "Kubernetes Applications Config"
name: default
provider: azure
specification:
  applications:
  - _merge_mode: 'merge'
  - name: auth-service
    enabled: true
```

The ```_merge_mode``` entry with ```merge``` will tell Epicli to merge the list and only change the ```enabled: true``` entry inside the ```auth-service``` and take the rests of the [configuration/applications]((https://github.com/epiphany-platform/epiphany/blob/develop/core/src/epicli/data/common/defaults/configuration/applications.yml)) defaults.
