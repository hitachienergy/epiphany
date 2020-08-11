resource "azurerm_resource_group" "aks-rg" {
    count = var.existing_resource_group_name != "" ? 0 : 1
    name     = "${var.prefix}-rg"
    location = var.location
}
