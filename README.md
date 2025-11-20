# High Five Recognition System

A QR code-based token validation system with SharePoint integration for employee recognition.

## 🎯 Features

-   QR code scanning with unique token and color parameters
-   Token validation (checks if token has been used before)
-   Recognition message submission form
-   SharePoint Excel backend storage
-   Streamlit web application (Python-based)
-   Azure Container Apps hosting (serverless with scale-to-zero)

## 📋 Setup Instructions

### Quick Start

**For detailed step-by-step instructions, see [STREAMLIT_AZURE_SETUP.md](STREAMLIT_AZURE_SETUP.md)**

### 1. SharePoint Setup

1. Create a new Excel workbook in SharePoint named `HighFiveSuccesses.xlsx`
2. Add the following columns:
    - TokenID (Text)
    - Color (Text)
    - Message (Text)
    - SubmittedBy (Text)
    - Timestamp (Date)
3. Format the data as a Table and name it "SuccessesTable"

### 2. Build and Test Locally

1. **Install Python dependencies** from `streamlit-app/requirements.txt`
2. **Set environment variables** with your Azure/SharePoint IDs
3. **Run locally**: `streamlit run streamlit-app/app.py`
4. **Test with sample QR parameters**: `?token=TEST001&color=orange`

### 3. Deploy to Azure Container Apps

1. **Build Docker image** from Streamlit app
2. **Push to Azure Container Registry**
3. **Create Container App** with environment variables
4. **Enable scale-to-zero** for cost savings

### 4. Generate QR Codes

Create QR codes with your Container App URL:
const CONFIG = {
checkTokenUrl:
"https://YOUR-FUNCTION-APP.azurewebsites.net/api/checktoken?code=YOUR_KEY",
submitTokenUrl:
"https://YOUR-FUNCTION-APP.azurewebsites.net/api/submittoken?code=YOUR_KEY",
};

```

### 4. Generate QR Codes

Create QR codes with your Static Web App URL:

```

https://your-app.azurestaticapps.net?token=ABC123&color=red
https://your-app.azurestaticapps.net?token=DEF456&color=blue

```

## 🎨 Supported Colors

-   red
-   blue
-   green
-   yellow
-   purple
-   orange

## 💰 Cost

-   Azure Container Registry (Basic): **$5/month**
-   Azure Container Apps (Consumption with scale-to-zero): **$0-2/month**
-   SharePoint Excel: **Included with O365**
-   **Total: ~$5-7/month** ✅ Well under budget!

## 🔒 Security Notes

-   API routes secured via Azure AD App Registration
-   Microsoft Graph API authentication for SharePoint access
-   Duplicate token prevention built-in
-   Environment variables stored securely in Azure
-   Automatic HTTPS with free SSL certificate

## 📱 Usage

1. User scans QR code
2. Website checks if token exists
3. If exists: Shows previous message
4. If new: Shows form to submit recognition
5. Data saved to SharePoint Excel

## 🛠️ Tech Stack

-   **Streamlit** (Python Web Framework)
-   **Azure Container Apps** (Serverless Container Hosting)
-   **Docker** (Containerization)
-   **Microsoft Graph API** (SharePoint Integration)
-   **SharePoint Excel** (Data Storage)
-   **Azure Container Registry** (Image Storage)

## 📄 License

MIT License - Feel free to modify and use for your organization.
```
