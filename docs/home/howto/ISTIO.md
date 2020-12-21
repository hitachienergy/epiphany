## Istio

Open source platform which allow us run service mesh for distributed microservice architecture. It allows to connect, manage and run secure connections between microservices and bring us a lot of features such as load balancing, monitoring, service-to-service authentication without any changes in service code. Read more about Istio [here](https://istio.io/latest/docs/concepts/what-is-istio/).

### Installing Istio

Istio in Epiphany is provided as K8s application. By default it is not installed. To deploy it you need to add "configuration/applications" document to your configuration yaml file, similar to the example below (`enabled` flags must be set as `true`):

Istio will be installed using Istio Operator. Operator is software extensions to kubernetes which have a deep knowledge how to Istio deployments should looks like and how to react if any problem appears. It is also very easy to make any upgrade and automate a tasks which user/admin normally should execute.

```yaml
---
kind: configuration/applications
version: 0.8.0
title: "Kubernetes Applications Config"
provider: aws
name: default
specification:
  applications:
  ...

## --- istio ---

  - name: istio
    enabled: yes
    use_local_image_registry: true
    namespaces:
      operator: istio-operator # namespace where operator will be deployed
      watched: # list of namespaces which operator will watch
        - istio-system
      istio: istio-system # namespace where istio control plane will be deployed
    istio_spec:
      profile: default # Check all possibilites https://istio.io/latest/docs/setup/additional-setup/config-profiles/
      name: istiocontrolplane

```

Using this configuration file, controller will detect Istio Operator resource in first of watched namespaces and will install Istio components corresponding to the specified profile (default). Using the default profile, istio control plane and istio ingress gateway will be deployed in istio-system namespace.

### How to set up service mesh for an application

The default istio installation use automcatic sidecar injection. You need to label the namespace where application will be hosted: `kubectl label namespace default istio-injection=enabled`

If the proper namespaces is already labeled and istio is deployed, You can deploy Your applicayion or restart deployment if exists.

You may need to make the application accessible from outside of your Kubernetes cluster. An Istio Gateway which was deployed using default profile is used for this purpose. Define the the ingress gateway deploying gateway and virtual service specification. The gateway specification describes the L4-L6 properties of a load balancer and the virtual service specification describe the L7 properties of a load balancer.

Example of the gateway and virtual service specification (You have to adapt the entire specification to the application):

[Gateway](https://istio.io/latest/docs/reference/config/networking/gateway/):

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: httpbin-gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "httpbin.example.com"
```

[Virtual Service](https://istio.io/latest/docs/reference/config/networking/virtual-service/):

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: httpbin
spec:
  hosts:
  - "httpbin.example.com"
  gateways:
  - httpbin-gateway
  http:
  - match:
    - uri:
        prefix: /status
    - uri:
        prefix: /delay
    route:
    - destination:
        port:
          number: 8000
        host: httpbin
```
