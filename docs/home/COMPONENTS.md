# Component and dependency versions and licenses

## Epiphany cluster components

Note that versions are default versions and can be changed in certain cases through configuration. Versions that are marked with '-' are dependent on the OS distribution version and packagemanager.

| Component                  | Version  | Repo/Website                                          | License                                                           |
| -------------------------- | -------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Kubernetes                 | 1.18.6   | https://github.com/kubernetes/kubernetes              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kubernetes Dashboard       | 2.0.3    | https://github.com/kubernetes/dashboard               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Calico                     | 3.15.0   | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Flannel                    | 0.12.0   | https://github.com/coreos/flannel/                    | [Apache License](https://www.apache.org/licenses/LICENSE-1.0)     |
| Canal                      | 3.15.0   | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka                      | 2.6.0    | https://github.com/apache/kafka                       | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Zookeeper                  | 3.5.8    | https://github.com/apache/zookeeper                   | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| RabbitMQ                   | 3.8.9    | https://github.com/rabbitmq/rabbitmq-server           | [Mozilla Public License](https://www.mozilla.org/en-US/MPL/)      |
| Docker CE                  | 19.03.14 | https://github.com/docker/docker-ce/                  | [Apache License](https://www.apache.org/licenses/LICENSE-1.0)     |
| KeyCloak                   | 9.0.0    | https://github.com/keycloak/keycloak                  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Elasticsearch OSS          | 7.10.2   | https://github.com/elastic/elasticsearch              | https://github.com/elastic/elasticsearch/blob/master/LICENSE.txt  |
| Elasticsearch Curator OSS  | 5.8.3    | https://github.com/elastic/curator                    | https://github.com/elastic/curator/blob/master/LICENSE.txt        |
| Opendistro for Elasticsearch          | 1.13.x   | https://opendistro.github.io/for-elasticsearch/                  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Opendistro for Elasticsearch Kibana   | 1.13.1   | https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/ | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat                   | 7.9.2    | https://github.com/elastic/beats                      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat Helm Chart        | 7.9.2    | https://github.com/elastic/helm-charts                | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Logstash OSS               | 7.12.0   | https://github.com/elastic/logstash                   | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Prometheus                 | 2.10.0   | https://github.com/prometheus/prometheus              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Grafana                    | 7.3.5    | https://github.com/grafana/grafana                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Node Exporter              | 1.0.1    | https://github.com/prometheus/node_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Bitnami Node Exporter Helm Chart      | 1.1.2    | https://github.com/bitnami/charts          | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka Exporter             | 1.2.0    | https://github.com/danielqsj/kafka_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| HAProxy Exporter           | 0.10.0   | https://github.com/prometheus/haproxy_exporter        | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| JMX Exporter               | 0.12.0   | https://github.com/prometheus/jmx_exporter            | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Postgres Exporter          | 0.9.0    | https://github.com/prometheus-community/postgres_exporter | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| PostgreSQL                 | 10       | https://www.postgresql.org/                           | https://opensource.org/licenses/postgresql                        |
| HAProxy                    | 2.2.2    | https://www.haproxy.org/                              | [GNU General Public License 2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| PGAudit                    | 1.2.2    | https://github.com/pgaudit/pgaudit                    | [PostgreSQL license](http://www.postgresql.org/about/licence/)    |
| PgBouncer                  | 1.10.0   | https://github.com/pgbouncer/pgbouncer                | [ISC License](https://opensource.org/licenses/isc)                |
| repmgr                     | 4.0.6    | https://github.com/2ndQuadrant/repmgr                 | [Apache License 2.0](https://github.com/2ndQuadrant/repmgr/blob/master/LICENSE) |
| PGPool                     | 4.1.1    | https://www.pgpool.net/                               | [License](https://www.pgpool.net/mediawiki/index.php/pgpool-II_License) |
| Alertmanager               | 0.17.0   | https://github.com/prometheus/alertmanager            | [Apache License 2.0](https://github.com/prometheus/alertmanager/blob/master/LICENSE) |
| Apache Ignite              | 2.9.1    | https://github.com/apache/ignite                      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Apache2                    | 2.4.29   | https://httpd.apache.org/                             | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Hashicorp Vault            | 1.7.0    | https://github.com/hashicorp/vault                    | [Mozilla Public License 2.0](https://github.com/hashicorp/vault/blob/master/LICENSE) |
| Hashicorp Vault Helm Chart | 0.11.0   | https://github.com/hashicorp/vault-helm               | [Mozilla Public License 2.0](https://github.com/hashicorp/vault-helm/blob/master/LICENSE.md) |
| Istio                      | 1.8.1    | https://github.com/istio/istio                        | [Apache License 2.0](https://github.com/istio/istio/blob/master/LICENSE) |

