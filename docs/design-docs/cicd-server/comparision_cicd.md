# Comparision of CI/CD tools


## Research of available solutions

After some research I found below tools. I group them by categories in columns:


|name    |paid	|open source|	self hosted|	cloud hosted|
|---------|---------|---------|---------|---------|
|jenkin-x	|0	|1	|1	|0|
|tekton | 0 | 1| 1| 0|
|jenkins | 0| 1| 1| 0|
|gitlabCI	|0	|1	|1	|0	|
|goCD	|0	|1	|1	|0	|
|bazel	|0	|1	|1	|0	|
|argoCD| 0| 1| 1| 0|
|spinnaker	|0	|1	|1	|0	|
|buildBot	|0	|1	|1	|0	|
|Travis	|0	|0	|0	|1	|
|buddy	|1	|0	|1	|1	|
|circleCI	|1	|0	|1	|1	|
|TeamCity	|1	|0	|1	|1	|
|CodeShip	|1	|0	|0	|1	|
|azureDevOps	|1	|0	|0	|1	|
|Bamboo	|1	|0	|1	|0	|

First for recognition goes only open source and free (at least in our usage model) tools.

## Closer look on choosen tools

|name    |paid	|open source|	self hosted|	cloud hosted|comment|
|---------|---------|---------|---------|---------|---------|
|jenkins-x	|0	|1	|1	|0|	|
|tekton | 0 | 1| 1| 0|
|jenkins | 0| 1| 1| 0|
|gitlabCi	|0	|1	|1	|0	|requires use GitLab|
|goCD	|0	|1	|1	|0	||
|argoCD| 0| 1| 1| 0| CD tool requie other CI tool
|bazel	|0	|1	|1	|0	|this is build engine not a build server|
|spinnaker	|0	|1	|1	|0	|mostly used for CD purposes|
|buildBot	|0	|1	|1	|0	|looks worse then previous tools |
|Travis	|0/1	|0	|0	|1	|In our usage model we will have to pay|

After closer look I consider this tools:
* `goCD`
* `jenkins-x`
* `tekton`
* `jenkins`
* `argoCD` - this is CD tools so it's not compared in table below
* `spinnaker` - wasn't tested because it is CD tools and we need also CI tool

## Comparision

### Run server on kubernetes

__gocd__: easily installed by helm chart, requires to be accesible from outside cluster if we want to access UI. Can be run on Linux systems also

__jenkins__: can be easily started on any cluster

__jenkins-x__: hard to set up on running cluster. I created new kubernetes cluster by their tool which generally is ok - but in my vision it will be good to use it on epiphany cluster (eat your own dog food vs drink your own champane). Many (probably all) services works based on DNS names so also I have to use public domain (use mine personal)

__tekton__: easily started on epiphany cluster.

### Accesses
__gocd__: , OAuth, LDAP or internal database

__jenkins__: OIDC, LDAP, internal, etc.

__jenkins-x__: `Jenkins X uses Role-Based Access Control (RBAC) policies to control access to its various resources`

__tekton__: For building purposes there is small service which webhooks can connect and there predined pipeline is starting. For browsing purposes dashboard has no restrictions - it's open for everybody - this could be restricted by HAProxy or nginx. Only things you can do in dashbord is re-run pipeline or remove historical builds. Nothing more can be done.

### Pipeline as a Code
__gocd__: possible and looks ok, pipeline code can be in different repository

__jenkins__: possible and looks ok

__jenkins-x__: possible looks ok (Tekton)

__tekton__: pipelines are CRD so can be only as a code

### Build in pods

__gocd__: Elastic agent concepts. Can create many groups (probably on different clusters - not tested yet) and assigned them to proper pipelines

__jenkins__: plugin for building in kubernetes

__jenkins-x__: building in pods in cluster jenkins-x is installed. Possible to install many jenkins-x servers (according to documentation per each team in different namespace). Able to run in multi cluster mode

__tekton__: building in cluster easily. Not possible to build on different server - but I didn't any sence in that use case. Possible to deploy on other kubernetes service.

### Secrets
__gocd__: Plugins for secrets from: hashicorp vault, kubernetes secrets, file based

__jenkins__: plugins for many options: hashicorp vault, kubernetes secrets, internal secrets, etc

__jenkins-x__: Providers for secrets from: hashicorp vault, kubernetes secrets

__tekton__: Use secrets from kubernetes so everything what is inside kubernetes can be read

### Environment varaibles:

__gocd__: multiple level of variables: environment, pipeline, stage, job

