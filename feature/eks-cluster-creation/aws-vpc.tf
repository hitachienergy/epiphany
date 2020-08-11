// VPC, Subnets, Availability zones

data "aws_availability_zones" "available" {}

module "vpc" {
  source               = "terraform-aws-modules/vpc/aws"
  version              = "2.6.0"
  name                 = var.vpc_name
  cidr                 = var.cidr
  azs                  = data.aws_availability_zones.available.names
  // private_subnets      = var.private_subnets
  public_subnets       = var.public_subnets
  // enable_nat_gateway   = true
  // single_nat_gateway   = true
  enable_dns_hostnames = true
  // tags = {
  //   "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  // }
  // private_subnet_tags = {
  //   "kubernetes.io/cluster/${local.cluster_name}" = "shared"
  //   "kubernetes.io/role/internal-elb"             = "1"
  // }

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }
}
