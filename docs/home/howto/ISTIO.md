## Istio

Open source platform which allows you to run service mesh for distributed microservice architecture. It allows to connect, manage and run secure connections between microservices and brings a lot of features such as load balancing, monitoring and service-to-service authentication without any changes in service code. Read more about Istio [here](https://istio.io/latest/docs/concepts/what-is-istio/).

### Installing Istio

Istio in Epiphany is provided as K8s application. By default, it is not installed. To deploy it you need to add "configuration/applications" document to your configuration yaml file, similar to the example below (`enabled` flag must be set as `true`):

Istio is installed using Istio Operator. Operator is a software extension to the Kubernetes API which has a deep knowledge how Istio deployments should look like and how to react if any problem appears. It is also very easy to make upgrades and automate tasks that would normally be executed by user/admin.

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
    enabled: true
    use_local_image_registry: true
    namespaces:
      operator: istio-operator # namespace where operator will be deployed
      watched: # list of namespaces which operator will watch
        - istio-system
      istio: istio-system # namespace where Istio control plane will be deployed
    istio_spec:
      profile: default # Check all possibilites https://istio.io/latest/docs/setup/additional-setup/config-profiles/
      name: istiocontrolplane

```

Using this configuration file, controller will detect Istio Operator resource in first of watched namespaces and will install Istio components corresponding to the specified profile (default). Using the default profile, Istio control plane and Istio ingress gateway will be deployed in istio-system namespace.

### How to set up service mesh for an application

The default Istio installation use automcatic sidecar injection. You need to label the namespace where application will be hosted:

```bash
kubectl label namespace default istio-injection=enabled
```

Once the proper namespaces are labeled and Istio is deployed, you can deploy your applications or restart existing ones.

You may need to make an application accessible from outside of your Kubernetes cluster. An Istio Gateway which was deployed using default profile is used for this purpose. Define the ingress gateway deploying gateway and virtual service specification. The gateway specification describes the L4-L6 properties of a load balancer and the virtual service specification describes the L7 properties of a load balancer.

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
