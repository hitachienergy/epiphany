# Epiphany CLI UX

Affected version: unknown

## Goals

This document aim is to improve user experience with epicli tool with strong emphasis to lower entry level for new users. It provides idea for following scenarios: 
 * epicli installation
 * environment initialization and deployment
 * environment component update
 * cli tool update
 * add component to existing environment
 
## Assumptions

Following scenarios assume: 
 * there is component version introduced - epicli version is separated from component version. It means that i.e. epicli v0.0.1 can provide component PostgreSQL 10.x and/or PostgreSQL 11.x.
 * there is server-side component - epiphany environment is always equipped with server side daemon component exposing some API to epicli. 
 
## Convention
I used square brackets with dots inside: 
```
[...]
```
to indicate processing or some not important for this document output. 

## Story

### epicli installation

To increase user base we need to provide brew formulae to allow simple installation. 
```
> brew install epicli
``` 
 
### environment initialization and deployment

#### init

As before user should be able to start interaction with epicli with `epicli init` command. In case of no parameters interactive version would be opened. 
```
> epicli init 
What cloud provider do you want to use? (Azure, AWS): AWS
Is that a production environment? No
Do you want Single Node Kubernetes?: No
How many Kubernetes Masters do you want?: 1
How many Kubernetes Nodes do you want?: 2
Do you want PostgreSQL relational database?: Yes
Do you want RabbitMQ message broker?: No
Name your new Epiphany environment: test1
There is already environment called test1, please provide another name: test2
[...]
Your new environment configuration was generated! Go ahead and type: 'epicli status' or 'epicli apply. 
```

It could also be `epicli init -p aws -t nonprod -c postgresql ....` or `epicli --no-interactive -p aws` for non-interactive run. 

#### inspect .epicli/

Previous command generated files in ~/.epicli directory. 
```
> ls –la ~/.epicli
config
environemts/
> ls –la ~/.epicli/environments/
test2/
> ls –la ~/.epicli/environments/test2/
test2.yaml
> cat ~/.epicli/config
version: v1
kind: Config 
preferences: {} 
environments: 
- environment: 
  name: test2 
    localStatus: initialized
    remoteStatus: unknown
users: 
- name: aws-admin 
contexts: 
- context: 
  name: test2-aws-admin
    user: aws-admin
    environment: test2
current-context: test2-admin
```

#### status after init

Output from `epicli init` asked to run `epicli status`. 
```
> epicli status
Client Version: 0.5.3
Environment version: unknown
Environment: test2
User: aws-admin
Local status: initialized
Remote status: unknown
Cloud:
  Provider: AWS
  Region: eu-central-1
  Authorization: 
    Type: unknown
    State: unknown
Components: 
  Kubernetes: 
    Local status: initialized
    Remote status: unknown
    Nodes: ? (3)
    Version: 1.17.1
  PostgreSQL: 
    Local status: initialized
    Remote status: unknown
    Nodes: ? (1)
    Version: 11.2
---
You are not connected to your environment. Please type 'epicli init cloud' to provide authorization informations!    
```

As output is saying for now this command only uses local files in ~/.epicli directory. 

#### init cloud

Follow instructions to provide cloud provider authentication.  
```
> epicli init cloud
Provide AWS API Key: HD876KDKJH9KJDHSK26KJDH 
Provide AWS API Secret: ***********************************
[...]
Credentials are correct! Type 'epicli status' to check environment. 
```

Or in non-interactive mode something like: `epicli init cloud -k HD876KDKJH9KJDHSK26KJDH -s dhakjhsdaiu29du2h9uhd2992hd9hu`. 

#### status after init cloud

Follow instructions. 
```
> epicli status 
Client Version: 0.5.3
Environment version: unknown 
Environment: test2 
User: aws-admin 
Local status: initialized 
Remote status: unknown 
Cloud: 
  Provider: AWS 
  Region: eu-central-1 
  Authorization:  
    Type: key-secret
    State: OK
Components:  
  Kubernetes:  
    Local status: initialized 
    Remote status: unknown 
    Nodes: ? (3) 
    Version: 1.17.1 
  PostgreSQL:  
    Local status: initialized 
    Remote status: unknown 
    Nodes: ? (1) 
    Version: 11.2  
--- 
Remote status is unknown! Please type 'epicli status update' to synchronize status with remote. 
```

#### status update

As epicli was able to connect to cloud but it doesn't know remote state it asked to update state. 
```
> epicli status update
[...]
Remote status updated!
> epicli status 
Client Version: 0.5.3
Environment version: unknown 
Environment: test2 
User: aws-admin 
Local status: initialized 
Remote status: uninitialized
Cloud: 
  Provider: AWS 
  Region: eu-central-1 
  Authorization:  
    Type: key-secret
    State: OK
Components:  
  Kubernetes:  
    Local status: initialized 
    Remote status: uninitialized
    Nodes: 0 (3) 
    Version: 1.17.1 
  PostgreSQL:  
    Local status: initialized 
    Remote status: uninitialized
    Nodes: 0 (1) 
    Version: 11.2 
--- 
Your cluster is uninitialized. Please type 'epicli apply' to start cluster setup. 
Please type 'epicli status update' to synchronize status with remote.
```
 
