# Changelog 0.2

## [0.2.2] 2019-05-20

### Fixed

- Fixed vulnerability in Docker development image
- Upgraded Keycloak Python examples to python 3.7.2

## [0.2.1] 2019-03-07

### Fixed

- ZooKeeper distribution URL #147

## [0.2.0] 2019-02-19

### Changed

- Kubernetes v1.13.0 installation
- Filebeat 6.5.4 installation
- RabbitMQ installation inside Kubernetes (clustered RabbitMQ) #17
- RabbitMQ installation outside of Kubernetes (VM) #17
- PostgreSQL installation with replication #16
- Authentication service installation (Keycloak) inside Kubernetes
- Automatic untainting Kubernetes Master when single Master deployed without Nodes #22
- Example applications added to /examples
  - Keycloak authentication (dotnet, java, python, javascript) #19
  - RabbitMQ/Kafka (dotnet) #50, #39
- Documentation updates

### Fixed

- Filebeat memory consumption when Elasticsearch does not accept data #61
