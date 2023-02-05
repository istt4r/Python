import gspread
from google.oauth2.service_account import Credentials
from config import CREDENTIALS, CSV_TEST

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

cell_start = "A3"


def import_csv(csv, sheet, cell):
    '''
    csv - path to csv file to upload
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

    with open(csv, 'r', encoding='utf-8') as f:
        csvContents = f.read()
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": wks.id,
                    "rowIndex": firstRow-1,
                    "columnIndex": firstColumn-1,
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }
    return sheet.batch_update(body)

import_csv(CSV_TEST, spreadsheet, cell_start)