# Context

This design document presents findings on what are important pieces of modules communication it Dockerized Custom Modules approach described [here](./modularization-approaches.md). 

# Plan 

Idea is to have something running and working mimicking real world modules. I used GNU make to perform this. With GNU make I was able to easily implement “run” logic. I also wanted to package everything into docker images to experience real world containers limitations of communication, work directory sharing and other stuff. 

# Dependencies problem

First definition of modules [here](https://github.com/mkyc/epiphany-wrapper-poc-repo/blob/master/v1.yaml) in example presented here: 

```
version: v1
kind: Repository
components:
- name: c1
  type: docker
  versions:
  - version: 0.1.0
    latest: true
    image: "docker.io/hashicorp/terraform:0.12.28"
    workdir: "/terraform"
    mounts: 
    - "/terraform"
    commands:
    - name: init
      description: "initializes terraform in local directory"
      command: init
      envs:
        TF_LOG: WARN
    - name: apply
      description: "applies terraform in local directory"
      command: apply
      envs:
        TF_LOG: DEBUG
      args:
      - -auto-approve
```

... didn't have any dependencies section. We know that some kind of dependencies will be required very soon. I created idea of how to define dependencies between modules in following mind map: 

![mm](./dependencies.png)

It shows following things: 
 * every module has some set of labels. I don't think we need to have any "obligatory" labels. If you create very custom ones you will be very hard to find. 
 * module has `requires` section with possible subsections `strong` and `weak`. A strong requirement is one has to be fulfilled for the module to be applied. A weak requirement, on the other hand, is something we can proceed without, but it is in some way connected when present. 
 
It's worth co notice each `requires` rule. I used [kubernetes matchExpressions](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#resources-that-support-set-based-requirements) approach as main way of defining dependencies, as one of main usage here would be "version >= X", and we cannot use simple labels matching mechanism without being forced to update all modules using my module every time I release a new version of that module.   
 
# Influences

I started to implement example docker based mocked modules in [tests](./cpt-tests) directory, and I found a 3rd section required: `influences`. To explain this lets notice one folded module in upper picture: "BareMetalMonitoring". It is Prometheus based module so, as it works in pull mode, it needs to know about addresses of machines it should monitor. Let's imagine following scenario:
 * I have Prometheus already installed, and it knows about IP1, IP2 and IP3 machines to be monitored,  
 * in next step I install, let's say `BareMetalKafka` module, 
 * so now, I want Prometheus to monitor Kafka machines as well,  
 * so, I need `BareMetalKafka` module to "inform" in some way `BareMetalMonitoring` module to monitor IP4, IP5 and IP6 addresses to addition of what it monitors already. 
 
This example explains "influences" section. Mocked example is following: 

```
labels:
  version: 0.0.1
  name: Bare Metal Kafka
  short: BMK
  kind: stream-processor
  core-technology: apache-kafka
  provides-kafka: 2.5.1
  provides-zookeeper: 3.5.8
requires:
  strong:
    - - key: kind
        operator: eq
        values: [infrastructure]
      - key: provider,
        operator: in,
        values:
          - azure
          - aws
  weak:
    - - key: kind
        operator: eq
        values:
          - logs-storage
    - - key: kind
        operator: eq
        values:
          - monitoring
      - key: core-technology
        operator: eq
        values:
          - prometheus
influences:
  - - key: kind
      operator: eq
      values:
        - monitoring
```

As presented there is `influences` section notifying that "there is something what that I'll do to selected module (if it's present)". I do not feel urge to define it more strictly at this point in time before development. I know that this kind of `influences` section will be required, but I do not know exactly how it will end up.  
