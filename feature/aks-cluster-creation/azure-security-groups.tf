resource "azurerm_subnet_network_security_group_association" "aks-nsg-association" {
  count = "${var.existing_vnet_subnet_id != "" ? 0 : 1}"
  subnet_id                 = "${azurerm_subnet.subnet[0].id}"
  network_security_group_id = "${azurerm_network_security_group.security_group_epiphany[0].id}"
}
resource azurerm_network_security_group "security_group_epiphany" {
  count = "${var.existing_vnet_subnet_id != "" ? 0 : 1}"
  name                = "aks-1-nsg"
  location            = "${azurerm_resource_group.aks-rg[0].location}"
  resource_group_name = "${azurerm_resource_group.aks-rg[0].name}"

   security_rule {
    name                        = "ssh"
    description                 = "Allow SSH"
    priority                    = 100
    direction                   = "Inbound"
    access                      = "Allow"
    protocol                    = "Tcp"
    source_port_range           = "*"
    destination_port_range      = "22"
    source_address_prefix       = "0.0.0.0/0"
    destination_address_prefix  = "0.0.0.0/0"
  }
}
