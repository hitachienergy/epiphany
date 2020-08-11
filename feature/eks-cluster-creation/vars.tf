// -- [ VARS ] ------------------------------------------------------
// Cluster name
// variable "eks_cluster_name" {
//   default = "eks-terraform-cluster"
// }

// Cluster version
variable "eks_cluster_version" {
  default = "1.16"
}

variable "iam_path" { default = "/autoscale" }

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
    asg_desired_capacity = 2
    asg_min_size = 1
    asg_max_size = 10
  }
}

// variable "worker2_data" {
//   type = object({
//     name                 = string
//     instance_type        = string
//     asg_desired_capacity = number
//     asg_min_size         = number
//     asg_max_size         = number
//   })
//   default = {
//     name = "eks-worker-2"
//     instance_type = "t2.medium"
//     asg_desired_capacity = 1
//     asg_min_size = 1
//     asg_max_size = 5
//   }
// }

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
