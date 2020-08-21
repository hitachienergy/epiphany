resource "helm_release" "cluster-autoscaler" {
  name  = "cluster-autoscaler"
  chart = "stable/cluster-autoscaler"
  version = var.eks_autoscaler_chart_version
  cleanup_on_fail = "true"
  namespace = "kube-system"
  timeout = 300

  set {
    name  = "cloudProvider"
    type  = "string"
    value = "aws"
  }
  set {
    name  = "awsRegion"
    type  = "string"
    value = var.region
  }
  set {
    name  = "autoDiscovery.clusterName"
    type  = "string"
    value = var.eks_cluster_name
  }
  set {
    name  = "autoDiscovery.enabled"
    type  = "string"
    value = "true"
  }
  set {
    name  = "image.repository"
    type  = "string"
    value = "k8s.gcr.io/autoscaling/cluster-autoscaler"
  }
  set {
    name  = "image.tag"
    type  = "string"
    value = var.eks_autoscaler_version
  }
  set {
    name  = "extraArgs.scale-down-utilization-threshold"
    type  = "auto"
    value = var.cluster-autoscaler_scale-down-utilization-threshold
  }
  set {
    name  = "rbac.serviceAccountAnnotations.eks\\.amazonaws\\.com/role-arn"
    type = "string"
    value = var.cluster-autoscaler_rbac
  }
}
