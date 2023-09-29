# Component and dependency versions and licenses

## Epiphany cluster components

Note that versions are default versions and can be changed in certain cases through configuration. Versions that are marked with '-' are dependent on the OS distribution version and packagemanager.

| Component                  | Version  | Repo/Website                                          | License                                                           |
| -------------------------- | -------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Alertmanager               | 0.23.0   | https://github.com/prometheus/alertmanager            | [Apache License 2.0](https://github.com/prometheus/alertmanager/blob/master/LICENSE) |
| Apache2                    | 2.4.29   | https://httpd.apache.org/                             | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| curator-opensearch         | 0.0.9    | https://github.com/flant/curator-opensearch           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka                      | 2.8.1    | https://github.com/apache/kafka                       | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Zookeeper                  | 3.5.8    | https://github.com/apache/zookeeper                   | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat                   | 7.12.1   | https://github.com/elastic/beats                      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat Helm Chart        | 7.12.1   | https://github.com/elastic/helm-charts                | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Prometheus                 | 2.31.1   | https://github.com/prometheus/prometheus              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Grafana                    | 10.0.3   | https://github.com/grafana/grafana                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Node Exporter              | 1.6.1    | https://github.com/prometheus/node_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Bitnami Node Exporter Helm Chart      | 3.6.2    | https://github.com/bitnami/charts          | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka Exporter             | 1.4.0    | https://github.com/danielqsj/kafka_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| JMX Exporter               | 0.16.1   | https://github.com/prometheus/jmx_exporter            | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| OpenSearch                 | 2.8.0    | https://github.com/opensearch-project/OpenSearch      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| OpenSearch Dashboards      | 2.8.0    | https://github.com/opensearch-project/OpenSearch-Dashboards | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |

## Epicli binary dependencies

| Component                 | Version | Repo/Website                                          | License                                                           |
| ------------------------- | ------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Terraform                 | 1.1.3   | https://www.terraform.io/                             | [Mozilla Public License 2.0](https://github.com/hashicorp/terraform/blob/master/LICENSE) |
| Terraform AzureRM provider | 3.74.0 | https://github.com/terraform-providers/terraform-provider-azurerm | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/LICENSE) |
| Terraform AWS provider     | 3.71.0  | https://github.com/terraform-providers/terraform-provider-aws | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-aws/blob/master/LICENSE) |
| Crane                      | 0.11.0  | https://github.com/google/go-containerregistry/tree/main/cmd/crane     | [Apache License 2.0](https://github.com/google/go-containerregistry/blob/main/LICENSE) |
| Git                        | latest | https://github.com/git/git | [GNU GENERAL PUBLIC LICENSE Version 2](https://github.com/git/git/blob/master/COPYING) |
| aws-cli                    | 2.0.30  | https://github.com/aws/aws-cli | [Apache License 2.0](https://github.com/aws/aws-cli/blob/develop/LICENSE.txt) |

## Epicli Python dependencies

