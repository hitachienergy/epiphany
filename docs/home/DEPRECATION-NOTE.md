# Deprecation Note

This page is related to our components deprecation plan. Components listed below are marked as deprecated with plan of
removal in Epiphany version 2.0.

The list of components removed:

- Hashicorp Vault

The role related to Hashicorp Vault has never been developed beyond MVP/PoC stage and cannot be used for production
usage. It also causes troubles with upgrade to new Kubernetes versions.

Removed: Epiphany 2.0 Issue: [2834](https://github.com/epiphany-platform/epiphany/issues/2834)

- Istio

We are considering replacement of Istio component with different solution. Additionally, Istio causes problems during
upgrade of Kubernetes.

Removed: Epiphany 2.0 Issue: [2836](https://github.com/epiphany-platform/epiphany/issues/2836)

- Apache Ignite

Apache Ignite is prone to 1.x log4j issue.

Removed: Epiphany 2.0 Issue: [2837](https://github.com/epiphany-platform/epiphany/issues/2837)

- Logstash

The functionality that the Logstash is serving in Epiphany - exporting csv can right now be achieved using the Open
Distro for Elasticsearch plugin. The Logstash in this version is prone to log4j issue and this is also the reason it
should be removed.

Removed: Epiphany 2.0 Issue: [2833](https://github.com/epiphany-platform/epiphany/issues/2833)

## Next steps

### Logstash

If you plan Epiphany upgrade from v1.x to v2.x and Logstash is installed in your cluster, but you don't use it, it is
recommended to:

- remove `logstash` group, if present, from `inventory` file
- remove Logstash from machines (recommended way is to use `apt`/`yum` according to your OS)
