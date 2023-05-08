<!-- markdownlint-disable-file no-duplicate-header -->
# Changelog 2.1-PGML

## [2.1.0-dev+PGML]

### Added

- Allow to define service endpoints for subnets
- curator-opensearch 0.0.9

### Updated

- Terraform Azure Provider 2.91.0 to 3.45.0
- Upgrade Keycloak to 20.0.5-0
- Make YAML format of default configuration compatible with sops (it converts YAML block scalars to flow scalars)
- Change default proxy mode for Keycloak from `reencrypt` to `edge` (HTTP is enabled)
- Switch from `k8s.gcr.io` to `registry.k8s.io`

### Removed

- Elasticsearch Curator
- RabbitMQ
- Rook
- `logging` role (merged with `opensearch`)
