output "kubeconfig" {
    sensitive = true
    value = azurerm_kubernetes_cluster.aks.kube_config_raw
}

output "kubeconfig_export" {
    value = "terraform output kubeconfig > ./kubeconfig_${var.prefix} && export KUBECONFIG=./kubeconfig_${var.prefix}"
}

output "cluster_endpoint" {
    value = azurerm_kubernetes_cluster.aks.kube_config.0.host
}
