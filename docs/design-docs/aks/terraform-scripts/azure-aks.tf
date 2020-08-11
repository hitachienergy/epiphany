resource "azurerm_kubernetes_cluster" "aks" {
    name                = "${var.prefix}-aks"
    location            = var.location
    dns_prefix          = var.prefix
    resource_group_name = var.existing_resource_group_name != "" ? var.existing_resource_group_name : azurerm_resource_group.aks-rg[0].name
	node_resource_group = "${var.prefix}-rg-worker"
    kubernetes_version  = var.kubernetes_version


	default_node_pool {
		name                  = substr(var.default_node_pool.name, 0, 12)
		node_count            = var.default_node_pool.node_count
		vm_size               = var.default_node_pool.vm_size
		vnet_subnet_id        = var.existing_vnet_subnet_id != "" ? var.existing_vnet_subnet_id : azurerm_subnet.subnet[0].id
		orchestrator_version  = var.kubernetes_version
		os_disk_size_gb       = var.default_node_pool.os_disk_size_gb
		enable_node_public_ip = var.nodes_public_ip
        type                  = var.default_node_pool.type
        enable_auto_scaling   = var.default_node_pool.enable_auto_scaling
        min_count             = var.default_node_pool.min_count
        max_count             = var.default_node_pool.max_count
     }

    identity {
      type = "SystemAssigned"
    }

    linux_profile {
        admin_username = var.linux_admin_username
        ssh_key {
            key_data = file(var.public_ssh_key_path)
        }
    }

	network_profile {
	    network_plugin     = var.network_policy == "azure" ? "azure" : var.network_plugin
	    network_policy     = var.network_policy
    }

    addon_profile {
        kube_dashboard {
        enabled = true
        }
    }
    auto_scaler_profile {
        balance_similar_node_groups = var.auto_scaler_profile.balance_similar_node_groups
        max_graceful_termination_sec = var.auto_scaler_profile.max_graceful_termination_sec
        scale_down_delay_after_add = var.auto_scaler_profile.scale_down_delay_after_add
        scale_down_delay_after_delete = var.auto_scaler_profile.scale_down_delay_after_delete
        scale_down_delay_after_failure = var.auto_scaler_profile.scale_down_delay_after_failure
        scan_interval = var.auto_scaler_profile.scan_interval
        scale_down_unneeded = var.auto_scaler_profile.scale_down_unneeded
        scale_down_unready = var.auto_scaler_profile.scale_down_unready
        scale_down_utilization_threshold = var.auto_scaler_profile.scale_down_utilization_threshold
    }

    tags = {
        Environment = var.prefix
    }
}

resource "azurerm_kubernetes_cluster_node_pool" "aks" {
        count = var.additional_cluster_node_pools.node_count > "0" ? 1 : 0
        kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
        name                  = substr(var.additional_cluster_node_pools.name, 0, 6)
        node_count            = var.additional_cluster_node_pools.node_count  
        vm_size               = var.additional_cluster_node_pools.vm_size
        vnet_subnet_id        = var.existing_vnet_subnet_id != "" ? var.existing_vnet_subnet_id : azurerm_subnet.subnet[0].id
        orchestrator_version  = var.kubernetes_version
        os_disk_size_gb       = var.additional_cluster_node_pools.os_disk_size_gb
        enable_node_public_ip = var.nodes_public_ip
        os_type               = var.additional_cluster_node_pools.os_type
        enable_auto_scaling   = var.additional_cluster_node_pools.enable_auto_scaling
        min_count             = var.additional_cluster_node_pools.min_count
        max_count             = var.additional_cluster_node_pools.max_count
}
