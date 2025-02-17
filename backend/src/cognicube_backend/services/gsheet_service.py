import gspread
from google.oauth2.service_account import Credentials

def get_gsheet_client():
    """获取Google Sheets客户端"""
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('your-google-creds.json', scopes=scope)
    return gspread.auth.authorize(creds)

def add_user_to_sheet(email: str):
    """将用户添加到Google Sheet"""
    client = get_gsheet_client()
    sheet = client.open("YourSpreadsheetName").sheet1
    sheet.append_row([email])
    print(f"Email {email} added to Google Sheet.")
