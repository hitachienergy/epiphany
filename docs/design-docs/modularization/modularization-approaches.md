# Intent

This document tries to compare 3 existing propositions to implement modularization. 

# Compared models

To introduce modularization in Epiphany we identified 3 approaches to consider. Following sections will describe briefly those 3 approaches. 

## Dockerized custom modules

This approach would look following way:
* Each component management code would be packaged into docker containers
* Components would need to provide some known call methods to expose metadata (dependencies, info, state, etc.)
* Each component would be managed by one management container
* Components (thus management containers) can depend on each other in ‘pre-requisite’ manner (not runtime dependency, but order of executions)
* Separate wrapper application to call components execution and process metadata (dependencies, info, state, etc.)

All that means that if we would like to install following stack: 
* On-prem Kubernetes cluster
* Rook Operator with Ceph cluster working on that on-prem cluster
* PostgreSQL database using persistence provided by Ceph cluster, 

Then steps would need to look somehow like this:
* CLI command to install PostgreSQL
* It should check pre-requisites and throw an error that it cannot be installed because there is persistence layer missing
* CLI command to search persistence layer
* It would provide some possibilities
* CLI command to install rook
* It should check pre-requisites and throw an error that it cannot be installed because there is Kubernetes cluster missing
* CLI command to search Kubernetes cluster
* It would provide some possibilities
* CLI command to install on-prem Kubernetes 
* It should perform whole installation process
* CLI command to install rook
* It should perform whole installation process
* CLI command to install PostgreSQL
* It should perform whole installation process

## Terraform providers

This approach would mean following: 
* We reuse most of terraform providers to provide infrastructure
* We reuse Kubernetes provider to deliver Kubernetes resources
* We provide “operator” applications to wrap ansible parts in terraform-provider consumable API (???)
* Separate wrapper application to instantiate “operator” applications and execute terraform

All that means that if we would like to install following stack: 
* On-prem Kubernetes cluster
* Rook Operator with Ceph cluster working on that on-prem cluster
* PostgreSQL database using persistence provided by Ceph cluster, 

Then steps would need to look somehow like this: 
* Prepare terraform configuration setting up infrastructure containing 3 required elements
* CLI command to execute that configuration
* It would need to find that there is on-prem cluster provider which does not have where to connect, and it needs to instantiate “operator” container
* It instantiates “operator” container and exposes API
* It executes terraform script
* It terminates “operator” container

## Kubernetes operators

This approach would mean following:
* To run anything, we need Kubernetes cluster of any kind (local Minikube is good as well)
* We provide Kubernetes CR’s to operate components
* We would reuse some existing operators
* We would need to create some operators on our own
* There would be need to separate mechanism to create “on-prem” Kubernetes clusters (might be operator too)

All that means that if we would like to install following stack: 
* On-prem Kubernetes cluster
* Rook Operator with Ceph cluster working on that on-prem cluster
* PostgreSQL database using persistence provided by Ceph cluster, 

Then steps would need to look somehow like this: 
* Start Minikube instance on local node
* Provide CRD of on-prem Kubernetes operator
* Deploy on-prem Kubernetes operator
* Wait until new cluster is deployed
* Connect to it
* Deploy rook operator definition
* Deploy PostgreSQL operator definition

