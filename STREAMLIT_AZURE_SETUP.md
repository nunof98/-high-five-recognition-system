# Streamlit App on Azure Container Apps - Setup Guide

Complete step-by-step guide to deploy the High Five Recognition System using Streamlit on Azure Container Apps.

## 📋 Prerequisites

-   Azure subscription
-   Docker Desktop installed
-   Azure CLI installed
-   Python 3.11+ (for local testing)
-   Git

## 🚀 Step 1: Install Required Tools

### Install Docker Desktop

Download from: https://www.docker.com/products/docker-desktop

### Install Azure CLI

Windows: Download from https://aka.ms/installazurecliwindows

Verify installation:

```bash
az --version
docker --version
```

### Install Python Dependencies (for local testing)

```bash
cd streamlit-app
pip install -r requirements.txt
```

## 🔧 Step 2: Create Azure Resources

### 2.1 Create App Registration (Same as Before)

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **"+ New registration"**

    - Name: `HighFiveRecognition`
    - Supported account types: **"Accounts in this organizational directory only"**
    - Click **Register**

4. **📋 Copy these values**:

    - **Application (client) ID** → Your `CLIENT_ID`
    - **Directory (tenant) ID** → Your `TENANT_ID`

5. **Create a client secret:**

    - Go to **Certificates & secrets** → **Client secrets**
    - Click **"+ New client secret"**
    - Description: `HighFive Secret`
    - Expires: 12 months
    - Click **Add**
    - **⚠️ Copy the "Value" immediately** → Your `CLIENT_SECRET`

6. **Add API permissions:**
    - Go to **API permissions**
    - Click **"+ Add a permission"**
    - Choose **Microsoft Graph** → **Application permissions**
    - Add:
        - ✅ `Sites.ReadWrite.All`
        - ✅ `Files.ReadWrite.All`
    - Click **Add permissions**
    - Click **"✓ Grant admin consent"**

### 2.2 Get SharePoint IDs (Same as Before)

Use [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer):

**Get Site ID:**

```
GET https://graph.microsoft.com/v1.0/sites/{tenant}.sharepoint.com:/sites/{site-name}
```

**Get Drive ID:**

```
GET https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives
```

**Get File ID:**

```
GET https://graph.microsoft.com/v1.0/sites/{SITE_ID}/drives/{DRIVE_ID}/root/children
```

## 🧪 Step 3: Test Locally

### 3.1 Set Environment Variables

Create `.env` file in `streamlit-app` folder:

```bash
cd /c/M_BDO2/high-five-recognition-system/streamlit-app
cp .env.example .env
```

Edit `.env` with your values:

```bash
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
SHAREPOINT_SITE_ID=your-site-id
SHAREPOINT_DRIVE_ID=your-drive-id
SHAREPOINT_FILE_ID=your-file-id
SHAREPOINT_TABLE_NAME=SuccessesTable
```

### 3.2 Run Locally

```bash
# Load environment variables (Windows Git Bash)
export $(cat .env | xargs)

# Or on Windows PowerShell
Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }

# Run Streamlit app
streamlit run app.py
```

### 3.3 Test with Sample URL

Open browser to:

```
http://localhost:8501?token=TEST001&color=orange
```

Test the form and verify data appears in SharePoint Excel!

## 🐳 Step 4: Build Docker Image

### 4.1 Build the Image

```bash
cd /c/M_BDO2/high-five-recognition-system/streamlit-app

# Build Docker image
docker build -t highfive-streamlit:latest .
```

### 4.2 Test Docker Container Locally

```bash
# Run container with environment variables
docker run -p 8501:8501 \
  -e TENANT_ID="your-tenant-id" \
  -e CLIENT_ID="your-client-id" \
  -e CLIENT_SECRET="your-client-secret" \
  -e SHAREPOINT_SITE_ID="your-site-id" \
  -e SHAREPOINT_DRIVE_ID="your-drive-id" \
  -e SHAREPOINT_FILE_ID="your-file-id" \
  -e SHAREPOINT_TABLE_NAME="SuccessesTable" \
  highfive-streamlit:latest
```

Test at: `http://localhost:8501?token=TEST002&color=blue`

## ☁️ Step 5: Deploy to Azure

### 5.1 Login to Azure

```bash
az login
```

### 5.2 Create Resource Group

