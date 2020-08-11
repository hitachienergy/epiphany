module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "12.2.0"
  cluster_name    = local.cluster_name
  subnets         = module.vpc.public_subnets
  // subnets         = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id
  cluster_version = var.eks_cluster_version
  enable_irsa     = true
  // manage_cluster_iam_resources = true
  // manage_worker_iam_resources  = true

  // tags = {
  //   Environment = var.environment
  // }

  worker_groups = [
    {
      name                          = var.worker1_data["name"]
      instance_type                 = var.worker1_data["instance_type"]
      asg_desired_capacity          = var.worker1_data["asg_desired_capacity"]
      asg_min_size                  = var.worker1_data["asg_min_size"]
      asg_max_size                  = var.worker1_data["asg_max_size"]
      // additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
      tags = [
        {
          "key"                 = "k8s.io/cluster-autoscaler/enabled"
          "propagate_at_launch" = "false"
          "value"               = "true"
        },
        {
          "key"                 = "k8s.io/cluster-autoscaler/${local.cluster_name}"
          "propagate_at_launch" = "false"
          "value"               = "true"
        },
      ]
    },
    // {
    //   name                          = var.worker2_data["name"]
    //   instance_type                 = var.worker2_data["instance_type"]
    //   asg_desired_capacity          = var.worker2_data["asg_desired_capacity"]
    //   asg_min_size                  = var.worker2_data["asg_min_size"]
    //   asg_max_size                  = var.worker2_data["asg_max_size"]
    //   // additional_security_group_ids = [aws_security_group.worker_group_mgmt_two.id]
    //   tags = [
    //     {
    //       "key"                 = "k8s.io/cluster-autoscaler/enabled"
    //       "propagate_at_launch" = "false"
    //       "value"               = "true"
    //     },
    //     {
    //       "key"                 = "k8s.io/cluster-autoscaler/${local.cluster_name}"
    //       "propagate_at_launch" = "false"
    //       "value"               = "true"
    //     }
    //   ]
    // },
  ]
}

data "aws_eks_cluster"      "cluster" { name = module.eks.cluster_id }
data "aws_eks_cluster_auth" "cluster" { name = module.eks.cluster_id }

resource "null_resource" "kubeconfig" {
  provisioner "local-exec" {
    // command = "export KUBECONFIG=kubeconfig_${var.eks_cluster_name}"
    command = "export KUBECONFIG=kubeconfig_${local.cluster_name}"
  }
}
