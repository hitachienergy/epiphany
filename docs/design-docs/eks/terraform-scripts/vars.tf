// // EKS Cluster name
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

// AWS Resource group name
variable "resource_group_name" {
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

// Rbac installation path
variable "cluster-autoscaler_rbac" {
  type = string
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
