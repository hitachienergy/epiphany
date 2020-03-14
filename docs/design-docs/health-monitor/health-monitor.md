# Epiphany Health Monitor service design proposal

Affected version: 0.6.x/0.7.x

## Goals

Provide service that will be monitoring components (Kubernetes, Docker, Kafka, EFK, Prometheus, etc.) deployed using Epiphany.

## Use cases

Service will be installed and used on Virtual Machines/Bare Metal on Ubuntu and RedHat (systemd service).
Health Monitor will check status of components that were installed on the cluster. Combinations of those components can be different and will be provided to the service through configuration file.

Components that Health Monitor should check:
- Kubernetes (kubelet)*
- Query Kubernetes health endpoint (/healthz)*
- Docker*
- Query Docker stats*
- PostgreSQL
- HAProxy
- Prometheus
- Kafka
- ZooKeeper
- ElasticSearch
- RabbitMQ

`*` means MVP version.

Health Monitor exposes endpoint that is compliant with [Prometheus metrics format](https://github.com/prometheus/docs/blob/master/content/docs/instrumenting/exposition_formats.md#text-format-example) and serves data about health checks. This endpoint should listen on the configurable port (default 98XX).

## Design proposal

The proposal includes creating an application that can be run as systemd on the installed vms and bare metals .  This application will read a yml configuration file and based on the given input it will send data on an http or tcp connection using prometheus metric format. This application will run on given port and will have an endpoint attached to it. upon calling it should provide all available metrics over that has been defined in the configuration file.

![diagram][./diagram.jpg]

To collect metrics for the docker system , the application will look for the following input in the config.yml file
 `-name:docker
   metrics :['cpu','memory']
   interval : 30s
  `

  this config will tell the system on what process to look which is signified by name, metrics denotes what metrics we need to collect using docker stats, interval defines how often. since docker stats return statistics for all containers, while sending the data we will use container names as label followed by metrics to send the data.


  For kubernetes we would need to examine kubernetes cluster and that can be achieved by calling 'kubectl top' command. we would create a similar configuration as docker for this one also 
  `-name:kubectl
   metrics :['cpu','memory']
   pods :["pod1","pod2"]
   services :["service1","service2"]
   interval : 30s
  `
  since kubectl top collect metrics using metrics-server[https://github.com/kubernetes-incubator/metrics-server] , we can use this to retrieve metrics from specific pods and services running on the cluster and send it over given endpoint.

  Kubernetes provides certain health checks or probes to check the liveness and readiness of the running pods, we can create a simple http server that would connect to the services and let us know about the liveliness of the current running application.This application will be added to the image of the running applications. 

  ### Postgres
  for postgres we will need configuration parameters like
    `-name:postgres
    endpoint:"/healthz"
    interval : 30s
    `

 using this configuration the server calls the metrics endpoint of the postgres and returns the result. 

 ### HAProxy
for haproxy we will need configuration parameters like
    `-name:haproxy
    endpoint:"/status"
    interval : 30s
    `
the application will connect to the ha proxy pod and will return the status based on the given endpoint


TODO