__jenkins__: environment variables can be overriden

__jenkins-x__: Didn't find any information but expect it will not be worst than in gocd

__tekton__: You can read env variables from any config map so this is kind of overriding.

### Plugins

__gocd__: not big number of plugins (but is this really bad?) but very of them really usefull (LDAP, running in pods, vault, k8s secrets, docker registry, push to S3, slack notification, etc)

__jenkins__: many plugins. But if there is too much of them they start making serious issues. Each plugin has different quality and each can breake the server and has its own security issues so we have to be very careful with them.

__jenkins-x__: plugins are called app. There are few of them and this app are helm charts.
Jenkins-x uses embeded nexus, chartmuseum and monocular services. I don't know if the is option to get rid of them.

__tekton__: tekton itself is kind of plugin for building. You can create whatever you want in different pod and get it.

## Personal conclusion
__gocd__:
* This looks like really good CI/CD central server which can be use by many teams.
* Really mature application. Older release on github from Nov 2014. According to wiki first release in 2007.
* very intuitive
* Working really good in kubernetes
* Good granuality of permission.
* Good documentation
* Small amount of help in Internet (compare to jenkins)
* Small community

GoCD can be easily set up for our organizations. Adding new customers should not be big deal. Working with is very intuitive - old school concept of CICD.

__jenkins__:
* Production ready
* The most search CI/CD tool in google - so almost every case is describe somwhere
* Very simple
* Working very good in kubernetes
* After using it for some time pipelines are getting bigger and harder to maintain
* Good granuality of permission
* XML configuration for many plugins
* Big amount of information in Internet
* Big community

The most popular CI/CD tool. Small and simple. You can do everything as a code or by GUI - which is not good because it's temptation to fix it right now and then probably do not put it to repository. A lot of plugins which and each of them is single point of failure. Hard to configure some plugin as a code - but still possible.

__jenkins-x__:
* There is new sheriff in town - new way of maintainig CICD server
* New application still under heavy development (don't know what exactly but number of commits is really big)
* New concept of CICD, a lot of magic doing under the hood, GitOps and ChatOps
* Designed to work inside oif kubernetes
* Still don't know how to manage permissions
* Big community (CDFoundation is under Linux Foundation)

Jenkins-x is definetly new sheriff in town. But to enable it in big existing organization with new way of CICD process requires changing the way of thinking about all process. So it's really hot topic, but is it ok for us to pay that price.

__tekton__:
* New concept of CI - serverless.
* Tekton is young (first release 20 Feb 2019).
* Is a part of jenkins-x so it's simpler when you starting playing with it and still you can configure everything as in jenkins-x by yourself.
* Easy to install in epiphany cluster - kubernetes CRD
* Easy to install triggers which allow to build when request is comming.
* It should be separate namespace for every team. Builds will be running in one cluster using the same hosts.
* No permission to dashboard. It has to be resolve by properly configure HAProxy or nginx in front of dashboard. Dashboard is running as kubernetes service.
* Big community.
* Smal but good enough help regarding tekton itself. Under the hood it's kubernetes so you can configure it as you want.


Comparing it previous solutions jenkins-x is using tekton. So it has less features then jenkins-x - and thanks to that is simpler -  but by deafult I was not able to configure really usefull feature building on push. There is such possibility by running tekton triggers which is realy simple.
This project is under CDFoundation and has a big community which is really good.
My personal choice.

## Another concept CI and CD tool

Use separate tools for Continious Integration and Continious Deployment. In this concept I recognized [Tekton](tekton.dev) for building and [ArgoCD](https://argoproj.github.io/argo-cd/) for delivery purposes.

### ArgoCD

In ArgoCD you can easily deploy one of your applications described as kubernetes resources into one of your kubernetes clusters.
In that case recommended option is to have two repos one for code and one for configuration. Thanks to that you can easily separate code from configuration. It also works with one repo where you keep code and configuration in one repo.

When Argo detect changes in configuration it runs new configuration on cluster. It's simple like that.

#### User management

Possible to use: local users, SSO with Bundled Dex OIDC provider, SSO with Existing OIDC provider

#### Secrets
* Bitnami Sealed Secrets
* Godaddy Kubernetes External Secrets
* Hashicorp Vault
* Banzai Cloud Bank-Vaults
* Helm Secrets
* Kustomize secret generator plugins
* aws-secret-operator
* KSOPS

#### Conclusion
ArgoCD looks very good if you have a really big number of clusters you are managing. Thanks to that you can deploy whatever you want wherever you need. But this is needed for really for big scale.
