// Resource id of existing Subnets in the Virtual Network where You want to join Your EKS cluster
variable "existing_subnets_id" {
  type = list(string)
}

// Resource id of existing the Virtual Network where You want to join Your EKS cluster
variable "existing_vpc_id" {
  type = string
}

// EKS Cluster name
variable "eks_cluster_name" {
  type = string
}

// EKS Cluster version
variable "eks_cluster_version" {
  type = number
}

// EKS autoscaller version
variable "eks_autoscaler_version" {
  type = string
}

// AWS Autoscaler name
variable "eks_autoscaler_name" {
  type = string
}

// EKS chart version
variable "eks_autoscaler_chart_version" {
  type = string
}

// AWS Region
variable "region" {
  type = string
}

// Environment type (used to tag resources)
variable "environment" {
  type = string
}

// AWS VPC name
variable "vpc_name" {
  type = string
}

// IAM roles save path
variable "iam_path" {
  type = string
}

// Autoscaling threshold
variable "cluster-autoscaler_scale-down-utilization-threshold" {
  type = number
}

// Save kubeconfig
variable "write_kubeconfig" {
  type = bool
}

// Nodes/Workers objects
variable "worker1_data" {
  type = object({
    name                 = string
    instance_type        = string
    asg_desired_capacity = number
    asg_min_size         = number
    asg_max_size         = number
  })
}

variable "worker2_data" {
  type = object({
    name                 = string
    instance_type        = string
    asg_desired_capacity = number
    asg_min_size         = number
    asg_max_size         = number
  })
}

// VPC CIDR
variable "cidr" {
	type = string
}

// VPC Private subnet list
variable "private_subnets" {
	type = list(string)
}

// VPC Public subnet list
variable "public_subnets" {
	type = list(string)
}

// AWS Security group list
variable "secgrp_mgmt_one" {
	type = list(string)
}
variable "secgrp_mgmt_two" {
	type = list(string)
}
variable "secgrp_mgmt_all" {
	type = list(string)
}
