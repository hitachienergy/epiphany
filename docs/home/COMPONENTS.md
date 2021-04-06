# Component and dependency versions and licenses

## Epiphany cluster components

Note that versions are default versions and can be changed in certain cases through configuration. Versions that are marked with '-' are dependent on the OS distribution version and packagemanager.

| Component                 | Version | Repo/Website                                          | License                                                           |
| ------------------------- | ------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Kubernetes                | 1.17.4  | https://github.com/kubernetes/kubernetes              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Calico                    | -       | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Flannel                   | -       | https://github.com/coreos/flannel/                    | [Apache License](https://www.apache.org/licenses/LICENSE-1.0)     |
| Canal                     | -       | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka                     | 2.3.1   | https://github.com/apache/kafka                       | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Zookeeper                 | 3.4.12  | https://github.com/apache/zookeeper                   | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| RabbitMQ                  | 3.8.9  | https://github.com/rabbitmq/rabbitmq-server           | [Mozilla Public License](https://www.mozilla.org/en-US/MPL/)      |
| Docker-ce                 | 18.09   | https://github.com/docker/docker-ce/                  | [Apache License](https://www.apache.org/licenses/LICENSE-1.0)     |
| KeyCloak                  | 9.0.0   | https://github.com/keycloak/keycloak                  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Elasticsearch OSS         | 7.6.1   | https://github.com/elastic/elasticsearch              | https://github.com/elastic/elasticsearch/blob/master/LICENSE.txt  |
| Elasticsearch Curator OSS | 5.8.3   | https://github.com/elastic/curator                    | https://github.com/elastic/curator/blob/master/LICENSE.txt        |
| Kibana                    | 6.5.4   | https://github.com/elastic/kibana                     | https://github.com/elastic/kibana/blob/master/LICENSE.txt         |
| Opendistro for Elasticsearch  | 1.3.0   | https://opendistro.github.io/for-elasticsearch/  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  |
| Opendistro for Elasticsearch Kibana  | 1.3.0   | https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)  |
| Filebeat                  | 6.8.5   | https://github.com/elastic/beats/tree/6.8             | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Prometheus                | 2.10.0  | https://github.com/prometheus/prometheus              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Grafana                   | 6.2.5   | https://github.com/grafana/grafana                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| node_exporter             | 0.16.0  | https://github.com/prometheus/node_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| kafka_exporter            | 1.2.0   | https://github.com/danielqsj/kafka_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| haproxy_exporter          | 0.10.0  | https://github.com/prometheus/haproxy_exporter        | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| jmx_exporter              | 0.12.0  | https://github.com/prometheus/jmx_exporter            | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| PostgreSQL                | 10      | https://www.postgresql.org/                           | https://opensource.org/licenses/postgresql                        |
| HAProxy                   | 1.8     | https://www.haproxy.org/                              | [GNU General Public License 2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| PGAudit                   | 1.2.0   | https://github.com/pgaudit/pgaudit                    | [PostgreSQL license](http://www.postgresql.org/about/licence/)    |
| PGBouncer                 | 1.10.0  | https://github.com/pgbouncer/pgbouncer                | [ISC License](https://opensource.org/licenses/isc)                |
| repmgr                    | 4.0.6   | https://github.com/2ndQuadrant/repmgr                 | [Apache License 2.0](https://github.com/2ndQuadrant/repmgr/blob/master/LICENSE) |
| PGPool                    | 4.1.1   | https://www.pgpool.net/                               | [License](https://www.pgpool.net/mediawiki/index.php/pgpool-II_License) |
| alertmanager              | 0.17.0  | https://github.com/prometheus/alertmanager            | [Apache License 2.0](https://github.com/prometheus/alertmanager/blob/master/LICENSE) |
| ignite                    | 2.5.0   | https://github.com/apache/ignite                      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Apache2                   | 2.4.29  | https://httpd.apache.org/                             | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |

## Epicli binary dependencies

