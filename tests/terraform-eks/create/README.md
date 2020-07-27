## Terraform scripts to provision EKS cluster #
***


The Amazon Elastic Kubernetes Service (EKS) is the AWS service for deploying, managing, and scaling containerized applications with Kubernetes. This repo contain terraform files, to automate the EKS cluster deployment.
***

#### Requirements:
- AWS account with the IAM permissions listed on the [EKS module documentation](https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/iam-permissions.md)
- Configured AWS CLI
- AWS IAM Authenticator
- kubectl
- terraform

#### Deployment:
- Initialize working directory:  
``` terraform init```
- Create execution plan:  
``` terraform plan```
- Create a cluster:  
``` terraform apply```
- Destroy the cluster:  
``` terraform destroy```


#### Files overview:
- aws-eks.tf   
Provisions all the resources (AutoScaling Groups, etc...) required to set up an EKS cluster in the private subnets and bastion servers to access the cluster using the AWS EKS Module.
- aws-security-groups.tf  
Provisions the security groups used by the EKS cluster.
- aws-vpc.tf  
Provisions a VPC, subnets and availability zones using the AWS VPC Module.
- main.fg
Setup kubernetes and aws providers.
- output.tf  
Defines the output configuration.
- vars.tf  
Sets the min component versions and setup vars used on other files
> Be aware that, there should be also a file `vars-secret.tf` which contain two variables required to log-in into Azure: `access_key` and `secret_key`.  This file is not included into this repo because of security reasons.

***

#### Sources
- https://learn.hashicorp.com/terraform/kubernetes/provision-eks-cluster
- https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.32.0