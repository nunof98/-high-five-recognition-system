# Variables for High Five Recognition System

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "highfiverecognition-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "westeurope"
}

variable "acr_name" {
  description = "Name of the Azure Container Registry"
  type        = string
  default     = "highfiverecognitionacr"
}

variable "app_service_plan_name" {
  description = "Name of the App Service Plan"
  type        = string
  default     = "highfiverecognition-plan"
}

variable "app_service_sku" {
  description = "SKU for App Service Plan (B1, B2, S1, P1v2, etc.)"
  type        = string
  default     = "B1"
}

variable "webapp_name" {
  description = "Name of the Web App"
  type        = string
  default     = "highfiverecognition-app"
}

variable "docker_image_name" {
  description = "Docker image name"
  type        = string
  default     = "highfiverecognition"
}

variable "docker_image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

# SharePoint Configuration
variable "tenant_id" {
  description = "Azure AD Tenant ID"
  type        = string
  sensitive   = true
}

variable "client_id" {
  description = "Azure AD Application (Client) ID"
  type        = string
  sensitive   = true
}

variable "client_secret" {
  description = "Azure AD Application Client Secret"
  type        = string
  sensitive   = true
}

variable "sharepoint_site_id" {
  description = "SharePoint Site ID"
  type        = string
  default     = "bosch.sharepoint.com,22963e73-ce77-445e-b04d-652d263376f0,e7561372-dc50-4abe-9382-e7e79e3d39bb"
}

variable "sharepoint_drive_id" {
  description = "SharePoint Drive ID"
  type        = string
  default     = "b!cz6WInfOXkSwTWUtJjN28HITVudQ3L5Kk4Ln5549ObsleUFf3VU7Tr82fkrmo87c"
}

variable "sharepoint_file_id" {
  description = "SharePoint File ID"
  type        = string
  default     = "01WG5M6OEGGA5RYHIBMVBZYHH365GUTM3J"
}

variable "sharepoint_table_name" {
  description = "SharePoint Excel Table Name"
  type        = string
  default     = "SuccessesTable"
}

# Tags
variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "Production"
    Project     = "HighFiveRecognition"
    ManagedBy   = "Terraform"
  }
}
