# Component and dependency versions and licenses

## Epiphany cluster components

Note that versions are default versions and can be changed in certain cases through configuration. Versions that are marked with '-' are dependent on the OS distribution version and packagemanager.

| Component                  | Version  | Repo/Website                                          | License                                                           |
| -------------------------- | -------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Kubernetes                 | 1.22.4   | https://github.com/kubernetes/kubernetes              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kubernetes Dashboard       | 2.3.1    | https://github.com/kubernetes/dashboard               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kubernetes metrics-scraper | 1.0.7    | https://github.com/kubernetes-sigs/dashboard-metrics-scraper | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| containerd                 | 1.5.11   | https://github.com/containerd/containerd | [Apache License 2.0](https://github.com/containerd/containerd/blob/main/LICENSE) |
| Calico                     | 3.23.3   | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Flannel                    | 0.14.0   | https://github.com/coreos/flannel/                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)     |
| Canal                      | 3.23.3   | https://github.com/projectcalico/calico               | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Coredns                    | 1.8.4    | https://github.com/coredns/coredns                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka                      | 2.8.1    | https://github.com/apache/kafka                       | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Zookeeper                  | 3.5.8    | https://github.com/apache/zookeeper                   | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| RabbitMQ                   | 3.8.9    | https://github.com/rabbitmq/rabbitmq-server           | [Mozilla Public License](https://www.mozilla.org/en-US/MPL/)      |
| Docker CE                  | 20.10.8  | https://docs.docker.com/engine/release-notes/         | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| KeyCloak                   | 19.0.2   | https://github.com/keycloak/keycloak                  | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat                   | 7.12.1    | https://github.com/elastic/beats                      | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Filebeat Helm Chart        | 7.12.1    | https://github.com/elastic/helm-charts                | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Prometheus                 | 2.31.1   | https://github.com/prometheus/prometheus              | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Grafana                    | 8.3.2    | https://github.com/grafana/grafana                    | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Node Exporter              | 1.3.1    | https://github.com/prometheus/node_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Bitnami Node Exporter Helm Chart      | 1.1.2    | https://github.com/bitnami/charts          | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Kafka Exporter             | 1.4.0    | https://github.com/danielqsj/kafka_exporter           | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| JMX Exporter               | 0.16.1   | https://github.com/prometheus/jmx_exporter            | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Postgres Exporter          | 0.10.0    | https://github.com/prometheus-community/postgres_exporter | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| PostgreSQL                 | 13       | https://www.postgresql.org/                           | [PostgreSQL license](http://www.postgresql.org/about/licence/)    |
| HAProxy                    | 2.2.2    | https://www.haproxy.org/                              | [GNU General Public License 2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| PgAudit                    | 1.5.0    | https://github.com/pgaudit/pgaudit                    | [PostgreSQL license](http://www.postgresql.org/about/licence/)    |
| repmgr                     | 5.2.1    | https://github.com/EnterpriseDB/repmgr                | [GNU General Public License 3.0](https://github.com/EnterpriseDB/repmgr/blob/master/LICENSE) |
| Pgpool                     | 4.2.4    | https://www.pgpool.net/                               | [License](https://www.pgpool.net/mediawiki/index.php/pgpool-II_License) |
| Alertmanager               | 0.23.0   | https://github.com/prometheus/alertmanager            | [Apache License 2.0](https://github.com/prometheus/alertmanager/blob/master/LICENSE) |
| Apache2                    | 2.4.29   | https://httpd.apache.org/                             | [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Rook                    | 1.8.8   | https://rook.io/                             | [Apache License 2.0](https://github.com/rook/rook/blob/master/LICENSE) |
| OpenSearch                 | 1.2.4   | https://opensearch.org/                                | [Apache License 2.0](https://github.com/opensearch-project/OpenSearch/blob/main/LICENSE.txt) |
| OpenSearch Dashboards      | 1.2.0   | https://opensearch.org/                                | [Apache License 2.0](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/LICENSE.txt) |

## Epicli binary dependencies

| Component                 | Version | Repo/Website                                          | License                                                           |
| ------------------------- | ------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| Terraform                 | 1.1.3   | https://www.terraform.io/                             | [Mozilla Public License 2.0](https://github.com/hashicorp/terraform/blob/master/LICENSE) |
| Terraform AzureRM provider | 2.91.0  | https://github.com/terraform-providers/terraform-provider-azurerm | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/LICENSE) |
| Terraform AWS provider     | 3.71.0  | https://github.com/terraform-providers/terraform-provider-aws | [Mozilla Public License 2.0](https://github.com/terraform-providers/terraform-provider-aws/blob/master/LICENSE) |
| Crane                      | 0.11.0  | https://github.com/google/go-containerregistry/tree/main/cmd/crane     | [Apache License 2.0](https://github.com/google/go-containerregistry/blob/main/LICENSE) |
| Git                        | latest | https://github.com/git/git | [GNU GENERAL PUBLIC LICENSE Version 2](https://github.com/git/git/blob/master/COPYING) |
| aws-cli                    | 2.0.30  | https://github.com/aws/aws-cli | [Apache License 2.0](https://github.com/aws/aws-cli/blob/develop/LICENSE.txt) |

