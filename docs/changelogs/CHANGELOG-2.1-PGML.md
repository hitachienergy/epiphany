<!-- markdownlint-disable-file no-duplicate-header -->
# Changelog 2.1-PGML

## [2.1.0-dev+PGML]

### Added

- Allow to define service endpoints for subnets
- curator-opensearch 0.0.9
- Proxy's root CA certificate in dev container's Dockerfile
- `use_device_code` option for `az login`
- Scrape Alertmanager's metrics
- Blackbox exporter
- Grafana Dashboard: Certificates Expiration (X509 Certificate Exporter)

### Updated

- Terraform Azure Provider 2.91.0 to 3.74.0
- Keycloak to 20.0.5-0
- Make YAML format of default configuration compatible with sops (it converts YAML block scalars to flow scalars)
- Change default proxy mode for Keycloak from `reencrypt` to `edge` (HTTP is enabled)
- Switch from `k8s.gcr.io` to `registry.k8s.io`
- epicli base image `python:3.10.6-slim` to `python:3.10.11-slim`
- Prometheus: Avoid false positives from brief spikes for alert "Disk will run out of space"
- OpenSearch to 2.8.0
- node_exporter to 1.6.1
- Grafana to 10.0.3
- Grafana dashboards
- Use availability set for `kafka` and `logging` components in the default configuration
- Change naming convention - VMs are numbered starting from 1 with a leading 0 (01, 02, ...)
- Apply alerts provided by InfraOps

### Removed

- Elasticsearch Curator
- RabbitMQ
- Rook
- `logging` role (merged with `opensearch`)
- `openjdk-11-jdk-headless` from epicli Docker image
- Kubernetes
- PostgreSQL
- Image registry
- Helm chart repository
- HAProxy
- Support for RHEL and ARM
- Keycloak
- sshtunnel role
- `prefix` setting from `epiphany-cluster` input manifest for Azure provider
- Cloud storage for K8s
