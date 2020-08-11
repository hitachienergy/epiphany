resource "azurerm_virtual_network" "vnet" {
  count = var.existing_vnet_subnet_id != "" ? 0 : 1
  name                = "${var.prefix}-network-aks"
  address_space       = var.vnet_address_space
  resource_group_name = azurerm_resource_group.aks-rg[0].name
  location            = azurerm_resource_group.aks-rg[0].location
}