## Epicli Python dependencies

| Component | Version | Repo/Website | License |
| --------- | ------- | ------------ | ------- |
| adal | 1.2.7 | https://github.com/AzureAD/azure-activedirectory-library-for-python | MIT |
| ansible-core | 2.16.2 | https://ansible.com/ | GPLv3+ |
| ansible | 9.1.0 | https://ansible.com/ | GPL-3.0-or-later |
| antlr4-python3-runtime | 4.13.1 | http://www.antlr.org | BSD |
| anyio | 4.2.0 | https://github.com/agronholm/anyio | MIT |
| applicationinsights | 0.11.10 | https://github.com/Microsoft/ApplicationInsights-Python | MIT |
| argcomplete | 3.1.6 | https://github.com/kislyuk/argcomplete | Apache Software License |
| attrs | 23.1.0 | https://www.attrs.org/ | MIT |
| azure-appconfiguration | 1.1.1 | https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/appconfiguration/azure-appconfiguration | MIT License |
| azure-batch | 14.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-cli-core | 2.55.0 | https://github.com/Azure/azure-cli | MIT |
| azure-cli-telemetry | 1.1.0 | https://github.com/Azure/azure-cli | MIT |
| azure-cli | 2.55.0 | https://github.com/Azure/azure-cli | MIT |
| azure-common | 1.1.28 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-core | 1.29.6 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-core | MIT License |
| azure-cosmos | 3.2.0 | https://github.com/Azure/azure-documentdb-python | MIT |
| azure-data-tables | 12.4.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/table/azure-table | MIT License |
| azure-datalake-store | 0.0.53 | https://github.com/Azure/azure-data-lake-store-python | MIT License |
| azure-graphrbac | 0.60.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-keyvault-administration | 4.4.0b2 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-administration | MIT License |
| azure-keyvault-certificates | 4.7.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-certificates | MIT License |
| azure-keyvault-keys | 4.9.0b3 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-keys | MIT License |
| azure-keyvault-secrets | 4.7.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/keyvault/azure-keyvault-secrets | MIT License |
| azure-loganalytics | 0.1.1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-advisor | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-apimanagement | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-appconfiguration | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-appcontainers | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-applicationinsights | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-authorization | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-batch | 17.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-batchai | 7.0.0b1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-billing | 6.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-botservice | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-cdn | 12.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-cognitiveservices | 13.5.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-compute | 30.3.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-containerinstance | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-containerregistry | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-containerservice | 28.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-core | 1.4.0 | https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/core/azure-mgmt-core | MIT License |
| azure-mgmt-cosmosdb | 9.3.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-databoxedge | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-datalake-nspkg | 3.0.1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-datalake-store | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-datamigration | 10.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-devtestlabs | 4.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-dns | 8.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-eventgrid | 10.2.0b2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-eventhub | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-extendedlocation | 1.0.0b2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-hdinsight | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-imagebuilder | 1.2.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-iotcentral | 10.0.0b2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-iothub | 3.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-iothubprovisioningservices | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-keyvault | 10.3.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-kusto | 0.3.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-loganalytics | 13.0.0b4 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-managedservices | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-managementgroups | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-maps | 2.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-marketplaceordering | 1.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-media | 9.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-monitor | 5.0.1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-msi | 7.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-netapp | 10.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-policyinsights | 1.1.0b4 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-privatedns | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-rdbms | 10.2.0b13 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-recoveryservices | 2.5.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-recoveryservicesbackup | 7.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-redhatopenshift | 1.4.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-redis | 14.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-resource | 23.1.0b2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-search | 9.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-security | 5.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-servicebus | 8.2.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-servicefabric | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-servicefabricmanagedclusters | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-servicelinker | 1.2.0b1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-signalr | 2.0.0b1 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-sql | 4.0.0b13 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-sqlvirtualmachine | 1.0.0b5 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-storage | 21.1.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-synapse | 2.1.0b5 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-trafficmanager | 1.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-mgmt-web | 7.0.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-multiapi-storage | 1.2.0 | https://github.com/Azure/azure-multiapi-storage-python | MIT |
| azure-nspkg | 3.0.2 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-storage-common | 1.4.2 | https://github.com/Azure/azure-storage-python | MIT License |
| azure-synapse-accesscontrol | 0.5.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-synapse-artifacts | 0.17.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-synapse-managedprivateendpoints | 0.4.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| azure-synapse-spark | 0.2.0 | https://github.com/Azure/azure-sdk-for-python | MIT License |
| bcrypt | 4.1.2 | https://github.com/pyca/bcrypt/ | Apache-2.0 |
| boto3 | 1.34.5 | https://github.com/boto/boto3 | Apache License 2.0 |
| botocore | 1.34.5 | https://github.com/boto/botocore | Apache License 2.0 |
| certifi | 2023.11.17 | https://github.com/certifi/python-certifi | MPL-2.0 |
| cffi | 1.16.0 | http://cffi.readthedocs.org | MIT |
| chardet | 3.0.4 | https://github.com/chardet/chardet | LGPL |
| charset-normalizer | 3.3.2 | https://github.com/Ousret/charset_normalizer | MIT |
| click | 8.1.7 | https://palletsprojects.com/p/click/ | BSD-3-Clause |
| colorama | 0.4.6 | https://github.com/tartley/colorama | BSD 3-Clause "New" or "Revised" License |
| cryptography | 41.0.7 | https://github.com/pyca/cryptography | Apache-2.0 OR BSD-3-Clause |
| Deprecated | 1.2.14 | https://github.com/tantale/deprecated | MIT |
| Antergos Linux | 2015.10 (ISO-Rolling) | https://github.com/python-distro/distro | Apache License, Version 2.0 |
| exceptiongroup | 1.2.0 | https://github.com/agronholm/exceptiongroup | MIT |
| fabric | 2.7.1 | https://fabfile.org | BSD |
| humanfriendly | 10.0 | https://humanfriendly.readthedocs.io | MIT |
| idna | 3.6 | https://github.com/kjd/idna | BSD 3-Clause "New" or "Revised" License |
| invoke | 1.7.3 | https://pyinvoke.org | BSD |
| isodate | 0.6.1 | https://github.com/gweis/isodate/ | BSD |
| javaproperties | 0.5.2 | https://github.com/jwodder/javaproperties | MIT |
| Jinja2 | 3.1.2 | https://palletsprojects.com/p/jinja/ | BSD-3-Clause |
| jmespath | 1.0.1 | https://github.com/jmespath/jmespath.py | MIT |
| jsondiff | 2.0.0 | https://github.com/ZoomerAnalytics/jsondiff | MIT |
| jsonschema-specifications | 2023.11.2 | https://json-schema.org/ | MIT |
| jsonschema | 4.20.0 | https://json-schema.org/ | MIT |
| knack | 0.11.0 | https://github.com/microsoft/knack | MIT |
| MarkupSafe | 2.1.3 | https://palletsprojects.com/p/markupsafe/ | BSD-3-Clause |
| msal-extensions | 1.0.0 | https://github.com/AzureAD/microsoft-authentication-extensions-for-python | MIT |
| msal | 1.24.0b2 | https://github.com/AzureAD/microsoft-authentication-library-for-python | MIT |
| msrest | 0.7.1 | https://github.com/Azure/msrest-for-python | MIT License |
| msrestazure | 0.6.4 | https://github.com/Azure/msrestazure-for-python | MIT License |
| oauthlib | 3.2.2 | https://github.com/oauthlib/oauthlib | BSD |
| packaging | 23.2 | https://github.com/pypa/packaging | [Other](https://api.github.com/repos/pypa/packaging/license) |
| paramiko | 3.4.0 | https://paramiko.org | LGPL |
| pathlib2 | 2.3.7.post1 | https://github.com/jazzband/pathlib2 | MIT |
| pkginfo | 1.9.6 | https://code.launchpad.net/~tseaver/pkginfo/trunk | MIT |
| portalocker | 2.8.2 | https://github.com/WoLpH/portalocker  | BSD-3-Clause |
| psutil | 5.9.7 | https://github.com/giampaolo/psutil | BSD-3-Clause |
| pycomposefile | 0.0.30 | https://github.com/smurawski/pycomposefile | MIT |
| pycparser | 2.21 | https://github.com/eliben/pycparser | BSD |
| PyGithub | 1.59.1 | https://github.com/pygithub/pygithub | GNU Lesser General Public License v3.0 |
| Pygments | 2.17.2 | https://pygments.org/ | BSD-2-Clause |
| PyJWT | 2.8.0 | https://github.com/jpadilla/pyjwt | MIT |
| PyNaCl | 1.5.0 | https://github.com/pyca/pynacl/ | Apache License 2.0 |
| pyOpenSSL | 23.3.0 | https://pyopenssl.org/ | Apache License, Version 2.0 |
| PySocks | 1.7.1 | https://github.com/Anorov/PySocks | BSD |
| python-dateutil | 2.8.2 | https://github.com/dateutil/dateutil | Dual License |
| python-json-logger | 2.0.7 | http://github.com/madzak/python-json-logger | BSD |
| PyYAML | 6.0.1 | https://pyyaml.org/ | MIT |
| referencing | 0.32.0 | https://json-schema.org/ | MIT |
| requests-oauthlib | 1.3.1 | https://github.com/requests/requests-oauthlib | ISC |
| requests | 2.31.0 | https://requests.readthedocs.io | Apache 2.0 |
| resolvelib | 1.0.1 | https://github.com/sarugaku/resolvelib | ISC License |
| rpds-py | 0.15.2 | https://github.com/crate-py/rpds | MIT |
| ruamel.yaml.clib | 0.2.8 | https://sourceforge.net/p/ruamel-yaml-clib/code/ci/default/tree | MIT |
| ruamel.yaml | 0.17.40 | https://sourceforge.net/p/ruamel-yaml/code/ci/default/tree | MIT license |
| s3transfer | 0.9.0 | https://github.com/boto/s3transfer | Apache License 2.0 |
| scp | 0.13.6 | https://github.com/jbardin/scp.py | LGPL-2.1-or-later |
| semver | 2.13.0 | https://github.com/python-semver/python-semver | BSD |
| six | 1.16.0 | https://github.com/benjaminp/six | MIT |
| sniffio | 1.3.0 | https://github.com/python-trio/sniffio | MIT OR Apache-2.0 |
| sshtunnel | 0.1.5 | https://github.com/pahaz/sshtunnel | MIT |
| tabulate | 0.9.0 | https://github.com/astanin/python-tabulate | MIT |
| typing_extensions | 4.9.0 | https://github.com/python/typing_extensions | [Other](https://github.com/python/typing_extensions/blob/main/LICENSE) |
| urllib3 | 2.0.7 | https://urllib3.readthedocs.io/ | MIT |
| websocket-client | 1.3.3 | https://github.com/websocket-client/websocket-client.git | Apache-2.0 |
| wrapt | 1.16.0 | https://github.com/GrahamDumpleton/wrapt | BSD |
| xmltodict | 0.13.0 | https://github.com/martinblech/xmltodict | MIT |

