import gspread
from pathlib import Path
from google.oauth2.service_account import Credentials
from config import CREDENTIALS, CSV_TEST, ROOT_DIR

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
content_file = r"C:/Users/jecla/OneDrive/Desktop/FitExport/Content.txt"
staging_file = r"C:/Users/jecla/OneDrive/Desktop/FitExport/Staging.txt"

def import_csv(root_dir, sheet, cell):
    '''
    path - root directory of .csv files to be uploaded
    sheet - a gspread.Spreadsheet object
    cell - string giving starting cell, optionally including sheet/tab name
      ex: 'A1', 'MySheet!C3', etc.
    '''    
    if '!' in cell:
        (tabName, cell) = cell.split('!')
        wks = sheet.worksheet(tabName)
    else:
        wks = sheet.sheet1
    (firstRow, firstColumn) = gspread.utils.a1_to_rowcol(cell)
    print(f"firstRow, firstColumn: {firstRow}, {firstColumn}")
    
    root = Path(root_dir)

    content_data = ""
    for path in root.rglob('*.csv'):
        with open(path, 'r', encoding='utf-8') as f:
            print(f"Path: {path}")
            content_data += f.read() + "\n"

    # writing to the content_file
    with open(content_file, "w", encoding='utf-8') as content:
        content.write(content_data)
            
    with open(staging_file, "w", encoding='utf-8') as staging:
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
        staging.write(f"{body}\n")
        print(f"Body: {body}")
        sheet.batch_update(body)
    

import_csv(ROOT_DIR, spreadsheet, starting_cell)