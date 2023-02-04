from pathlib import Path
import shutil
import re

from config import ROOT_DIR, DEST_DIR

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


def archive_workout(root_dir, dest_dir):
    root = Path(root_dir)
    log_path = Path(dest_dir) / "Log.txt"

    with open(log_path, "w", encoding="utf-8") as log:
        for path in root.rglob('*.csv'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    print(f"\nReading content from: {path}")
                    content = f.read()
                    date_match = re.search(r'[A-Za-z]+ \d{1,2}, \d{4}', content)
                    if date_match:
                        format_date = format_date_string(date_match)
                        print(f"Date: {format_date}")
                                            
                        session_match = re.search(r'^(.*?)\b[0-9a-f]{32}\b', path.name, re.IGNORECASE)
                        print(f"Session_Match: {session_match}")
                        
                        if session_match:
                            session = session_match.group(1)
                            new_filename = format_date + " - " + session + ".csv"
                            notion_export_id = path.name.split('_')[-1]
                            dest_path = Path(dest_dir)
                            dest_file_path = dest_path / new_filename
                            if not dest_file_path.exists():
                                shutil.copy2(path, dest_file_path)
                                print(f"Copied {path.name} to {dest_file_path}")
                                log.write(f"{format_date},{notion_export_id}\n")
            except FileNotFoundError as e:
                print(f"Error: {e}")

root_dir = ROOT_DIR
dest_dir = DEST_DIR

archive_workout(root_dir, dest_dir)
