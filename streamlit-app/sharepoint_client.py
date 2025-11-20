import os
import requests
from datetime import datetime
from typing import Optional, Dict, List


class SharePointClient:
    """Client for interacting with SharePoint Excel via Microsoft Graph API"""

    def __init__(self):
        """Initialize SharePoint client with environment variables"""
        self.tenant_id = os.getenv("TENANT_ID")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.site_id = os.getenv("SHAREPOINT_SITE_ID")
        self.drive_id = os.getenv("SHAREPOINT_DRIVE_ID")
        self.file_id = os.getenv("SHAREPOINT_FILE_ID")
        self.table_name = os.getenv("SHAREPOINT_TABLE_NAME", "SuccessesTable")

        self._validate_config()
        self.access_token = None

    def _validate_config(self):
        """Validate that all required environment variables are set"""
        required_vars = [
            "TENANT_ID",
            "CLIENT_ID",
            "CLIENT_SECRET",
            "SHAREPOINT_SITE_ID",
            "SHAREPOINT_DRIVE_ID",
            "SHAREPOINT_FILE_ID",
        ]

        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

    def _get_access_token(self) -> str:
        """Get access token from Azure AD"""
        if self.access_token:
            return self.access_token

        token_url = (
            f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        )

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }

        try:
            response = requests.post(token_url, data=data, timeout=10)
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get access token: {str(e)}")

    def _make_graph_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict:
        """Make a request to Microsoft Graph API"""
        token = self._get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        url = f"https://graph.microsoft.com/v1.0{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Graph API request failed: {str(e)}")

    def _get_table_rows(self) -> List[Dict]:
        """Get all rows from SharePoint Excel table"""
        endpoint = f"/sites/{self.site_id}/drives/{self.drive_id}/items/{self.file_id}/workbook/tables/{self.table_name}/rows"

        result = self._make_graph_request("GET", endpoint)

        # Transform rows into list of dictionaries
        rows = []
        for row in result.get("value", []):
            values = row["values"][0]  # Get the first (and only) row array
            rows.append(
                {
                    "TokenID": values[0],
                    "Color": values[1],
                    "Message": values[2],
                    "SubmittedBy": values[3],
                    "Timestamp": values[4],
                }
            )

        return rows

    def check_token(self, token: str) -> Optional[Dict]:
        """
        Check if a token exists in SharePoint

        Args:
            token: The token ID to check

        Returns:
            Dictionary with token data if found, None otherwise
        """
        try:
            rows = self._get_table_rows()

            # Find matching token
            for row in rows:
                if row["TokenID"] == token:
                    return row

            return None
        except Exception as e:
            raise Exception(f"Error checking token: {str(e)}")

    def add_token(
        self, token: str, color: str, message: str, submitted_by: str
    ) -> bool:
        """
        Add a new token to SharePoint

        Args:
            token: The token ID
            color: The token color
            message: The recognition message
            submitted_by: Name of person submitting

        Returns:
            True if successful, False if token already exists
        """
        try:
            # Check if token already exists
            existing = self.check_token(token)
            if existing:
                return False

            # Add new row
            endpoint = f"/sites/{self.site_id}/drives/{self.drive_id}/items/{self.file_id}/workbook/tables/{self.table_name}/rows"

            timestamp = datetime.now().isoformat()

            data = {"values": [[token, color, message, submitted_by, timestamp]]}

            self._make_graph_request("POST", endpoint, data)
            return True

        except Exception as e:
            raise Exception(f"Error adding token: {str(e)}")
