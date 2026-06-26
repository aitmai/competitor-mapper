"""
Reads startup data from Google Sheets "Competitor-Input"
"""
import gspread
from google.oauth2.service_account import Credentials


def get_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds  = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    return gspread.authorize(creds)


def load_startups():
    client = get_client()
    sheet  = client.open("Competitor-Input").sheet1
    rows   = sheet.get_all_records()

    startups = []
    for row in rows:
        if not row.get("Company Name"):
            continue
        startups.append({
            "company_name": str(row.get("Company Name", "")),
            "sector":       str(row.get("Sector", "")),
            "description":  str(row.get("Description", "")),
            "website":      str(row.get("Website", "")),
            "stage":        str(row.get("Stage", "")),
        })

    return startups
