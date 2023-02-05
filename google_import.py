import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials
from config import CREDENTIALS, DEST_DIR

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

client = gspread.authorize(credentials)

spreadsheet = client.open("Notion Fitness CSV Import")

starting_cell = "A1"


# root_dir - root directory of .csv files to be uploaded
# spreadsheet - a gspread.Spreadsheet object 
# cell - desired cell (row/column) to insert data when uploading to spreadsheet
#  ex: 'A1', 'MySheet!C3', etc.

def import_csv(root_dir, sheet, cell):   
    if '!' in cell:
        (tabName, cell) = cell.split('!')
        wks = sheet.worksheet(tabName)
    else:
        wks = sheet.sheet1
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)
    
    root = Path(root_dir)

    # reading all .csv files, and appending the successive text to content_data
    content_data = ""
    for path in root.rglob('*.csv'):
        with open(path, 'r', encoding='utf-8') as f:
            print(f"Path: {path}")
            content_data += f.read() + "\n"
        
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": wks.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": content_data,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }
    sheet.batch_update(body)
    

import_csv(DEST_DIR, spreadsheet, starting_cell)