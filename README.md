# High Five Recognition System

A QR code-based recognition system.

## 🎯 Features

-   🎫 QR code scanning with unique token and color parameters
-   ✅ Token validation (checks if token has been used before)
-   💬 Recognition message submission form
-   📊 CSV-based storage
-   🔐 Admin dashboard with password protection
-   📥 Download data as CSV or Excel
-   📈 Statistics and analytics
-   📱 Mobile-responsive design

## 🚀 Quick Start

### Run Locally

````bash
# Create a virtual environment
uv venv

```bash
# Install dependencies
uv sync

# Set admin password in .streamlit/secrets.toml
echo 'ADMIN_PASSWORD = "your-password"' > .streamlit/secrets.toml

# Run the app
streamlit run streamlit-app/app.py

# Test it
# User: http://localhost:8501?token=TEST001&color=blue
# Admin: http://localhost:8501?admin
````

## 📋 How It Works

### For Users (QR Code Recipients)

1. **Scan QR code** on token
2. **Read existing message** (if token already used) OR **Submit new message**
3. **Enter name and message**
4. **Submit** - Token is now marked as used

### For Admins

1. **Access admin dashboard**
2. **Enter password**
3. **View all submissions**, download data, see statistics

## 🎨 QR Code Format

Generate QR codes with this URL format:

```
https://highfive.streamlit.app?token=UNIQUE_TOKEN&color=COLOR_NAME
```

**Examples:**

```
https://highfive.streamlit.app?token=ABC123&color=orange
https://highfive.streamlit.app?token=DEF456&color=blue
https://highfive.streamlit.app?token=TEAM2025-001&color=green
```

**Admin Access:**

```
https://highfive.streamlit.app?token=admin&color=admin
https://highfive.streamlit.app?admin
```

## 🎨 Supported Colors

-   red (#e74c3c)
-   blue (#3498db)
-   green (#2ecc71)
-   yellow (#f39c12)
-   purple (#9b59b6)
-   orange (#FF9900)

## 📄 License

MIT License - Feel free to use and modify for your organization!
