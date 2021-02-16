# KAFKA MONITORING TOOLS - RESEARCH RESULTS

## 1. CONFLUENT CONTROL CENTER [link](https://docs.confluent.io/)

- Commercial feature, only trial version for free
- Out of the box UI
- Managing and monitoring Kafka cluster (including view consumer offset)
- Possibility to set up alerts
- Detailed documentation, lots of tutorials, blog articles and a wide community
- All-in-one solution with additional features through Confluent Platform/Cloud

## 2. LENSES [link](https://github.com/kubicorn/kubicorn)

- Commercial feature, only trial version for free
- Out of the box UI
- Deliver monitoring of Kafka data pipelines
- Managing and monitoring Kafka cluster (including view consumer offset)
- Possibility to set up alerts
- Smaller community, fewer articles and tutorials around Lenses compared to the Control Center

## 3. SEMATEXT  [link](https://sematext.com/)

- Commercial feature, only trial version for free
- ChatOps integrations
- Out of the box UI
- Built-in anomaly detection, threshold, and heartbeat alerts
- Managing and monitoring Kafka cluster (including view consumer offset)
- Possibility to set up alerts

## 4. DATADOG KAFKA [link](https://www.datadoghq.com)

- Commercial feature, only trial version for free
- Out of the box Kafka monitoring dashboards
- Monitoring tool (including view consumer offset). Displays key metrics for Kafka brokers, producers, consumers and Apache Zookeeper. Less focused on cluster state
- Possibility to set up alerts

## 5. CLOUDERA MANAGER  [link](https://www.cloudera.com/)

- Commercial feature, only trial version for free
- Less rich monitoring tool compared to Confluent, Lenses and Datadog but is very convenient for companies that are already customers of Cloudera and need their monitoring mechanisms under the same platform

## 6. KAFKA TOOL  [link](https://www.kafkatool.com/)

- Commercial feature, only trial version for free
- Out of the box UI
- Monitoring tool (including view consumer offset)
- Poor documentation
- In latest changelogs, only support for kafka 2.1 mentioned
- Some of opensource projects looks much more better that this one

## 7. KADECK  [link](https://www.xeotek.com/)

- Commercial feature, only trial version for free
- Out of the box UI
- Focused on filtering the messages within the topics and the creation of custom views
- No possibility to set up alerts
- Focuses more on business monitoring than on technical monitoring like Control Center or Lenses
- KaDeck could be used in addition to the other monitoring tools

## 8. YAHOO CLUSTER MANAGER [link](https://github.com/yahoo/CMAK)

- Opensource project, Apache-2.0 License
- Managing and monitoring Kafka cluster (including view consumer offset)
- Out of the box UI
- No possibility to set up alerts

## 9. LINKEDIN CRUISE CONTROL [link](https://github.com/linkedin/cruise-control)

- Opensource project, BSD 2-Clause "Simplified" License
- Managing and monitoring Kafka cluster (not possible to view consumer offset :warning:)
- Possible to track resource utilization for brokers, topics, and partitions, query cluster state, to view the status of partitions, to monitor server capacity (i.e. CPU, network IO, etc.)
- Anomaly Detection and self-healing and rebalancing
- Possibility to set up alerts
- UI as seperated component [link](https://github.com/linkedin/cruise-control-ui)
- It can use metrics reporter from LinkedIn (necessary to add jar file to kafka lib directory) but it is also possible to uses Prometheus for metric aggregation

## 10. LINKEDIN BURROW [link](https://github.com/linkedin/Burrow)

- Opensource project, Apache-2.0 License
- Provides consumer lag checking as a service without the need for specifying thresholds. It monitors committed offsets for all consumers and calculates the status of those consumers on demand
- It does not monitor anything related to the health of the brokers

## 11. KAFKA DROP 3 [link](https://github.com/obsidiandynamics/kafdrop)

- Opensource project, Apache-2.0 License, reboot of Kafdrop 2.x
- Monitoring tool (including view consumer offset)
- Out of the box UI

## 12. KAFKA MONITOR [link](https://github.com/linkedin/kafka-monitor)

- Opensource project, Apache-2.0 License
- Kafka monitor is a framework to implement and execute long-running kafka system tests in a real cluster
- It plays a role as a passive observer and reports what it observes (broker availability, produce/consume latency, etc) by emitting metrics. In other words, it pretends to be a Kafka user and keeps reporting metrics from the user's PoV
- It is more a load generation and reporting tool
- UI does not exist

## 13. OTHERS

Things like on the list below are there as well, but usually such smaller projects and have little or no development activity:

- [doctorK](https://github.com/pinterest/DoctorK)
- [kafdrop](https://github.com/obsidiandynamics/kafdrop)
- [kafka-offset-monitor](https://github.com/Morningstar/kafka-offset-monitor)

## 14. CONCLUSIONS

Currently in Epiphany monitoring and getting metrics from Kafka are based one:
- Kafka Exporter [link](https://github.com/danielqsj/kafka_exporter)
- JMX Exporter [link](https://github.com/prometheus/jmx_exporter)
- Prometheus [link](https://prometheus.io/)
- Grafana [link](https://grafana.com/)

In real scenarios, based on some use cases and opinions from internal teams:
- Kafka Exporter is used in order to get consumer offset and lag
- JMX Exporter is used in order to get some standard broker's metrics such as cpu, memory utilization and so on
- Problems with the administration of the leader election are reported

If it is possible to pay for a commercial license. Confluent, Lenses and Sematext offer more rich functionality compared to the other monitoring tools and they are really similar.

As far as the open source project is considered:
- LinkedIn Cruise Control looks like the winner. Provides not only managing and monitoring kafka cluster but also some extra features such as rebalancing, anomaly detection or self-healing
- Yahoo cluster manager looks like good competitor but only for managing and monitoring kafka cluster. However in compare to Cruise Control, during the installation I met some issues and I was not able to recieve some consumer data and a few issues are already reported in official repository related to my problem [link](https://github.com/yahoo/CMAK/issues/641). I would not recommend this tools since it looks like the project does not have good spirit of open source software
- LinkedIn Burrow looks like good additional tool for LinkedIn Cruise Control if we would like to have consumer lag checking service instead of kafka exporter plugin which cause some outstanding issues