## Epicli binary dependencies

| Component                 | Version | Repo/Website                                          | License                                                           |
| ------------------------- | ------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Terraform                 | 0.12.6  | https://www.terraform.io/                             | [Mozilla Public License 2.0](https://github.com/hashicorp/terraform/blob/master/LICENSE) |
| Terraform AzureRM provider | 1.38.0  | https://github.com/terraform-providers/terraform-provider-azurerm | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/LICENSE) |
| Terraform AWS provider    | 2.26    | https://github.com/terraform-providers/terraform-provider-aws | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-aws/blob/master/LICENSE) |
| Crane                     | 0.4.1  | https://github.com/google/go-containerregistry/tree/main/cmd/crane     | [Apache License 2.0](https://github.com/google/go-containerregistry/blob/main/LICENSE) |

## Epicli Python dependencies

| Component | Version | Repo/Website | License |
| --------- | ------- | ------------ | ------- |
| adal | 1.2.7 | https://github.com/AzureAD/azure-activedirectory-library-for-python | [Other](https://api.github.com/repos/azuread/azure-activedirectory-library-for-python/license) |
| ansible-base | 2.10.9 | https://ansible.com/ | GPLv3+ |
| ansible | 2.10.5 | https://ansible.com/ | GPLv3+ |
| antlr4-python3-runtime | 4.7.2 | http://www.antlr.org | BSD |
| applicationinsights | 0.11.10 | https://github.com/Microsoft/ApplicationInsights-Python | [MIT License](https://api.github.com/repos/microsoft/applicationinsights-python/license) |
| argcomplete | 1.12.3 | https://github.com/kislyuk/argcomplete | [Apache License 2.0](https://api.github.com/repos/kislyuk/argcomplete/license) |
| attrs | 21.1.0 | https://www.attrs.org/ | MIT |
| azure-appconfiguration | 1.1.1 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/appconfiguration/azure-appconfiguration | MIT License |
| azure-batch | 10.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-cli-core | 2.23.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-telemetry | 1.0.6 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli | 2.23.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-common | 1.1.27 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-core | 1.13.0 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-core | MIT License |
| azure-cosmos | 3.2.0 | https://github.com/Azure/azure-documentdb-python | [MIT License](https://api.github.com/repos/azure/azure-documentdb-python/license) |
| azure-datalake-store | 0.0.52 | https://github.com/Azure/azure-data-lake-store-python | [Other](https://api.github.com/repos/azure/azure-data-lake-store-python/license) |
| azure-functions-devops-build | 0.0.22 | https://github.com/Azure/azure-functions-devops-build | [MIT License](https://api.github.com/repos/azure/azure-functions-devops-build/license) |
| azure-graphrbac | 0.60.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-identity | 1.5.0 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity | MIT License |
| azure-keyvault-administration | 4.0.0b3 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/keyvault/azure-keyvault-administration | MIT License |
| azure-keyvault | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-loganalytics | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-advisor | 2.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-apimanagement | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-appconfiguration | 1.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-applicationinsights | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-authorization | 0.61.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batch | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batchai | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-billing | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-botservice | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cdn | 11.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cognitiveservices | 6.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-compute | 20.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-consumption | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerinstance | 1.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerregistry | 3.0.0rc17 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerservice | 11.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-core | 1.2.2 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/core/azure-mgmt-core | MIT License |
| azure-mgmt-cosmosdb | 6.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-databoxedge | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-analytics | 0.2.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-nspkg | 3.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-store | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datamigration | 4.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-deploymentmanager | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-devtestlabs | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-dns | 8.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventgrid | 3.0.0rc9 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventhub | 4.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-hdinsight | 2.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-imagebuilder | 0.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iotcentral | 4.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothub | 0.12.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothubprovisioningservices | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-keyvault | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-kusto | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-loganalytics | 8.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-managedservices | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-managementgroups | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-maps | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-marketplaceordering | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-media | 3.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-monitor | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-msi | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-netapp | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-network | 18.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-policyinsights | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-privatedns | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-rdbms | 8.1.0b4 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservices | 0.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservicesbackup | 0.11.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-redhatopenshift | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-redis | 7.0.0rc2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-relay | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-reservations | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-resource | 12.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-search | 8.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-security | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicebus | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicefabric | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicefabricmanagedclusters | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-signalr | 0.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sql | 0.26.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sqlvirtualmachine | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-storage | 17.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-synapse | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-trafficmanager | 0.51.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-web | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-multiapi-storage | 0.6.2 | https://github.com/Azure/azure-multiapi-storage-python | [MIT License](https://api.github.com/repos/azure/azure-multiapi-storage-python/license) |
| azure-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-storage-common | 1.4.2 | https://github.com/Azure/azure-storage-python | [MIT License](https://api.github.com/repos/azure/azure-storage-python/license) |
| azure-synapse-accesscontrol | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-synapse-artifacts | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-synapse-spark | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| bcrypt | 3.2.0 | https://github.com/pyca/bcrypt/ | [Apache License 2.0](https://api.github.com/repos/pyca/bcrypt/license) |
| boto3 | 1.17.67 | https://github.com/boto/boto3 | [Apache License 2.0](https://api.github.com/repos/boto/boto3/license) |
| botocore | 1.20.67 | https://github.com/boto/botocore | [Apache License 2.0](https://api.github.com/repos/boto/botocore/license) |
| certifi | 2020.12.5 | https://certifiio.readthedocs.io/en/latest/ | MPL-2.0 |
| cffi | 1.14.5 | http://cffi.readthedocs.org | MIT |
| chardet | 4.0.0 | https://github.com/chardet/chardet | [GNU Lesser General Public License v2.1](https://api.github.com/repos/chardet/chardet/license) |
| colorama | 0.4.4 | https://github.com/tartley/colorama | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/tartley/colorama/license) |
| cryptography | 3.3.2 | https://github.com/pyca/cryptography | [Other](https://api.github.com/repos/pyca/cryptography/license) |
| fabric | 2.6.0 | http://fabfile.org | BSD |
| humanfriendly | 9.1 | https://humanfriendly.readthedocs.io | MIT |
| idna | 2.10 | https://github.com/kjd/idna | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/kjd/idna/license) |
| importlib-metadata | 1.7.0 | http://importlib-metadata.readthedocs.io/ | Apache Software License |
| invoke | 1.5.0 | http://docs.pyinvoke.org | BSD |
| isodate | 0.6.0 | https://github.com/gweis/isodate/ | BSD |
| javaproperties | 0.5.1 | https://github.com/jwodder/javaproperties | [MIT License](https://api.github.com/repos/jwodder/javaproperties/license) |
| Jinja2 | 2.11.3 | https://palletsprojects.com/p/jinja/ | BSD-3-Clause |
| jmespath | 0.10.0 | https://github.com/jmespath/jmespath.py | [Other](https://api.github.com/repos/jmespath/jmespath.py/license) |
| jsmin | 2.2.2 | https://github.com/tikitu/jsmin/ | [MIT License](https://api.github.com/repos/tikitu/jsmin/license) |
| jsondiff | 1.2.0 | https://github.com/ZoomerAnalytics/jsondiff | [MIT License](https://api.github.com/repos/zoomeranalytics/jsondiff/license) |
| jsonschema | 3.2.0 | https://github.com/Julian/jsonschema | [MIT License](https://api.github.com/repos/julian/jsonschema/license) |
| knack | 0.8.1 | https://github.com/microsoft/knack | [MIT License](https://api.github.com/repos/microsoft/knack/license) |
| MarkupSafe | 1.1.1 | https://palletsprojects.com/p/markupsafe/ | BSD-3-Clause |
| mock | 4.0.3 | http://mock.readthedocs.org/en/latest/ | UNKNOWN |
| msal-extensions | 0.3.0 | UNKNOWN | UNKNOWN |
| msal | 1.11.0 | https://github.com/AzureAD/microsoft-authentication-library-for-python | [Other](https://api.github.com/repos/azuread/microsoft-authentication-library-for-python/license) |
| msrest | 0.6.21 | https://github.com/Azure/msrest-for-python | [MIT License](https://api.github.com/repos/azure/msrest-for-python/license) |
| msrestazure | 0.6.4 | https://github.com/Azure/msrestazure-for-python | [MIT License](https://api.github.com/repos/azure/msrestazure-for-python/license) |
| oauthlib | 3.1.0 | https://github.com/oauthlib/oauthlib | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/oauthlib/oauthlib/license) |
| packaging | 20.9 | https://github.com/pypa/packaging | [Other](https://api.github.com/repos/pypa/packaging/license) |
| paramiko | 2.7.2 | https://github.com/paramiko/paramiko/ | [GNU Lesser General Public License v2.1](https://api.github.com/repos/paramiko/paramiko/license) |
| pathlib2 | 2.3.5 | https://github.com/mcmtroffaes/pathlib2 | [MIT License](https://api.github.com/repos/mcmtroffaes/pathlib2/license) |
| pkginfo | 1.7.0 | https://code.launchpad.net/~tseaver/pkginfo/trunk | MIT |
| portalocker | 1.7.1 | https://github.com/WoLpH/portalocker | [Other](https://api.github.com/repos/wolph/portalocker/license) |
| psutil | 5.8.0 | https://github.com/giampaolo/psutil | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/giampaolo/psutil/license) |
| pycparser | 2.20 | https://github.com/eliben/pycparser | [Other](https://api.github.com/repos/eliben/pycparser/license) |
| Pygments | 2.9.0 | https://pygments.org/ | BSD License |
| PyJWT | 1.7.1 | http://github.com/jpadilla/pyjwt | [MIT License](https://api.github.com/repos/jpadilla/pyjwt/license) |
| PyNaCl | 1.4.0 | https://github.com/pyca/pynacl/ | [Apache License 2.0](https://api.github.com/repos/pyca/pynacl/license) |
| pyOpenSSL | 20.0.1 | https://pyopenssl.org/ | Apache License, Version 2.0 |
| pyparsing | 2.4.7 | https://github.com/pyparsing/pyparsing/ | [MIT License](https://api.github.com/repos/pyparsing/pyparsing/license) |
| pyrsistent | 0.17.3 | http://github.com/tobgu/pyrsistent/ | [MIT License](https://api.github.com/repos/tobgu/pyrsistent/license) |
| python-dateutil | 2.8.1 | https://dateutil.readthedocs.io | Dual License |
| python-json-logger | 2.0.1 | http://github.com/madzak/python-json-logger | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/madzak/python-json-logger/license) |
| pytz | 2019.1 | http://pythonhosted.org/pytz | MIT |
| PyYAML | 5.4.1 | https://pyyaml.org/ | MIT |
| requests-oauthlib | 1.3.0 | https://github.com/requests/requests-oauthlib | [ISC License](https://api.github.com/repos/requests/requests-oauthlib/license) |
| requests | 2.25.1 | https://requests.readthedocs.io | Apache 2.0 |
| ruamel.yaml.clib | 0.2.2 | https://sourceforge.net/p/ruamel-yaml-clib/code/ci/default/tree | MIT |
| ruamel.yaml | 0.17.4 | https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree | MIT license |
| s3transfer | 0.4.2 | https://github.com/boto/s3transfer | [Apache License 2.0](https://api.github.com/repos/boto/s3transfer/license) |
| scp | 0.13.3 | https://github.com/jbardin/scp.py | [Other](https://api.github.com/repos/jbardin/scp.py/license) |
| semver | 2.13.0 | https://github.com/python-semver/python-semver | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/python-semver/python-semver/license) |
| six | 1.16.0 | https://github.com/benjaminp/six | [MIT License](https://api.github.com/repos/benjaminp/six/license) |
| sshtunnel | 0.1.5 | https://github.com/pahaz/sshtunnel | [MIT License](https://api.github.com/repos/pahaz/sshtunnel/license) |
| tabulate | 0.8.9 | https://github.com/astanin/python-tabulate | [MIT License](https://api.github.com/repos/astanin/python-tabulate/license) |
| terraform-bin | 1.0.1 | https://github.com/epiphany-platform/terraform-bin | [Apache License 2.0](https://api.github.com/repos/epiphany-platform/terraform-bin/license) |
| typing-extensions | 3.10.0.0 | https://github.com/python/typing/blob/master/typing_extensions/README.rst | PSF |
| urllib3 | 1.26.4 | https://urllib3.readthedocs.io/ | MIT |
| vsts-cd-manager | 1.0.2 | https://github.com/microsoft/vsts-cd-manager | [MIT License](https://api.github.com/repos/microsoft/vsts-cd-manager/license) |
| vsts | 0.1.25 | https://github.com/Microsoft/vsts-python-api | [MIT License](https://api.github.com/repos/microsoft/vsts-python-api/license) |
| websocket-client | 0.56.0 | https://github.com/websocket-client/websocket-client.git | BSD |
| xmltodict | 0.12.0 | https://github.com/martinblech/xmltodict | [MIT License](https://api.github.com/repos/martinblech/xmltodict/license) |
| zipp | 3.4.1 | https://github.com/jaraco/zipp | [MIT License](https://api.github.com/repos/jaraco/zipp/license) |
