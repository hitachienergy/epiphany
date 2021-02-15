# KAFKA MONITORING TOOLS - RESEARCH RESULTS

## 1. CONFLUENT CONTROL CENTER [link](https://docs.confluent.io/)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 2. LENSES [link](https://github.com/kubicorn/kubicorn)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 3. DATADOG KAFKA [link](https://www.datadoghq.com)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 4. CLOUDERA MANAGER  [link](https://www.cloudera.com/)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 5. KAFKA TOOL  [link](https://www.kafkatool.com/)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 6. SEMATEXT  [link](https://sematext.com/)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 7. KADECK  [link](https://www.xeotek.com/)

- Cannot be used in Epiphany, because it's commercial feature, only trial version for free.

## 8. YAHOO CLUSTER MANAGER [link](https://github.com/yahoo/CMAK)

- Can be used in Epiphany, opensource project, Apache-2.0 License.
- Managing Kafka cluster, cluster state (topics, brokers, offsets, partitions), managing topics. It can show statistics on individual brokers or topics, such as messages per second, lag, and etc. It's more of an administrative tool.

## 9. LINKEDIN CRUISE CONTROL [link](https://github.com/linkedin/cruise-control)

- Can be used in Epiphany, opensource project, BSD 2-Clause "Simplified" License.
- Out of the box it enables you to track resource utilization for brokers, topics, and partitions, query cluster state, to view the status of partitions, to monitor server capacity (i.e. CPU, network IO, etc.), message traffic distribution, add and remove brokers, rebalance your cluster, and so on ( anomaly Detection and self-healing. Cruise Control is used within LinkedIn to manage almost 3000 Kafka brokers, Sepearated UI : https://github.com/linkedin/cruise-control-ui/ . It drastically simplifies partition management.
- Standard of many projects worldwide, the most popular. 
- It can use metrics reporter from LinkedIn (necessary to add jar to kafka lib directory) or Cruise Control is also compatible with any Apache Kafka cluster that uses Prometheus for metric aggregation.

## 10. LINKEDIN BURROW [link](https://github.com/linkedin/Burrow)

- Can be used in Epiphany, opensource project, Apache-2.0 License.
- Provides consumer lag checking as a service without the need for specifying thresholds. It monitors committed offsets for all consumers and calculates the status of those consumers on demand.
- It does not monitor anything related to the health of the brokers.

## 11. KAFKA DROP 3 [link](https://github.com/obsidiandynamics/kafdrop)

- Can be used in Epiphany, opensource project, Apache-2.0 License, reboot of Kafdrop 2.x.
- Kafdrop 3 is a web UI for viewing Kafka topics and browsing consumer groups. The tool displays information such as brokers, topics, partitions, consumers, and lets you view messages.

## 12. KAFKA MONITOR [link](https://github.com/linkedin/kafka-monitor)

- Can be used in Epiphany, opensource project, Apache-2.0 License.
- Kafka monitor is a framework to implement and execute long-running kafka system tests in a real cluster.
- It plays a role as a passive observer and reports what it observes (broker availability, produce/consume latency, etc) by emitting metrics. In other words, it pretends to be a Kafka user and keeps reporting metrics from the user's PoV.
- It is more a load generation and reporting tool.

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
- Kafka Exporter is used in order to get customer lag
- JMX Exporter is used in order to get some standard broker's metrics such as cpu, memory utilization and so on
- Problems with the administration of the leader election are reported

Out of what we have here now:
- LinkedIn Cruise Control looks like the best solution if we would like to add rebalacing and anomaly detection feature. Cruise Control is also very valuabnle tool as far as administration and monitoring is consider but we can not check here lag consumer
- Yahoo cluster manager looks like the best solution for administration and monitoring of kafka cluster including customer lag
- LinkedIn Cruise Control and Yahoo cluster manager can perform administrative task such as preferred leader election
- LinkedIn Burrow looks like the best solution if we would like to only add cunsomer lag checking service instead of kafka exporter plugin which cause some outstanding issues
