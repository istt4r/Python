from pathlib import Path
import shutil
import re
from config import ROOT_DIR, DEST_DIR, ARCHIVE_LOG_PATH

# Create a dictionary to map month names to their numerical values
month_map = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

# Restructures default date format into: YYYY_MM_DD
def format_date_string(date_match):
    date = date_match.group(0)
    date_parts = date.split()
    month = date_parts[0]
    month_num = month_map.get(month, "") # Use the get method to get the numerical value for the month
    day = date_parts[1].strip(',')
    day = "0" + day if len(day) == 1 else day
    year = date_parts[2]
    format_date = f"{year}_{month_num}_{day}"
    return format_date

# Sorts the lines logged to Log.txt in order of descending date
def sort_log_file(log_path):
    with open(log_path, "r") as log:
        lines = log.readlines()
        
    lines = [line.strip().split(',') for line in lines]
    lines = sorted(lines, key=lambda x: x[0], reverse=True)
    lines = [','.join(line) + '\n' for line in lines]

    with open(log_path, "w") as log:
        log.writelines(lines)

# Explores directory for .csv files, extracts the date, renames the file, and copies it to an archive location.
def archive_workout(root_dir, dest_dir,log_path):
    root = Path(root_dir)
    
    with open(log_path, "w", encoding="utf-8") as log:
        for path in root.rglob('*.csv'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    print(f"\nReading content from: {path}")
                    content = f.read()
                    date_match = re.search(r'[A-Za-z]+ \d{1,2}, \d{4}', content)
                    if date_match:
                        format_date = format_date_string(date_match)                  
                        session_match = re.search(r'^(.*?)\b[0-9a-f]{32}\b', path.name, re.IGNORECASE)
                        print(f"Date: {format_date}, Session_Match: {session_match}")
                        
                        if session_match:
                            session = session_match.group(1)
                            new_filename = format_date + " - " + session + ".csv"
                            notion_export_id = path.name.split('_')[-1]
                            dest_path = Path(dest_dir)
                            dest_file_path = dest_path / new_filename
                            
                            if dest_file_path.exists():
                                print("File already exists")
                            else:
                                shutil.copy2(path, dest_file_path)
                                print(f"Copied {path.name} to {dest_file_path}")
                                log.write(f"{format_date},{notion_export_id}\n")
            except FileNotFoundError as e:
                print(f"Error: {e}")

archive_workout(ROOT_DIR, DEST_DIR,ARCHIVE_LOG_PATH)
sort_log_file(ARCHIVE_LOG_PATH)