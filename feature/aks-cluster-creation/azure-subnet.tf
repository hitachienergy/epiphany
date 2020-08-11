resource "azurerm_subnet" "subnet" {
  count = var.existing_vnet_subnet_id != "" ? 0 : 1
  name                 = "${var.prefix}-subnet-aks"
  address_prefixes     = var.aks_address_prefix
  resource_group_name  = azurerm_resource_group.aks-rg[0].name
  virtual_network_name = azurerm_virtual_network.vnet[0].name
}