```bash
az group create \
  --name rg-highfive-streamlit \
  --location westeurope
```

### 5.3 Create Azure Container Registry

```bash
# Create registry (Basic tier is cheapest)
az acr create \
  --resource-group rg-highfive-streamlit \
  --name highfiveregistry \
  --sku Basic \
  --admin-enabled true

# Get registry credentials
az acr credential show --name highfiveregistry
```

**📋 Save the username and password!**

### 5.4 Push Image to Azure Container Registry

```bash
# Login to ACR
az acr login --name highfiveregistry

# Tag image for ACR
docker tag highfive-streamlit:latest highfiveregistry.azurecr.io/highfive-streamlit:latest

# Push to ACR
docker push highfiveregistry.azurecr.io/highfive-streamlit:latest
```

### 5.5 Create Azure Container Apps Environment

```bash
# Install Container Apps extension
az extension add --name containerapp --upgrade

# Create environment
az containerapp env create \
  --name highfive-env \
  --resource-group rg-highfive-streamlit \
  --location westeurope
```

### 5.6 Create Container App

```bash
az containerapp create \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --environment highfive-env \
  --image highfiveregistry.azurecr.io/highfive-streamlit:latest \
  --target-port 8501 \
  --ingress external \
  --registry-server highfiveregistry.azurecr.io \
  --registry-username <USERNAME_FROM_STEP_5.3> \
  --registry-password <PASSWORD_FROM_STEP_5.3> \
  --cpu 0.25 \
  --memory 0.5Gi \
  --min-replicas 0 \
  --max-replicas 3 \
  --env-vars \
    "TENANT_ID=your-tenant-id" \
    "CLIENT_ID=your-client-id" \
    "CLIENT_SECRET=secretref:client-secret" \
    "SHAREPOINT_SITE_ID=your-site-id" \
    "SHAREPOINT_DRIVE_ID=your-drive-id" \
    "SHAREPOINT_FILE_ID=your-file-id" \
    "SHAREPOINT_TABLE_NAME=SuccessesTable" \
  --secrets \
    "client-secret=your-client-secret"
```

**Important:** Replace the placeholder values with your actual IDs!

### 5.7 Get Your App URL

```bash
az containerapp show \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

Your app URL will be something like:

```
https://highfive-app.xxxxxx.westeurope.azurecontainerapps.io
```

## 📱 Step 6: Generate QR Codes

Create QR codes with your Container App URL:

```
https://highfive-app.xxxxxx.westeurope.azurecontainerapps.io?token=ABC001&color=orange
https://highfive-app.xxxxxx.westeurope.azurecontainerapps.io?token=ABC002&color=blue
https://highfive-app.xxxxxx.westeurope.azurecontainerapps.io?token=ABC003&color=green
```

Use any QR code generator:

-   https://www.qr-code-generator.com/
-   https://qr.io/
-   https://www.qrcode-monkey.com/

## 🔄 Step 7: Update and Redeploy

When you make changes to your app:

```bash
# Rebuild image
cd /c/M_BDO2/high-five-recognition-system/streamlit-app
docker build -t highfive-streamlit:latest .

# Tag and push
docker tag highfive-streamlit:latest highfiveregistry.azurecr.io/highfive-streamlit:latest
docker push highfiveregistry.azurecr.io/highfive-streamlit:latest

# Update Container App
az containerapp update \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --image highfiveregistry.azurecr.io/highfive-streamlit:latest
```

## 💰 Cost Management

### Pricing Breakdown

**Azure Container Registry (Basic):**

-   $5/month for 10 GB storage
-   Includes unlimited image pulls

**Azure Container Apps (Consumption):**

-   First 180,000 vCPU-seconds: Free
-   First 360,000 GiB-seconds: Free
-   After free tier: ~$0.000012/vCPU-second

**Estimated monthly cost:**

-   ACR: $5/month
-   Container Apps: $0-2/month (with scale to zero)
-   **Total: ~$5-7/month**

### Enable Scale to Zero

Your app already scales to 0 (`--min-replicas 0`), meaning:

-   ✅ No cost when not in use
-   ✅ Automatic scale-up when accessed
-   ✅ Cold start time: ~5-10 seconds

### Monitor Costs

```bash
# Check resource usage
az containerapp show \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --query properties.configuration.ingress.fqdn

