# High Five Recognition System - Terraform Configuration

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = var.tags
}

# Container Registry
resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = false

  tags = var.tags
}

# App Service Plan (Linux)
resource "azurerm_service_plan" "plan" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = var.app_service_sku

  tags = var.tags
}

# Web App for Containers
resource "azurerm_linux_web_app" "webapp" {
  name                = var.webapp_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.plan.id

  site_config {
    always_on = true

    application_stack {
      docker_image_name   = "${azurerm_container_registry.acr.login_server}/${var.docker_image_name}:${var.docker_image_tag}"
      docker_registry_url = "https://${azurerm_container_registry.acr.login_server}"
    }

    health_check_path = "/_stcore/health"
  }

  app_settings = {
    WEBSITES_PORT                      = "8501"
    DOCKER_REGISTRY_SERVER_URL         = "https://${azurerm_container_registry.acr.login_server}"
    DOCKER_ENABLE_CI                   = "true"
    TENANT_ID                          = var.tenant_id
    CLIENT_ID                          = var.client_id
    CLIENT_SECRET                      = var.client_secret
    SHAREPOINT_SITE_ID                 = var.sharepoint_site_id
    SHAREPOINT_DRIVE_ID                = var.sharepoint_drive_id
    SHAREPOINT_FILE_ID                 = var.sharepoint_file_id
    SHAREPOINT_TABLE_NAME              = var.sharepoint_table_name
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags

  depends_on = [
    azurerm_container_registry.acr,
    azurerm_service_plan.plan
  ]
}

# Assign AcrPull role to Web App's managed identity
resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_linux_web_app.webapp.identity[0].principal_id
}