# Comparision
| Question | Dockerized custom modules (DCM) | Terraform providers (TP) | Kubernetes operators (KO) |
| :---     | :---                            | :---                     | :---                      |
| How much work does it require to package epicli to first module? | Customize entrypoint of current image to provide metadata information. | Implement API server in current image to expose it to TP. | Implement ansible operator to handle CR’s and (possibly?) run current image as tasks. |
| Sizes: | 3XL | Too big to handle. We would need to implement just new modules that way.  | 5XL |
| How much work does it require to package module CNS? | From kubectl image, provide some parameters, provide CRD’s, provide CR’s | Use (possibly?) terraform-provider-kubernetes. Prepare CRD’s, prepare CR’s. No operator required. | Just deploy Rook CRD’s, operator, CR’s. |
| Sizes: | XXL | XL | XL |
| How much work does it require to package module AKS/EKS? | From terraform, provide some parameters, provide terraform scripts | Prepare terraform scripts. No operator required. | [there is something called rancher/terraform-controller and it tries to be what we need. It’s alpha] Use (possibly?) rancher terraform-controller operator, provide DO module with terraform scripts. |
| Sizes: | XL | L | XXL |
| How would be dependencies handled? | Not defined so far. It seems that using kind of “selectors” to check if modules are installed and in state “applied” or something like this. | Standard terraform dependencies tree. It’s worth to remember that terraform dependencies sometimes work very weird and if you change one value it has to call multiple places. We would need to assess how much dependencies there should be in dependencies. | It seems that embedding all Kubernetes resources into helm charts, and adding dependencies between them could solve a problem. |
| Sizes: | XXL | XL | XXL |
| Would it be possible to install CNS module on Epiphany Kubernetes in version 0.4.4? | yes | yes | yes |
| If I want to install CNS, how would dependencies be provided? | By selectors mechanism (that is proposition) | By terraform tree | By helm dependencies |
| Let’s assume that in version 0.8.0 of epiphany PostgreSQL is migrated to new component (managed not in epicli config). How would migration from 0.7.0 to 0.8.0 on existing environments be processed? | Proposition is, that for this kind of operations we can create separate “image” to conduct just that upgrade operation. So for example epi-o0-08-upgrader. It would check that environment v0.7.x had PostgreSQL installed, then it would generate config for new PostgreSQL module, it would initialize that module and it would allow upgrade of epicli module to v0.8.x | It doesn’t look like there is a way to do it automatically by terraform. You would need to add new PostgreSQL terraform configuration and import existing state into it, then remove PostgreSQL configuration from old module (while preventing it from deletion of resources). If you are advanced terraform user it still might be tricky. I’m not sure if we are able to handle it for user. | We would need to implement whole functionality in operator. Basically very similar to DCM scenario, but triggered by CR change. |
| Sizes: | XXL | Unknown | 3XL |
| Where would module store it’s configuration? | Locally in ~/.e/ directory. In future we can implement remote state (like terraform remote backend) | All terraform options. | As Kubernetes CR. |
| How would status of components be gathered by module? | We would need to implement it. | Standard terraform output and datasource mechanisms. | Status is continuously updated by operator in CR so there it is. |
| Sizes: | XL | XS | S |
| How would modules pass variables between each other? | CLI wrapper should be aware that one module needs other module output and it should call `module1 get-output` and pass that json or part of it to `module2 apply` | Standard terraform. | Probably by Config resources. But not defined. |
| Sizes: | XXL | XS | XL |
| How would upstream module notify downstream that something changed in it’s values? | We would need to implement it. | Standard terraform tree update. Too active changes in a tree should be considered here as in dependencies. | It’s not clear. If upstream module can change downstream Config resource (what seems to be ridiculous idea) than it’s simple. Other way is that downstream periodically checks upstream Config for changes, but that introduces problems if we use existing operators. |
| Sizes: | XXL | XL | XXL |
| Sizes summary: | 1 3XL, 5 XXL, 2 XL | 1 Too big, 1 Unknown, 3 XL, 1 L, 2 XS | 1 5XL, 1 3XL, 3 XXL, 2 XL, 1 S |

# Conclusions

## Strategic POV

DCM and KO are interesting. TP is too strict and not elastic enough. 

## Tactic POV

DCM has the smallest standard deviation when you look at task sizes. It indicates the smallest risk. TP is on the opposite side of list with the biggest estimations and some significant unknowns. 

## Fast gains

If we were to consider only cloud provided resources TP is the fastest way. Since we need to provide multiple different resources and work on-prem it is not that nice. KO approach looks like something interesting, but it might be hard at the beginning. DCM looks like simplest to implement with backward compatibility. 

## Risks

DCM has significant risk of “custom development”. KO has risks related to requirement to use operator-framework and its concept, since very beginning of Epic work. TP has huge risks related to on-prem operational overhead. 

# Final thoughts

Risks related to DCM are smallest and learning curve looks best. We would also be able to be backward compatible in relatively simple way. 

**DCM looks like desired approach.** 
