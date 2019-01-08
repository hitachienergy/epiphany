# Epiphany Physical View

Epiphany Platform is deployed on a number of machines that require communication in order to exchange large amount of data. Components described in [Logical View](logical-view.md) and [Process View](process-view.md) are deployed on different machines.

![Logging process view](diagrams/physical-view/physical-view.svg)

`Node exporter` and `Filebeat` should be present on each machine, because those components are responsible for collecting monitoring and logging data.

Computing section - contains `Kubernetes Master` and `Kubernetes Node` where many `Kubernetes Node` machines (virtual, cloud, bare metal) are possible.

Centralized monitoring section with `Prometheus`, `Grafana` and `Alert Manager` pulls data from exporters installed on all machines. `Grafana` web dashboards are available on the machine running this role. Machine running `Alert Manager` requires access to configured endpoints for alerting - like email server, Slack, PagerDuty.

Centralized logging receives data pushed by `Filebeat` component that is installed on each machine. `Kibana` web interface is available on machine running this role.

Messaging with `Kafka` like `Kubernetes Node` scales horizontally, it means as many machines running this role are possible as needed.

Load Balancing machine running `HAProxy` is an entry point for applications running inside of `Kubernetes`.