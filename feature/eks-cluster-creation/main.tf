# # Kubernetes provider
# # https://learn.hashicorp.com/terraform/kubernetes/provision-eks-cluster#optional-configure-terraform-kubernetes-provider
# # To learn how to schedule deployments and services using the provider, go here: ttps://learn.hashicorp.com/terraform/kubernetes/deploy-nginx-kubernetes.

provider "kubernetes" {
  version                = ">= 1.11.1"
  load_config_file       = "false"
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}

provider "aws" {
  version     = ">= 2.28.1"
  region      = var.region
  access_key  = var.access_key
  secret_key  = var.secret_key
}

// Minimum terraform version
terraform {
  required_version = ">= 0.12"
}

// Generate random suffix onto each object name to avoid collisions
provider "random" {
  version = "~> 2.1"
}

locals {
  cluster_name                  = "training-eks-${random_string.suffix.result}"
  k8s_service_account_namespace = "kube-system"
  k8s_service_account_name      = "cluster-autoscaler-aws-cluster-autoscaler"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
}
