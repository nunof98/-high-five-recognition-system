# High Five Recognition System - Terraform Infrastructure

This directory contains Terraform configuration for deploying the High Five Recognition System to Azure.

## Prerequisites

1. **Install Terraform** (v1.0+)

    - [Download Terraform](https://www.terraform.io/downloads)
    - Verify: `terraform --version`

2. **Azure CLI** (already installed)

    - Login: `az login`
    - Set subscription: `az account set --subscription <subscription-id>`

3. **Docker Image** must be built and pushed to ACR
    ```bash
    az acr build --registry highfiverecognitionacr --image highfiverecognition:latest --file docker/Dockerfile .
    ```

## Setup

### 1. Create `terraform.tfvars`

Copy the example file and fill in your Azure credentials:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and add your actual values:

-   `tenant_id`
-   `client_id`
-   `client_secret`

### 2. Initialize Terraform

```bash
cd terraform
terraform init
```

This downloads the Azure provider and initializes the backend.

### 3. Review the Plan

```bash
terraform plan
```

This shows what resources will be created without actually creating them.

### 4. Apply the Configuration

```bash
terraform apply
```

Type `yes` when prompted. This will create:

-   Resource Group
-   Azure Container Registry
-   App Service Plan
-   Web App (Linux with Docker)
-   Managed Identity
-   Role Assignment (ACR Pull)

### 5. Get Outputs

After deployment, view the outputs:

```bash
terraform output
```

You'll see:

-   `webapp_url`: Your app's public URL
-   `acr_login_server`: Container registry URL
-   `webapp_identity_principal_id`: Managed identity ID

## Usage

### Update Infrastructure

If you change any `.tf` files:

```bash
terraform plan    # Review changes
terraform apply   # Apply changes
```

### Destroy Infrastructure

To delete all resources:

```bash
terraform destroy
```

⚠️ **Warning:** This will permanently delete all resources!

## File Structure

```
terraform/
├── main.tf                    # Main infrastructure definition
├── variables.tf               # Variable declarations
├── outputs.tf                 # Output values
├── terraform.tfvars.example   # Example variables file
├── terraform.tfvars           # Your actual values (gitignored)
├── .gitignore                 # Terraform-specific gitignore
└── README.md                  # This file
```

## Important Notes

### Security

-   `terraform.tfvars` is gitignored and contains sensitive credentials
-   Never commit actual credentials to version control
-   Consider using Azure Key Vault for production secrets

### Cost Management

-   Default SKU is B1 (~$13/month)
-   Change `app_service_sku` in `terraform.tfvars` to scale up/down
-   Use `terraform destroy` when not in use to avoid costs

### Continuous Deployment

After initial deployment, push new images to ACR:

```bash
# Build and push new version
az acr build --registry highfiverecognitionacr --image highfiverecognition:latest --file docker/Dockerfile .

# Web App will automatically pull the new image (DOCKER_ENABLE_CI is enabled)
```

## Troubleshooting

### Authentication Issues

```bash
# Ensure you're logged in
az login
az account show

# Set the correct subscription
az account set --subscription <subscription-id>
```

### State Lock Issues

If Terraform gets stuck:

```bash
terraform force-unlock <lock-id>
```

### Verify Resources

```bash
# List all resources in the resource group
az resource list --resource-group highfiverecognition-rg --output table
```

## Next Steps

1. Access your app at the `webapp_url` from outputs
2. Test the QR code functionality
3. Monitor logs in Azure Portal
4. Set up custom domain (optional)
5. Configure SSL certificate (optional)

## Support

For issues or questions, refer to:

-   [Terraform Azure Provider Docs](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
-   [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
