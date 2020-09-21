## Terraform scripts to provision EKS cluster #
***


The Amazon Elastic Kubernetes Service (EKS) is the AWS service for deploying, managing, and scaling containerized applications with Kubernetes. This repo contain terraform files, to automate the EKS cluster deployment.
***

#### Requirements:
- AWS account with the IAM permissions listed on the [EKS module documentation](https://github.com/terraform-aws-modules/terraform-aws-eks/blob/master/docs/iam-permissions.md) - set credentials in `vars-secret.tf` file.
- kubectl
- terraform in version at least 0.12.9
- helm and added repository: ``` helm repo add stable https://kubernetes-charts.storage.googleapis.com ```
- awscli ``` aws configure ```
- ssh-key uploaded into [AWS](https://www.eksworkshop.com/020_prerequisites/sshkey/) - in case you need to connect into the node
- adjusted `terraform.tfvars` file. Mandatory options to change: `eks_cluster_name` and `eks_autoscaler_name`.

#### Features:
- Possibility to create new network or use existing network. EKS will just join to the existing network. It is enough to set two variables with existing VPC ID and SUBNETS ID and EKS will be based there ( var.existing_vpc_id and var.existing_subnets_id ). [VPC considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html)
- Cluster autoscaling
- Different cluster specification  (size, location, name, k8s version, name etc...)

#### Deployment:
- Initialize working directory:  
``` terraform init```
- Create execution plan:  
``` terraform plan```
- Create a cluster:  
``` terraform apply -var-file=terraform.tfvars```
- Destroy the cluster:  
``` terraform destroy```
- When cluster is depoyed, you should be already connected to the cluster using null_resource kubeconfig.
- Whenever you switch into diffrent config, you can easly go back to the cluster using bellow command:
```aws eks --region $REGION update-kubeconfig --name $CLUSTER_NAME```

#### Files overview:
- aws-eks.tf   
Provisions all the resources (AutoScaling Groups, etc...) required to set up an EKS cluster in the private subnets and bastion servers to access the cluster using the AWS EKS Module.
- aws-autoscaling-groups.tf  
Provisions the autoscaling groups/roles to provide autoscaler functionality.
- aws-resource-groups.tf  
Provisions the resource groups to nicely group EKS EC2 resources.
- aws-security-groups.tf  
Provisions the security groups used by the EKS cluster.
- aws-vpc.tf  
Provisions a VPC, subnets and availability zones using the AWS VPC Module.
- aws-autoscaler.tf  
Deploy autoscaler pod, which is responsible, for load-ballancing on the cluster.
- aws-metrics-server.tf  
Deploy the metric server pod, required for autoscaler.  
- main.tf  
Setup kubernetes and aws providers.
- output.tf  
Defines the output configuration.
- terraform.tfvars  
Sets the min component versions and setup vars used on other files
- vars.tf  
Set the variables types, to avoid typos.
- vars-secret.tf  
File containing secret credentials to authorize into AWS. Currently this file is not included into repo, becasue of the security reasons. As example, file `vars-secret.tf-example` has been created. Adjust variables `access_key` and `secret_key`, than remove the `-example` extension do deploy k8s cluster.

***

## Testing the autoscaling feature

***
#### Requirements:
- working deployment of EKS cluster
- kubectl

#### Test:
- Apply deployment with simple php-apache image:  
``` kubectl apply -f https://k8s.io/examples/application/php-apache.yaml```
- Create horizontal pod autoscale based on CPU/Memory or some other from eg. prometheus metrics. Server metrics is installed by default in AKS version higher then 1.10  
```kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=50 ```
- Create a load-generator deployment file (load-gen.yaml) to test LB:
```
kind: Deployment
apiVersion: apps/v1
metadata:
  name: load-generator
spec:
  selector:
    matchLabels:
      run: load-generator
  replicas: 1
  template:
    metadata:
      labels:
        run: load-generator
    spec:
      containers:
      - name: load-generator
        image: busybox
        args:
        - /bin/sh
        - "-c"
        - "while true; do wget -q -O- http://php-apache; done"
```  
- Execute the deployment with a containers in order to increase load on nodes using infinite loop of queries to the php-apache service created in previous point.:  
```kubectl apply -f load-gen.yaml```  
- Increase load as needed   
```kubectl scale deployment load-generator --replicas=5```  
- Check the effect using monitoring tools:  
```kubectl get hpa```  
- Check the autoscaller logs: 
```kubectl  logs -n kube-system cluster-autoscaler...*```


#### Sources
- https://learn.hashicorp.com/terraform/kubernetes/provision-eks-cluster
- https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/2.32.0
- https://registry.terraform.io/modules/terraform-aws-modules/iam/aws/2.7.0/submodules/iam-assumable-role-with-oidc
