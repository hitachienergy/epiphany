// VPC, Subnets, Availability zones
data "aws_availability_zones" "available" {}

module "vpc" {
  create_vpc           = var.existing_vpc_id != "" ? false : true
  source               = "terraform-aws-modules/vpc/aws"
  version              = "2.6.0"
  name                 = var.vpc_name
  cidr                 = var.cidr
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = var.private_subnets
  public_subnets       = var.public_subnets
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }
}
