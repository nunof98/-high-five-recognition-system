# Outputs for High Five Recognition System

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.main.name
}

output "acr_login_server" {
  description = "Login server for Azure Container Registry"
  value       = azurerm_container_registry.acr.login_server
}

output "acr_name" {
  description = "Name of the Azure Container Registry"
  value       = azurerm_container_registry.acr.name
}

output "webapp_name" {
  description = "Name of the Web App"
  value       = azurerm_linux_web_app.webapp.name
}

output "webapp_url" {
  description = "URL of the deployed web application"
  value       = "https://${azurerm_linux_web_app.webapp.default_hostname}"
}

output "webapp_identity_principal_id" {
  description = "Principal ID of the Web App's managed identity"
  value       = azurerm_linux_web_app.webapp.identity[0].principal_id
}

output "app_service_plan_id" {
  description = "ID of the App Service Plan"
  value       = azurerm_service_plan.plan.id
}
