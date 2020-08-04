# AKS design document:
## Goals:
Provide AKS cluster setup from Epiphany Platform. Fully managed master cluster by Azure. 
## Use cases:
Azure Kubernetes Service (AKS) is the service for deploying, managing, and scaling containerized applications with Kubernetes. This repo contain terraform files (will be integrated with epiphany soon) to automate the AKS cluster deployment. You can use AKS in order to speed up development, increase security, use only resources which You need and scale at speed.
## Nice to know:
- AKS require two resources group. First resource group which is managed by user and contains only the Kubernetes service resource. Second resource group, known as the node resource group, contains all of the infrastructure resources associated with the cluster. These resources include the Kubernetes node VMs, virtual networking, and storage. AKS automatically remove the node resource group whenever the cluster is removed.
- AKS require service principal to create additional resources but managed identities are essentially a wrapper around service principals, and make their management simpler. It is better to use Managed identities since are passwordless.
- AKS require default node pool which serve the primary purpose of hosting critical system pods such as CoreDNS and tunnelfront and operating system must be Linux. In additional node pools user can choose which operation system will be installed (Linux/Windows)
## Features:
- Different operating systems (Linux/Windows)
- Different virtual machines specification
- Different cluster specification (size, location, name, public ip, k8s version, name etc...)
- Different network drivers (basic/advance)
- Different resource groups
- Possibility to create new network or use existing network and resource group. AKS will just join to the existing network.
## Requirements:
- Azure account
- kubectl
- terraform
## Deployment:
- Initialize working directory:  
``` terraform init```
- Create execution plan:  
``` terraform plan```
- Create a cluster:  
``` terraform apply```
- Destroy the cluster:  
``` terraform destroy```
- When cluster is deployed, you should be already connected to the cluster using kubeconfig, which You can get from output. In order to save Your kubeconfig use the following command: ``` echo "$(terraform output kube_config)" > ./kubeconfig. ```
- Remember to export KUBECONFIG environment variable in order to use proper configuration file: ```export KUBECONFIG=./kubeconfig ```
## Files overview:
- azure-aks.tf  
Provisions all the resources (Resources Groups with default node pool and additional, network profile, vm and cluster specification etc...) required to set up an AKS cluster in the private subnets.
- azure-resource-groups.tf  
Provisions the resource groups to nicely group AKS resources.
- azure-security-groups.tf  
Provisions the security groups used by all virtual machines in new cluster. AKS by default create own customized security group only for cluster life time.
- azure-vnet.tf  
Provisions a new Network for AKS cluster 
- azure-subnet.tf
Provisions a new Subnet for AKS cluster  
- main.tf  
Setup azure providers.
- output.tf  
Defines the output configuration.
- vars.tf  
Sets the main component versions and setup vars used in other files.
## Design:
![AKS cluster](epiphany-aks.png)
#### Sources
- https://www.terraform.io/docs/providers/azurerm/r/kubernetes_cluster
- https://docs.microsoft.com/en-us/azure/aks/
