// -- [ VARS ] -------------------------------------------------------------------------
variable "eks_cluster_name"     { default = "gdajuk-cluster" }
variable "region"               { default = "eu-central-1" }
variable "environment"          { default = "dev" }
variable "resource_group_name"  { default = "gdajuk-cluster-rg" }
variable "worker_group1"        { default = "eks-worker-1" }
variable "worker_group2"        { default = "eks-worker-2"}
variable "env_tag"              { default = "gdajuk-test"}
variable "cidr"                 { default = "10.0.0.0/16"}

variable "private_subnets" {
  type = list
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24"
  ]
}

variable "public_subnets" {
  type = list
  default = [
    "10.0.4.0/24",
    "10.0.5.0/24",
    "10.0.6.0/24"
  ]
}

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

// -- [ VERSIONS & PROVIDERS ] ------------------------------------------------------------
// Use terraform with min version of 0.12
terraform { required_version = ">= 0.12" }
// Required to generate random strings
provider "random" { version = "~> 2.1"}
// provider "local" { version = "~> 1.2" }
// provider "null"  { version = "~> 2.1" }
// provider "template" { version = "~> 2.1" }