// -- [ VARS ] ------------------------------------------------------

// If You want to use existing network and resource group, just update the two variables, if not, leave them empty:
variable "existing_vnet_subnet_id" {
	description = "Resource id of existing the Virtual Network subnet where You want to join Your AKS cluster"
	type        = string
	default     = ""
}

variable "existing_resource_group_name" {
	description = "Name of the existing AKS cluster resource group where You want to join Your AKS cluster"
	type        = string
	default     = ""
}

// General variables:

variable "prefix" {
    description = "Prefix for resources's name"
    type        = string
}

variable "location" {
    description = "AKS cluster location"
    type        = string
}

variable "kubernetes_version" {
	description = "Kubernetes version"
	type        = string
}

variable "vnet_address_space" {
	description = "Network address space"
	type        = list(string)
}

variable "aks_address_prefix" {
	description = "SubNetwork address space"
	type        = list(string)
}

variable "public_ssh_key_path" {
    description = "Public ssh key path"
    type        = string
}

variable "nodes_public_ip" {
    description = "Assign a public IP per node for your node pools. In order to allow that, You have to install latest aks-preview extension and register feature for Node Public IP following the url: https://docs.microsoft.com/en-us/azure/aks/use-multiple-node-pools#assign-a-public-ip-per-node-for-your-node-pools-preview "
    type        = bool
}

variable "network_plugin" {
    description = "azure or kubenet supported only, if network policy set to azure, network plugin must be set to azure"
    type        = string
}

variable "network_policy" {
    description = "azure or calico supported, when Azure is set, network plugin must be set Azure value too"
    type        = string
}

variable "linux_admin_username" {
    description = "Admin user on Linux OS"
    type        = string
}

variable "default_node_pool" {
  description = "The object to configure the default node pool with number of worker nodes, worker node VM size and Availability Zones."
  type = object({
    name                           = string
    node_count                     = number
    vm_size                        = string
    os_disk_size_gb                = string
    type                           = string
    enable_auto_scaling            = bool
    min_count                      = number
    max_count                      = number
  })
}


variable "additional_cluster_node_pools" {
  
  description = "The map object to configure one or several additional node pools with number of worker nodes, worker node VM size and Availability Zones."
  type = object({
    name                           = string
    node_count                     = number
    vm_size                        = string
    os_type                        = string
    os_disk_size_gb                = string
    type                           = string
    enable_auto_scaling            = bool
    min_count                      = number
    max_count                      = number
  })
}