| Component | Version | Repo/Website | License |
| --------- | ------- | ------------ | ------- |
| adal | 1.2.7 | https://github.com/AzureAD/azure-activedirectory-library-for-python | [Other](https://api.github.com/repos/azuread/azure-activedirectory-library-for-python/license) |
| ansible-core | 2.13.11 | https://ansible.com/ | GPLv3+ |
| ansible | 6.7.0 | https://ansible.com/ | GPLv3+ |
| antlr4-python3-runtime | 4.9.3 | http://www.antlr.org | BSD |
| applicationinsights | 0.11.10 | https://github.com/Microsoft/ApplicationInsights-Python | [MIT License](https://api.github.com/repos/microsoft/applicationinsights-python/license) |
| argcomplete | 3.1.1 | https://github.com/kislyuk/argcomplete | [Apache License 2.0](https://api.github.com/repos/kislyuk/argcomplete/license) |
| attrs | 23.1.0 | https://www.attrs.org/ | MIT |
| azure-appconfiguration | 1.1.1 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/appconfiguration/azure-appconfiguration | MIT License |
| azure-batch | 14.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-cli-core | 2.51.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli-telemetry | 1.1.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-cli | 2.51.0 | https://github.com/Azure/azure-cli | [MIT License](https://api.github.com/repos/azure/azure-cli/license) |
| azure-common | 1.1.28 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-core | 1.29.2 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-core | MIT License |
| azure-cosmos | 3.2.0 | https://github.com/Azure/azure-documentdb-python | [MIT License](https://api.github.com/repos/azure/azure-documentdb-python/license) |
| azure-data-tables | 12.4.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/table/azure-table | MIT License |
| azure-datalake-store | 0.0.53 | https://github.com/Azure/azure-data-lake-store-python | [MIT License](https://api.github.com/repos/azure/azure-data-lake-store-python/license) |
| azure-graphrbac | 0.60.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-keyvault-administration | 4.3.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-administration | MIT License |
| azure-keyvault-certificates | 4.7.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-certificates | MIT License |
| azure-keyvault-keys | 4.8.0b2 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-keys | MIT License |
| azure-keyvault-secrets | 4.7.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-secrets | MIT License |
| azure-keyvault | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-loganalytics | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-advisor | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-apimanagement | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-appconfiguration | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-appcontainers | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-applicationinsights | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-authorization | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batch | 17.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-batchai | 7.0.0b1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-billing | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-botservice | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cdn | 12.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-cognitiveservices | 13.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-compute | 30.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-consumption | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerinstance | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerregistry | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-containerservice | 25.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-core | 1.4.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-mgmt-core | MIT License |
| azure-mgmt-cosmosdb | 9.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-databoxedge | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-analytics | 0.2.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-nspkg | 3.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datalake-store | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-datamigration | 10.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-devtestlabs | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-dns | 8.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventgrid | 10.2.0b2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-eventhub | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-extendedlocation | 1.0.0b2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-hdinsight | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-imagebuilder | 1.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iotcentral | 10.0.0b2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothub | 2.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-iothubprovisioningservices | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-keyvault | 10.2.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-kusto | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-loganalytics | 13.0.0b4 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-managedservices | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-managementgroups | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-maps | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-marketplaceordering | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-media | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-monitor | 5.0.1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-msi | 7.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-netapp | 10.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-policyinsights | 1.1.0b4 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-privatedns | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-rdbms | 10.2.0b10 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservices | 2.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-recoveryservicesbackup | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-redhatopenshift | 1.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-redis | 14.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-relay | 0.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-resource | 23.1.0b2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-search | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-security | 5.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicebus | 8.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicefabric | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicefabricmanagedclusters | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-servicelinker | 1.2.0b1 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-signalr | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sql | 4.0.0b10 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-sqlvirtualmachine | 1.0.0b5 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-storage | 21.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-synapse | 2.1.0b5 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-trafficmanager | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-mgmt-web | 7.0.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-multiapi-storage | 1.2.0 | https://github.com/Azure/azure-multiapi-storage-python | [MIT License](https://api.github.com/repos/azure/azure-multiapi-storage-python/license) |
| azure-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-storage-common | 1.4.2 | https://github.com/Azure/azure-storage-python | [MIT License](https://api.github.com/repos/azure/azure-storage-python/license) |
| azure-synapse-accesscontrol | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-synapse-artifacts | 0.15.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk | MIT License |
| azure-synapse-managedprivateendpoints | 0.4.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| azure-synapse-spark | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | [MIT License](https://api.github.com/repos/azure/azure-sdk-for-python/license) |
| bcrypt | 4.0.1 | https://github.com/pyca/bcrypt/ | [Apache License 2.0](https://api.github.com/repos/pyca/bcrypt/license) |
| boto3 | 1.28.31 | https://github.com/boto/boto3 | [Apache License 2.0](https://api.github.com/repos/boto/boto3/license) |
| botocore | 1.31.31 | https://github.com/boto/botocore | [Apache License 2.0](https://api.github.com/repos/boto/botocore/license) |
| certifi | 2023.7.22 | https://github.com/certifi/python-certifi | [Other](https://api.github.com/repos/certifi/python-certifi/license) |
| cffi | 1.15.1 | http://cffi.readthedocs.org | MIT |
| chardet | 3.0.4 | https://github.com/chardet/chardet | [GNU Lesser General Public License v2.1](https://api.github.com/repos/chardet/chardet/license) |
| charset-normalizer | 3.2.0 | https://github.com/Ousret/charset_normalizer | [MIT License](https://api.github.com/repos/ousret/charset_normalizer/license) |
| click | 8.1.7 | https://palletsprojects.com/p/click/ | BSD-3-Clause |
| colorama | 0.4.6 | https://github.com/tartley/colorama | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/tartley/colorama/license) |
| cryptography | 41.0.3 | https://github.com/pyca/cryptography | [Other](https://api.github.com/repos/pyca/cryptography/license) |
| Deprecated | 1.2.14 | https://github.com/tantale/deprecated | [MIT License](https://api.github.com/repos/tantale/deprecated/license) |
| Antergos Linux | 2015.10 (ISO-Rolling) | https://github.com/python-distro/distro | [Apache License 2.0](https://api.github.com/repos/python-distro/distro/license) |
| fabric | 2.7.1 | https://fabfile.org | BSD |
| humanfriendly | 10.0 | https://humanfriendly.readthedocs.io | MIT |
| idna | 3.4 | https://github.com/kjd/idna | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/kjd/idna/license) |
| invoke | 1.7.3 | https://pyinvoke.org | BSD |
| isodate | 0.6.1 | https://github.com/gweis/isodate/ | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/gweis/isodate/license) |
| javaproperties | 0.5.2 | https://github.com/jwodder/javaproperties | [MIT License](https://api.github.com/repos/jwodder/javaproperties/license) |
| Jinja2 | 3.1.2 | https://palletsprojects.com/p/jinja/ | BSD-3-Clause |
| jmespath | 1.0.1 | https://github.com/jmespath/jmespath.py | [MIT License](https://api.github.com/repos/jmespath/jmespath.py/license) |
| jsondiff | 2.0.0 | https://github.com/ZoomerAnalytics/jsondiff | [MIT License](https://api.github.com/repos/zoomeranalytics/jsondiff/license) |
| jsonschema-specifications | 2023.7.1 | https://json-schema.org/ | MIT |
| jsonschema | 4.17.3 | https://json-schema.org/ | MIT |
| knack | 0.11.0 | https://github.com/microsoft/knack | [MIT License](https://api.github.com/repos/microsoft/knack/license) |
| MarkupSafe | 2.1.3 | https://palletsprojects.com/p/markupsafe/ | BSD-3-Clause |
| msal-extensions | 1.0.0 | https://github.com/AzureAD/microsoft-authentication-extensions-for-python | MIT |
| msal | 1.24.0b1 | https://github.com/AzureAD/microsoft-authentication-library-for-python | [Other](https://api.github.com/repos/azuread/microsoft-authentication-library-for-python/license) |
| msal | 1.24.0b1 | https://github.com/AzureAD/microsoft-authentication-library-for-python | [Other](https://api.github.com/repos/azuread/microsoft-authentication-library-for-python/license) |
| msrest | 0.7.1 | https://github.com/Azure/msrest-for-python | [MIT License](https://api.github.com/repos/azure/msrest-for-python/license) |
| msrestazure | 0.6.4 | https://github.com/Azure/msrestazure-for-python | [MIT License](https://api.github.com/repos/azure/msrestazure-for-python/license) |
| oauthlib | 3.2.2 | https://github.com/oauthlib/oauthlib | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/oauthlib/oauthlib/license) |
| packaging | 23.1 | https://github.com/pypa/packaging | [Other](https://api.github.com/repos/pypa/packaging/license) |
| paramiko | 3.3.1 | https://paramiko.org | LGPL |
| pathlib2 | 2.3.7.post1 | https://github.com/jazzband/pathlib2 | [MIT License](https://api.github.com/repos/jazzband/pathlib2/license) |
| pkginfo | 1.9.6 | https://code.launchpad.net/~tseaver/pkginfo/trunk | MIT |
| portalocker | 2.7.0 | https://github.com/WoLpH/portalocker | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/wolph/portalocker/license) |
| psutil | 5.9.5 | https://github.com/giampaolo/psutil | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/giampaolo/psutil/license) |
| pycparser | 2.21 | https://github.com/eliben/pycparser | [Other](https://api.github.com/repos/eliben/pycparser/license) |
| PyGithub | 1.59.1 | https://github.com/pygithub/pygithub | [GNU Lesser General Public License v3.0](https://api.github.com/repos/pygithub/pygithub/license) |
| Pygments | 2.16.1 | https://pygments.org/ | BSD License |
| PyJWT | 2.8.0 | https://github.com/jpadilla/pyjwt | [MIT License](https://api.github.com/repos/jpadilla/pyjwt/license) |
| PyJWT | 2.8.0 | https://github.com/jpadilla/pyjwt | [MIT License](https://api.github.com/repos/jpadilla/pyjwt/license) |
| PyNaCl | 1.5.0 | https://github.com/pyca/pynacl/ | [Apache License 2.0](https://api.github.com/repos/pyca/pynacl/license) |
| pyOpenSSL | 23.2.0 | https://pyopenssl.org/ | Apache License, Version 2.0 |
| PySocks | 1.7.1 | https://github.com/Anorov/PySocks | [Other](https://api.github.com/repos/anorov/pysocks/license) |
| python-dateutil | 2.8.2 | https://github.com/dateutil/dateutil | [Other](https://api.github.com/repos/dateutil/dateutil/license) |
| python-json-logger | 2.0.7 | http://github.com/madzak/python-json-logger | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/madzak/python-json-logger/license) |
| PyYAML | 6.0.1 | https://pyyaml.org/ | MIT |
| referencing | 0.30.2 | https://json-schema.org/ | MIT |
| requests-oauthlib | 1.3.1 | https://github.com/requests/requests-oauthlib | [ISC License](https://api.github.com/repos/requests/requests-oauthlib/license) |
| requests | 2.31.0 | https://requests.readthedocs.io | Apache 2.0 |
| requests | 2.31.0 | https://requests.readthedocs.io | Apache 2.0 |
| resolvelib | 0.8.1 | https://github.com/sarugaku/resolvelib | [ISC License](https://api.github.com/repos/sarugaku/resolvelib/license) |
| rpds-py | 0.9.2 | https://github.com/crate-py/rpds | [MIT License](https://github.com/crate-py/rpds/blob/main/LICENSE) |
| ruamel.yaml.clib | 0.2.7 | https://sourceforge.net/p/ruamel-yaml-clib/code/ci/default/tree | MIT |
| ruamel.yaml | 0.17.32 | https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree | MIT license |
| s3transfer | 0.6.2 | https://github.com/boto/s3transfer | [Apache License 2.0](https://api.github.com/repos/boto/s3transfer/license) |
| scp | 0.13.6 | https://github.com/jbardin/scp.py | [Other](https://api.github.com/repos/jbardin/scp.py/license) |
| semver | 2.13.0 | https://github.com/python-semver/python-semver | [BSD 3-Clause "New" or "Revised" License](https://api.github.com/repos/python-semver/python-semver/license) |
| six | 1.16.0 | https://github.com/benjaminp/six | [MIT License](https://api.github.com/repos/benjaminp/six/license) |
| sshtunnel | 0.1.5 | https://github.com/pahaz/sshtunnel | [MIT License](https://api.github.com/repos/pahaz/sshtunnel/license) |
| tabulate | 0.9.0 | https://github.com/astanin/python-tabulate | [MIT License](https://api.github.com/repos/astanin/python-tabulate/license) |
| typing_extensions | 4.7.1 | https://github.com/python/typing_extensions | [Other](https://github.com/python/typing_extensions/blob/main/LICENSE) |
| urllib3 | 1.26.16 | https://urllib3.readthedocs.io/ | MIT |
| websocket-client | 1.3.3 | https://github.com/websocket-client/websocket-client.git | Apache-2.0 |
| wrapt | 1.15.0 | https://github.com/GrahamDumpleton/wrapt | [BSD 2-Clause "Simplified" License](https://api.github.com/repos/grahamdumpleton/wrapt/license) |
| xmltodict | 0.13.0 | https://github.com/martinblech/xmltodict | [MIT License](https://api.github.com/repos/martinblech/xmltodict/license) |
