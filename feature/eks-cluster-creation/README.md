## Terraform scripts to provision EKS cluster #
***


The Amazon Elastic Kubernetes Service (EKS) is the AWS service for deploying, managing, and scaling containerized applications with Kubernetes. This repo contain terraform files, to automate the EKS cluster deployment.
***

#### Requirements:
- AWS account with the IAM permissions listed on the [EKS module documentation](https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/iam-permissions.md) - set credentials in `vars-secret.tf` file.
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
- When cluster is depoyed, you should be already connected to the cluster using null_resource kubeconfig.
- Whenever you switch into diffrent config, you can easly go back to the cluster using bellow command:
```aws eks --region $REGION update-kubeconfig --name $CLUSTER_NAME```

#### Files overview:
- aws-eks.tf   
Provisions all the resources (AutoScaling Groups, etc...) required to set up an EKS cluster in the private subnets and bastion servers to access the cluster using the AWS EKS Module.
- aws-resource-groups.tf  
Provisions the resource groups to nicely group EKS EC2 resources.
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
- vars-secret.tf  
File containing secret credentials to authorize into AWS. Currently this file is not included into repo, becasue of the security reasons. As example, file `vars-secret.tf-example` has been created. Adjust variables `access_key` and `secret_key`, than remove the `-example` extension do deploy k8s cluster.

***

#### Sources
- https://learn.hashicorp.com/terraform/kubernetes/provision-eks-cluster
- https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.32.0