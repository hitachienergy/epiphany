resource "helm_release" "cluster-autoscaler" {
  name  = "cluster-autoscaler"
  chart = "stable/cluster-autoscaler"
  version = var.eks_autoscaler_chart_version
  cleanup_on_fail = "true"
  namespace = "kube-system"

  set {
    name  = "cloudProvider"
    value = "aws"
  }
  set {
    name  = "awsRegion"
    value = var.region
  }
  set {
    name  = "autoDiscovery.clusterName"
    value = var.cluster_name
  }
  set {
    name  = "autoDiscovery.enabled"
    value = "true"
  }
  set {
    name  = "image.repository"
    value = "k8s.gcr.io/autoscaling/cluster-autoscaler"
  }
  set {
    name  = "image.tag"
    value = var.eks_autoscaler_version
  }
  set {
    name  = "extraArgs.scale-down-utilization-threshold"
    value = var.cluster-autoscaler_scale-down-utilization-threshold
  }
  set {
    name  = "rbac.serviceAccountAnnotations.eks\\.amazonaws\\.com/role-arn"
    value = "arn:aws:iam::540350320930:role/cluster-autoscaler"
    type = "string"
  }
  timeout = 300
}
