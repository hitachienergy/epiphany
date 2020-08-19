// Cluster version
variable "eks_cluster_version" {
  // default = "1.17"
  default = "1.16"
}

variable "eks_autoscaler_version" {
  // default = "v1.17.3"
  default = "v1.16.6"
}

variable "eks_autoscaler_chart_version" {
  default = "7.3.4"
}

// AWS Region
variable "region" {
  default = "eu-central-1"
}

// Environment type (used to tag resources)
variable "environment" {
  default = "testing"
}

// AWS VPC name
variable "vpc_name" {
  default = "eks-terraform-vpc"
}

// AWS Resource group name
variable "resource_group_name" {
  default = "eks-terraform-rg"
}

// Cluster name
variable "cluster_name" {
  default = "gdajuk-cluster"
}

// IAM roles save path
variable "iam_path" {
  default = "/autoscale"
}

// Autoscaling threshold
variable "cluster-autoscaler_scale-down-utilization-threshold" {
  default = "0.65"
}

// Save kubeconfig
variable "write_kubeconfig" {
  default = "true"
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
  default = {
    name = "eks-worker-1"
    instance_type = "t2.medium"
    asg_desired_capacity = 1
    asg_min_size = 1
    asg_max_size = 10
  }
}

variable "worker2_data" {
  type = object({
    name                 = string
    instance_type        = string
    asg_desired_capacity = number
    asg_min_size         = number
    asg_max_size         = number
  })
  default = {
    name = "eks-worker-2"
    instance_type = "t2.medium"
    asg_desired_capacity = 1
    asg_min_size = 1
    asg_max_size = 5
  }
}

// VPC CIDR
variable "cidr" {
  default = "10.0.0.0/16"
}

// VPC Private subnet list
variable "private_subnets" {
  type = list
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24"
  ]
}

// VPC Public subnet list
variable "public_subnets" {
  type = list
  default = [
    "10.0.4.0/24",
    "10.0.5.0/24",
    "10.0.6.0/24"
  ]
}
// AWS Security group list
variable "secgrp_mgmt_one" {
  type = list
  default = [
    "10.0.0.0/8"
  ]
}
variable "secgrp_mgmt_two" {
  type = list
  default = [
    "192.168.0.0/16"
  ]
}
variable "secgrp_mgmt_all" {
  type = list
  default = [
      "10.0.0.0/8",
      "172.16.0.0/12",
      "192.168.0.0/16"
  ]
}
