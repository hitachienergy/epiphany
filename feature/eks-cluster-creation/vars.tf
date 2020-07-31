// -- [ VARS ] ------------------------------------------------------
// Cluster name
variable "eks_cluster_name"     { default = "eks-terraform-cluster" }
// Cluster version
variable "eks_cluster_version"  { default = "1.17" }
// AWS Region
variable "region"               { default = "eu-central-1" }
// Environment type (used to tag resources)
variable "environment"          { default = "testing" }
// AWS VPC name
variable "vpc_name"             { default = "eks-terraform-vpc" }
// AWS Resource group name
variable "resource_group_name"  { default = "eks-terraform-rg" }
// AWS Worker nodes name
variable "worker_group1"        { default = "eks-worker-1" }
variable "worker_group2"        { default = "eks-worker-2"}
// VPC CIDR
variable "cidr"                 { default = "10.0.0.0/16"}

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

// -- [ VERSIONS & PROVIDERS ] --------------------------------------
terraform { required_version = ">= 0.12" }
provider "random" { version = "~> 2.1" }
