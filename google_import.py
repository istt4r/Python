import gspread
from google.oauth2.service_account import Credentials
from config import CREDENTIALS

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(
    CREDENTIALS,
    scopes=scope
)

Client = gspread.authorize(credentials)

sh = Client.open("Notion Fitness CSV Import")

print(sh.sheet1.get('A1'))