It connected to cloud provider and checked that there is no cluster. 

#### apply
```
> epicli apply
[...]
---
Environment 'test2' was initialized successfully! Plese type 'epicli status' to see status or 'epicli components' to list components. To login to kubernetes cluster as root please type 'epicli components kubernetes login'. 
Command 'epicli status' will synchronize every time now, so no need to run 'epicli status update'
```

epicli knows now that there is cluster and it will connect for status every time user types `epicli status` unless some additional preferences are used. 

#### status after apply

Now it connects to cluster to check status. That relates to assumption from the beginning of this document that there is some server-side component providing status. Other way `epicli status` would have to call multiple services for status. 
```
> epicli status 
[...]
Client Version: 0.5.3
Environment version: 0.5.3
Environment: test2 
User: aws-admin 
Status: OK
Cloud: 
  Provider: AWS 
  Region: eu-central-1 
  Authorization:  
    Type: key-secret
    State: OK
Components:  
  Kubernetes:  
    Status: OK
    Nodes: 3 (3)
    Version: 1.17.1 
  PostgreSQL:  
    Status: OK
    Nodes: 1 (1) 
    Version: 11.2  
--- 
Your cluster is fully operational! Plese type 'epicli components' to list components. To login to kubernetes cluster as root please type 'epicli components kubernetes login'.
```

#### kubernetes login
```
> epicli components kubernetes login
[...]
You can now operate your kubernetes cluster via 'kubectl' command! 
```

Content is added to ~/.kube/config file. To be agreed how to do it. 
```
> kubectl get nodes
[...]
```

#### components

RabbitMQ is here on the list but with “-“ because it is not installed. 
```
> epicli components
[...]
+kubernetes
+postgresql
- rabbitmq
```

#### component status
```
> epicli components kubernetes status
[...]
Status: OK 
Nodes: 3 (3) 
Version: 1.17.1 (current)  
Running containers: 12
Dashboard: http://12.13.14.15:8008/ 
```

### environment component update

3 months passed and new version of Epiphany component was released. There is no need to update client and there is no need to update all components at once. Every component is upgradable separately. 

#### component status

`epicli status` command will notify user that there is new component version available. 
```
> epicli components kubernetes status
[...]
Status: OK 
Nodes: 3 (3) 
Version: 1.17.1 (outdated)  
Running containers: 73
Dashboard: http://12.13.14.15:8008/
---
Run 'epicli components kubernetes update' to update to 1.18.1 version! Use '--dry-run' flag to check update plan. 
```

#### component update
```
> epicli components kubernetes update
[...]
Kubernetes was successfully updated from version 1.17.1 to 1.18.1! 
```
It means that it updated ONLY one component. User could probably write something like `epicli components update` or even `epicli update` but there is no need to go all in, if one does not want to. 

### cli tool update  

User typed `brew update` in and epicli was updated to newest version.

#### status
```
> epicli status 
[...]
Client Version: 0.7.0
Environment version: 0.5.3
Environment: test2 
User: aws-admin 
Status: OK
Cloud: 
  Provider: AWS 
  Region: eu-central-1 
  Authorization:  
    Type: key-secret
    State: OK
Components:  
  Kubernetes:  
    Status: OK
    Nodes: 3 (3)
    Version: 1.18.1 
  PostgreSQL:  
    Status: OK
    Nodes: 1 (1) 
    Version: 11.2  
--- 
Your cluster is fully operational! Plese type “epicli components” to list components. To login to kubernetes cluster as root please type “epicli components kubernetes login”.
Your client version is newer than environment version. You might consider updating environment metadata to newest version. Read more at https://epiphany-platform.github.io/environment-version-update. 

```

It means that there is some metadata on cluster with information that it was created and governed with epicli version 0.5.3 but new version of epicli binary can still communicate with environment. 

### add component to existing environment

There is already existing environment and we want to add new component to it. 

#### component init
```
> epicli components rabbitmq init
[...]
RabbitMQ config was added to your local configuration. Please type “epicli apply” to apply changes. 
```
Component configuration files were generated in .epicli directory. Changes are still not applied.

#### apply 
``` 
> epicli apply
[...]
---
Environment “test2” was updated! Plese type “epicli status” to see status or “epicli components” to list components. To login to kubernetes cluster as root please type “epicli components kubernetes login”. 
Command “epicli status” will synchronize every time now, so no need to run “epicli status update”
```
 
## Daemon

We should also consider scenario with web browser management tool. It might look like: 
```
> epicli web
open http://127.0.0.1:8080 to play with environments configuration. Type Ctrl-C to finish ...
[...]
```

User would be able to access tool via web browser based UI to operate it even easier. 

## Context switching

Content of `~/.epicli` directory indicates that if user types `epicli init -n test3` there will be additional content generated and user will be able to do something like `epicli context use test3` and `epicli context use test2`. 
