
# Azure Resource Manager provider
# https://www.terraform.io/docs/providers/azurerm/index.html
provider "azurerm" {
  version = ">= 2.15.0"
  features {}
}

terraform { 
	required_version = ">= 0.12" 
	}