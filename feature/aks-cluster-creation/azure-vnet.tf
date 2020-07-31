#####################################################
# DO NOT Modify by hand - Managed by Automation
#####################################################
#####################################################
# This file can be used as a base template to build other Terraform files. It attempts to use as much
# Terraform interprolation as possible by creating Terraform variables instead of changing inline
# this approach provides an easier way to do creative looping, fetch IDs of created resources etc.
#####################################################
#####################################################
#####################################################

resource "azurerm_virtual_network" "vnet" {
  count = "${var.existing_vnet_subnet_id != "" ? 0 : 1}"
  name                = "${var.prefix}-network-aks"
  address_space       = "${var.vnet_address_space}"
  resource_group_name = azurerm_resource_group.aks-rg[0].name
  location            = azurerm_resource_group.aks-rg[0].location
}