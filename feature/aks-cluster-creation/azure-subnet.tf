#####################################################
# DO NOT Modify by hand - Managed by Automation
#####################################################
#####################################################
# This file can be used as a base template to build other Terraform files. It attempts to use as much
# Terraform interprolation as possible by creating Terraform variables instead of changing inline
# this approach provides an easier way to do creative looping, fetch IDs of created resources etc.
#####################################################
#####################################################
# {{ specification.name }}
#####################################################

resource "azurerm_subnet" "subnet" {
  count = "${var.existing_vnet_subnet_id != "" ? 0 : 1}"
  name                 = "${var.prefix}-subnet-aks"
  address_prefixes     = "${var.aks_address_prefix}"
  resource_group_name  = azurerm_resource_group.aks-rg[0].name
  virtual_network_name = azurerm_virtual_network.vnet[0].name
}