# View logs
az containerapp logs show \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --follow
```

## 🔒 Security Best Practices

### 1. Use Secrets for Sensitive Data

Store sensitive values in Container App secrets:

```bash
az containerapp secret set \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --secrets \
    "client-secret=your-new-secret"
```

### 2. Enable Managed Identity (Optional, Advanced)

Instead of client secrets, use managed identity:

```bash
az containerapp identity assign \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --system-assigned
```

Then grant SharePoint permissions to the managed identity.

### 3. Restrict Ingress

Add authentication if needed:

```bash
az containerapp ingress enable \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --type external \
  --allow-insecure false
```

## 🔍 Troubleshooting

### App not starting?

Check logs:

```bash
az containerapp logs show \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --follow
```

### Environment variables not set?

List current environment variables:

```bash
az containerapp show \
  --name highfive-app \
  --resource-group rg-highfive-streamlit \
  --query properties.template.containers[0].env
```

### SharePoint access denied?

Verify:

1. App Registration has correct permissions
2. Admin consent was granted
3. SharePoint IDs are correct
4. Client secret hasn't expired

### Container won't pull?

Check registry credentials:

```bash
az acr credential show --name highfiveregistry
```

## 📊 Monitoring

### View Application Insights

```bash
# Enable Application Insights
az containerapp env show \
  --name highfive-env \
  --resource-group rg-highfive-streamlit
```

### Check Replica Count

```bash
az containerapp replica list \
  --name highfive-app \
  --resource-group rg-highfive-streamlit
```

### View Metrics

Go to Azure Portal → Container Apps → highfive-app → Metrics

Key metrics to monitor:

-   Request count
-   Response time
-   CPU usage
-   Memory usage
-   Replica count

## 🚀 CI/CD with GitHub Actions (Optional)

Create `.github/workflows/deploy-streamlit.yml`:

```yaml
name: Deploy Streamlit to Azure

on:
    push:
        branches: [main]
        paths:
            - "streamlit-app/**"

jobs:
    build-and-deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v3

            - name: Login to Azure
              uses: azure/login@v1
              with:
                  creds: ${{ secrets.AZURE_CREDENTIALS }}

            - name: Build and push Docker image
              run: |
                  cd streamlit-app
                  az acr build \
                    --registry highfiveregistry \
                    --image highfive-streamlit:${{ github.sha }} \
                    --image highfive-streamlit:latest \
                    .

            - name: Update Container App
              run: |
                  az containerapp update \
                    --name highfive-app \
                    --resource-group rg-highfive-streamlit \
                    --image highfiveregistry.azurecr.io/highfive-streamlit:latest
```

## 📚 Useful Commands

```bash
# View app URL
az containerapp show -n highfive-app -g rg-highfive-streamlit --query properties.configuration.ingress.fqdn

# Restart app
az containerapp revision restart -n highfive-app -g rg-highfive-streamlit

# Scale manually
az containerapp update -n highfive-app -g rg-highfive-streamlit --min-replicas 1 --max-replicas 5

# Delete all resources (cleanup)
az group delete --name rg-highfive-streamlit --yes
```

## ✅ Advantages of Streamlit Approach

| Feature               | Static Web Apps + API     | **Streamlit on Container Apps** |
| --------------------- | ------------------------- | ------------------------------- |
| **Code Simplicity**   | ~500 lines (JS + Node.js) | **~200 lines (Python only)** ✅ |
| **Languages**         | HTML/CSS/JS + Node.js     | **Python only** ✅              |
| **UI Development**    | Manual HTML/CSS           | **Built-in components** ✅      |
| **Form Handling**     | Manual validation         | **Automatic** ✅                |
| **Deployment**        | GitHub Actions            | **Docker** ✅                   |
| **Local Testing**     | `swa start`               | **`streamlit run`** ✅          |
| **Cost**              | Free                      | **$5-7/month**                  |
| **Scaling**           | Automatic                 | **0 to N replicas** ✅          |
| **Session State**     | Manual                    | **Built-in** ✅                 |
| **Real-time Updates** | Manual refresh            | **Automatic rerun** ✅          |

## 🎓 Additional Resources

-   [Streamlit Documentation](https://docs.streamlit.io/)
-   [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
-   [Docker Documentation](https://docs.docker.com/)
-   [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/)

---

**🎉 Congratulations!** Your Streamlit High Five Recognition System is now running on Azure Container Apps!
