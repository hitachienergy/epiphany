module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.eks_cluster_name
  subnets         = module.vpc.private_subnets
  cluster_version = var.eks_cluster_version

  tags = {
    Environment = var.environment
  }

  vpc_id = module.vpc.vpc_id

  worker_groups = [
    {
      name                          = var.worker_group1
      instance_type                 = "t2.small"
      asg_desired_capacity          = 2
      asg_min_size                  = 1
      asg_max_size                  = 5
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
    },
    {
      name                          = var.worker_group2
      instance_type                 = "t2.medium"
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
      asg_desired_capacity          = 1
      asg_min_size                  = 1
      asg_max_size                  = 3
    },
  ]
}

data "aws_eks_cluster"      "cluster" { name = module.eks.cluster_id }
data "aws_eks_cluster_auth" "cluster" { name = module.eks.cluster_id }