## Predefined Grafana dashboards

| Dashboard name | Dashboard ID | Repo/Website | License |
| --------- | ------- | ------------ | ------- |
| Kubernetes Cluster | 7249 | https://grafana.com/grafana/dashboards/7249 | None |
| Kubernetes cluster monitoring (via Prometheus) | 315 | https://grafana.com/grafana/dashboards/315 | [MIT License](https://github.com/instrumentisto/grafana-dashboard-kubernetes-prometheus/blob/master/LICENSE.md) |
| Node Exporter Dashboard EN 20201010-StarsL.cn | 11074 | https://grafana.com/grafana/dashboards/11074 | [Apache License 2.0](https://github.com/starsliao/Prometheus/blob/master/LICENSE) |
| Node Exporter Server Metrics | 405 | https://grafana.com/grafana/dashboards/405 | None |
| Postgres Overview | 455 | https://grafana.com/grafana/dashboards/455 | None |
| PostgreSQL Database | 9628 | https://grafana.com/grafana/dashboards/9628 | [Apache License 2.0](https://github.com/lstn/misc-grafana-dashboards/blob/master/LICENSE) |
| RabbitMQ Monitoring | 4279 | https://grafana.com/grafana/dashboards/4279 | [MIT License](https://github.com/kbudde/rabbitmq_exporter/blob/main/LICENSE) |
| Node Exporter Full | 1860 | https://grafana.com/grafana/dashboards/1860 | [LGPL-3.0 License](https://github.com/rfrail3/grafana-dashboards/blob/master/LICENSE) |
| Kafka Exporter Overview | 7589 | https://grafana.com/grafana/dashboards/7589 | [Apache License 2.0](https://github.com/danielqsj/kafka_exporter/blob/master/LICENSE) |
| HaProxy backend (or frontend/servers) | 789 | https://grafana.com/grafana/dashboards/367 | None, [Source Code](https://github.com/tcheronneau/grafana_dashboard) | |
| Docker and Host Monitoring w/ Prometheus | 179 | https://grafana.com/grafana/dashboards/179 | [MIT License](https://github.com/vegasbrianc/prometheus/blob/master/LICENSE) |
| Kubernetes pod and cluster monitoring (via Prometheus) | 6663 | https://grafana.com/grafana/dashboards/6663 | None |
| RabbitMQ cluster monitoring (via Prometheus) | 10991 | https://grafana.com/grafana/dashboards/10991 | [License](https://github.com/rabbitmq/rabbitmq-server/blob/master/LICENSE), [Source Code](https://github.com/rabbitmq/rabbitmq-server/blob/master/deps/rabbitmq_prometheus/docker/grafana/dashboards/RabbitMQ-Overview.json) |