| Component                 | Version | Repo/Website                                          | License                                                           |
| ------------------------- | ------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Terraform                 | 0.12.6  | https://www.terraform.io/                             | [Mozilla Public License 2.0](https://github.com/hashicorp/terraform/blob/master/LICENSE) |
| Terraform AzureRM provider | 1.38.0  | https://github.com/terraform-providers/terraform-provider-azurerm | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/LICENSE) |
| Terraform AWS provider    | 2.26    | https://github.com/terraform-providers/terraform-provider-aws | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-aws/blob/master/LICENSE) |
| Skopeo                    | 0.1.40-dev  | https://github.com/containers/skopeo              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |

## Epicli Python dependencies

| Component | Version | Repo/Website | License |
| --------- | ------- | ------------ | ------- |
| adal | 1.2.2 | https://github.com/AzureAD/azure-activedirectory-library-for-python | [Other](https://api.github.com/repos/azuread/azure-activedirectory-library-for-python/license) |
| ansible | 2.8.8 | https://ansible.com/ | GPLv3+ |
| antlr4-python3-runtime | 4.7.2 | http://www.antlr.org | BSD |
| applicationinsights | 0.11.7 | https://github.com/Microsoft/ApplicationInsights-Python | [MIT License](https://api.github.com/repos/microsoft/applicationinsights-python/license) |
| argcomplete | 1.10.0 | https://github.com/kislyuk/argcomplete | [Apache License 2.0](https://api.github.com/repos/kislyuk/argcomplete/license) |
| astroid | 2.3.3 | https://github.com/PyCQA/astroid | [GNU Lesser General Public License v2.1](https://api.github.com/repos/pycqa/astroid/license) |
| attrs | 19.3.0 | https://www.attrs.org/ | MIT |
| azure-batch | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-cli | 2.0.67 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-acr | 2.2.9 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-acs | 2.4.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-advisor | 2.0.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-ams | 0.4.7 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-appservice | 0.2.21 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-backup | 1.2.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-batch | 4.0.3 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-batchai | 0.4.10 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-billing | 0.2.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-botservice | 0.2.2 | https://github.com/azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-cdn | 0.2.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-cloud | 2.1.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-cognitiveservices | 0.2.6 | https://github.com/azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-command-modules-nspkg | 2.0.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-configure | 2.0.24 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-consumption | 0.4.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-container | 0.3.18 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-core | 2.0.67 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-cosmosdb | 0.2.11 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-deploymentmanager | 0.1.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-dla | 0.2.6 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-dls | 0.1.10 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-dms | 0.1.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-eventgrid | 0.2.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-eventhubs | 0.3.7 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-extension | 0.2.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-feedback | 2.2.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-find | 0.3.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-hdinsight | 0.3.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-interactive | 0.4.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-iot | 0.3.11 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-iotcentral | 0.1.7 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-keyvault | 2.2.16 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-kusto | 0.2.3 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-lab | 0.1.8 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-maps | 0.3.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-monitor | 0.2.15 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-natgateway | 0.1.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-network | 2.5.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-nspkg | 3.0.3 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-policyinsights | 0.1.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-privatedns | 1.0.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-profile | 2.1.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-rdbms | 0.3.12 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-redis | 0.4.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-relay | 0.1.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-reservations | 0.4.3 | https://github.com/azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-resource | 2.1.16 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-role | 2.6.4 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-search | 0.1.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-security | 0.1.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-servicebus | 0.3.6 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-servicefabric | 0.1.20 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-signalr | 1.0.1 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-sql | 2.2.5 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-sqlvm | 0.2.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-storage | 2.4.3 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-telemetry | 1.0.2 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-vm | 2.2.23 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-common | 1.1.23 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-cosmos | 3.1.2 | https://github.com/Azure/azure-documentdb-python | [MIT License](https://api.github.com/repos/azure/azure-documentdb-python/license) |
| azure-datalake-store | 0.0.39 | https://github.com/Azure/azure-data-lake-store-python | [Other](https://api.github.com/repos/azure/azure-data-lake-store-python/license) |
| azure-functions-devops-build | 0.0.22 | https://github.com/Azure/azure-functions-devops-build | [MIT License](https://api.github.com/repos/azure/azure-functions-devops-build/license) |
| azure-graphrbac | 0.60.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-keyvault | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-advisor | 2.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-applicationinsights | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-authorization | 0.50.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batch | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batchai | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-billing | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-botservice | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cdn | 3.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cognitiveservices | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-compute | 5.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-consumption | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerinstance | 1.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerregistry | 2.8.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerservice | 5.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cosmosdb | 0.6.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-analytics | 0.2.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-nspkg | 3.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-store | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datamigration | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-deploymentmanager | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-devtestlabs | 2.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-dns | 2.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventgrid | 2.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventhub | 2.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-hdinsight | 0.2.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-imagebuilder | 0.2.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iotcentral | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothub | 0.8.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothubprovisioningservices | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-keyvault | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-kusto | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-loganalytics | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-managementgroups | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-maps | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-marketplaceordering | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-media | 1.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-monitor | 0.5.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-msi | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-network | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-policyinsights | 0.3.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-privatedns | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-rdbms | 1.8.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservices | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservicesbackup | 0.1.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-redis | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-relay | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-reservations | 0.3.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-resource | 2.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-search | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-security | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicebus | 0.6.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicefabric | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-signalr | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sql | 0.12.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sqlvirtualmachine | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-storage | 3.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-trafficmanager | 0.51.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-web | 0.42.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-multiapi-storage | 0.2.3 | https://github.com/Azure/azure-multiapi-storage-python | [MIT License](https://api.github.com/repos/azure/azure-multiapi-storage-python/license) |
| azure-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-storage-blob | 1.3.1 | https://github.com/Azure/azure-storage-python | [MIT License](https://api.github.com/repos/azure/azure-storage-python/license) |
| azure-storage-common | 1.4.2 | https://github.com/Azure/azure-storage-python | [MIT License](https://api.github.com/repos/azure/azure-storage-python/license) |
| azure-storage-nspkg | 3.1.0 | https://github.com/Azure/azure-storage-python | [MIT License](https://api.github.com/repos/azure/azure-storage-python/license) |
| bcrypt | 3.1.7 | https://github.com/pyca/bcrypt/ | [Apache License 2.0](https://api.github.com/repos/pyca/bcrypt/license) |
| bleach | 3.1.1 | https://github.com/mozilla/bleach | [Other](https://api.github.com/repos/mozilla/bleach/license) |
| boto3 | 1.10.9 | https://github.com/boto/boto3 | [Apache License 2.0](https://api.github.com/repos/boto/boto3/license) |
| botocore | 1.13.9 | https://github.com/boto/botocore | [Apache License 2.0](https://api.github.com/repos/boto/botocore/license) |
| certifi | 2019.9.11 | https://certifi.io/ | MPL-2.0 |
| cffi | 1.13.2 | http://cffi.readthedocs.org | MIT |
| chardet | 3.0.4 | https://github.com/chardet/chardet | [GNU Lesser General Public License v2.1](https://api.github.com/repos/chardet/chardet/license) |
| colorama | 0.4.1 | https://github.com/tartley/colorama | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/tartley/colorama/license) |
| cryptography | 2.8 | https://github.com/pyca/cryptography | [Other](https://api.github.com/repos/pyca/cryptography/license) |
| docutils | 0.15.2 | http://docutils.sourceforge.net/ | public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt) |
| fabric | 2.5.0 | http://fabfile.org | BSD |
| humanfriendly | 4.18 | https://humanfriendly.readthedocs.io | MIT |
| idna | 2.8 | https://github.com/kjd/idna | [Other](https://api.github.com/repos/kjd/idna/license) |
| importlib-metadata | 0.23 | http://importlib-metadata.readthedocs.io/ | Apache Software License |
| invoke | 1.3.0 | http://docs.pyinvoke.org | BSD |
| isodate | 0.6.0 | https://github.com/gweis/isodate/ | BSD |
| isort | 4.3.21 | https://github.com/timothycrosley/isort | [MIT License](https://api.github.com/repos/timothycrosley/isort/license) |
| jeepney | 0.4.2 | https://gitlab.com/takluyver/jeepney | UNKNOWN |
| Jinja2 | 2.10.3 | https://palletsprojects.com/p/jinja/ | BSD-3-Clause |
| jmespath | 0.9.4 | https://github.com/jmespath/jmespath.py | [Other](https://api.github.com/repos/jmespath/jmespath.py/license) |
| jsonschema | 3.1.1 | https://github.com/Julian/jsonschema | [MIT License](https://api.github.com/repos/julian/jsonschema/license) |
| keyring | 21.1.0 | https://github.com/jaraco/keyring | [MIT License](https://api.github.com/repos/jaraco/keyring/license) |
| knack | 0.6.3 | https://github.com/microsoft/knack | [MIT License](https://api.github.com/repos/microsoft/knack/license) |
| lazy-object-proxy | 1.4.3 | https://github.com/ionelmc/python-lazy-object-proxy | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/ionelmc/python-lazy-object-proxy/license) |
| MarkupSafe | 1.1.1 | https://palletsprojects.com/p/markupsafe/ | BSD-3-Clause |
| mccabe | 0.6.1 | https://github.com/pycqa/mccabe | [Other](https://api.github.com/repos/pycqa/mccabe/license) |
| mock | 3.0.5 | http://mock.readthedocs.org/en/latest/ | OSI Approved :: BSD License |
| more-itertools | 7.2.0 | https://github.com/erikrose/more-itertools | [MIT License](https://api.github.com/repos/erikrose/more-itertools/license) |
| msrest | 0.6.10 | https://github.com/Azure/msrest-for-python | [MIT License](https://api.github.com/repos/azure/msrest-for-python/license) |
| msrestazure | 0.6.2 | https://github.com/Azure/msrestazure-for-python | [MIT License](https://api.github.com/repos/azure/msrestazure-for-python/license) |
| oauthlib | 3.1.0 | https://github.com/oauthlib/oauthlib | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/oauthlib/oauthlib/license) |
| packaging | 20.1 | https://github.com/pypa/packaging | [Other](https://api.github.com/repos/pypa/packaging/license) |
| paramiko | 2.6.0 | https://github.com/paramiko/paramiko/ | [GNU Lesser General Public License v2.1](https://api.github.com/repos/paramiko/paramiko/license) |
| pkginfo | 1.5.0.1 | https://code.launchpad.net/~tseaver/pkginfo/trunk | MIT |
| pluggy | 0.13.1 | https://github.com/pytest-dev/pluggy | [MIT License](https://api.github.com/repos/pytest-dev/pluggy/license) |
| portalocker | 1.2.1 | https://github.com/WoLpH/portalocker | [Other](https://api.github.com/repos/wolph/portalocker/license) |
| prompt-toolkit | 1.0.18 | https://github.com/jonathanslenders/python-prompt-toolkit | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/jonathanslenders/python-prompt-toolkit/license) |
| psutil | 5.6.4 | https://github.com/giampaolo/psutil | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/giampaolo/psutil/license) |
| py | 1.8.1 | http://py.readthedocs.io/ | MIT license |
| pycparser | 2.19 | https://github.com/eliben/pycparser | [Other](https://api.github.com/repos/eliben/pycparser/license) |
| Pygments | 2.4.2 | http://pygments.org/ | BSD License |
| PyJWT | 1.7.1 | http://github.com/jpadilla/pyjwt | [MIT License](https://api.github.com/repos/jpadilla/pyjwt/license) |
| PyNaCl | 1.3.0 | https://github.com/pyca/pynacl/ | [Apache License 2.0](https://api.github.com/repos/pyca/pynacl/license) |
| pyOpenSSL | 19.0.0 | https://pyopenssl.org/ | Apache License, Version 2.0 |
| pyparsing | 2.4.6 | https://github.com/pyparsing/pyparsing/ | [MIT License](https://api.github.com/repos/pyparsing/pyparsing/license) |
| pyperclip | 1.7.0 | https://github.com/asweigart/pyperclip | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/asweigart/pyperclip/license) |
| pyrsistent | 0.15.5 | http://github.com/tobgu/pyrsistent/ | [MIT License](https://api.github.com/repos/tobgu/pyrsistent/license) |
| python-dateutil | 2.8.0 | https://dateutil.readthedocs.io | Dual License |
| python-json-logger | 0.1.11 | http://github.com/madzak/python-json-logger | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/madzak/python-json-logger/license) |
| pytz | 2019.3 | http://pythonhosted.org/pytz | MIT |
| PyYAML | 5.3 | https://github.com/yaml/pyyaml | [MIT License](https://api.github.com/repos/yaml/pyyaml/license) |
| readme-renderer | 24.0 | https://github.com/pypa/readme_renderer | [Apache License 2.0](https://api.github.com/repos/pypa/readme_renderer/license) |
| requests | 2.22.0 | http://python-requests.org | Apache 2.0 |
| requests-oauthlib | 1.2.0 | https://github.com/requests/requests-oauthlib | [ISC License](https://api.github.com/repos/requests/requests-oauthlib/license) |
| requests-toolbelt | 0.9.1 | https://toolbelt.readthedocs.org | Apache 2.0 |
| ruamel.yaml | 0.16.10 | https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree | MIT license |
| ruamel.yaml.clib | 0.2.0 | https://bitbucket.org/ruamel/yaml.clib | MIT |
| s3transfer | 0.2.1 | https://github.com/boto/s3transfer | [Apache License 2.0](https://api.github.com/repos/boto/s3transfer/license) |
| scp | 0.13.2 | https://github.com/jbardin/scp.py | [Other](https://api.github.com/repos/jbardin/scp.py/license) |
| SecretStorage | 3.1.2 | https://github.com/mitya57/secretstorage | [Other](https://api.github.com/repos/mitya57/secretstorage/license) |
| six | 1.12.0 | https://github.com/benjaminp/six | [MIT License](https://api.github.com/repos/benjaminp/six/license) |
| skopeo-bin | 1.0.3 | https://github.com/epiphany-platform/skopeo-bin | [Apache License 2.0](https://api.github.com/repos/epiphany-platform/skopeo-bin/license) |
| sshtunnel | 0.1.5 | https://github.com/pahaz/sshtunnel | [MIT License](https://api.github.com/repos/pahaz/sshtunnel/license) |
| tabulate | 0.8.5 | https://github.com/astanin/python-tabulate | [MIT License](https://api.github.com/repos/astanin/python-tabulate/license) |
| terraform-bin | 1.0.1 | https://github.com/epiphany-platform/terraform-bin | [Apache License 2.0](https://api.github.com/repos/epiphany-platform/terraform-bin/license) |
| tqdm | 4.43.0 | https://github.com/tqdm/tqdm | [Other](https://api.github.com/repos/tqdm/tqdm/license) |
| typed-ast | 1.4.1 | https://github.com/python/typed_ast | [Other](https://api.github.com/repos/python/typed_ast/license) |
| urllib3 | 1.25.6 | https://urllib3.readthedocs.io/ | MIT |
| vsts | 0.1.25 | https://github.com/Microsoft/vsts-python-api | [MIT License](https://api.github.com/repos/microsoft/vsts-python-api/license) |
| vsts-cd-manager | 1.0.2 | https://github.com/microsoft/vsts-cd-manager | [MIT License](https://api.github.com/repos/microsoft/vsts-cd-manager/license) |
| wcwidth | 0.1.7 | https://github.com/jquast/wcwidth | [MIT License](https://api.github.com/repos/jquast/wcwidth/license) |
| webencodings | 0.5.1 | https://github.com/SimonSapin/python-webencodings | [Other](https://api.github.com/repos/simonsapin/python-webencodings/license) |
| websocket-client | 0.56.0 | https://github.com/websocket-client/websocket-client.git | BSD |
| wrapt | 1.11.2 | https://github.com/GrahamDumpleton/wrapt | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/grahamdumpleton/wrapt/license) |
| xmltodict | 0.12.0 | https://github.com/martinblech/xmltodict | [MIT License](https://api.github.com/repos/martinblech/xmltodict/license) |
| zipp | 0.6.0 | https://github.com/jaraco/zipp | [MIT License](https://api.github.com/repos/jaraco/zipp/license) |

