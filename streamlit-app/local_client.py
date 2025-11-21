import pandas as pd
import os
from datetime import datetime

EXCEL_FILE = "HighFiveSuccesses.xlsx"

class LocalClient:
    def __init__(self):
        if not os.path.exists(EXCEL_FILE):
            # Create a new file with headers if it doesn't exist
            df = pd.DataFrame(columns=["Token", "Color", "Message", "SubmittedBy", "Timestamp"])
            df.to_excel(EXCEL_FILE, index=False)

    def check_token(self, token):
        df = pd.read_excel(EXCEL_FILE)
        row = df[df["Token"] == token]
        if not row.empty:
            return row.iloc[0].to_dict()
        return None

    def add_token(self, token, color, message, submitted_by):
        df = pd.read_excel(EXCEL_FILE)
        if token in df["Token"].values:
            return False
        new_row = {
            "Token": token,
            "Color": color,
            "Message": message,
            "SubmittedBy": submitted_by,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return True
