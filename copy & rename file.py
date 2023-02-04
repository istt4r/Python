from pathlib import Path
import shutil
import re

def copy_and_rename_file(root_dir, dest_dir):
    root = Path(root_dir)
    log_path = Path(dest_dir) / "Log.txt"

    with open(log_path, "w", encoding="utf-8") as log:
        for path in root.rglob('*.csv'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    print(f"Reading content from: {path}")  # Debugging statement
                    content = f.read()
                    date_match = re.search(r'[A-Za-z]+ \d{1,2}, \d{4}', content)
                    if date_match:
                        date = date_match.group(0)
                        print(f"Date: {date}")  # Debugging statement
                        
                        date_parts = date.split()
                        month = date_parts[0]
                        
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

                        # Use the get method to get the numerical value for the month
                        month_num = month_map.get(month, "")
                        day = date_parts[1].strip(',')
                        year = date_parts[2]
                        format_date = f"{year}_{month_num}_{day}"
                        print(f"Format_Date: {format_date}")  # Debugging statement
                                            
                        session_match = re.search(r'(back|biceps|chest|deltoid|forearm|triceps|abdominals|legs one|legs two|push one|push two|pull one|pull two)', path.name, re.IGNORECASE)
                        print(f"Session_Match: {session_match}")  # Debugging statement
                        
                        if session_match:
                            session = session_match.group(0)
                            new_filename = format_date + ": " + session + ".csv"
                            notion_export_id = path.name.split('_')[-1]
                            
                            dest_path = Path(dest_dir)
                            dest_file_path = dest_path / new_filename
                            if not dest_file_path.exists():
                                shutil.copy2(path, dest_file_path)
                                print(f"Copied {path.name} to {dest_file_path}")
                                log.write(f"{format_date},{notion_export_id}\n")
            except FileNotFoundError as e:
                print(f"Error: {e}")

root_dir = r'C:/Users/jecla/OneDrive/Desktop/Notion/Feb 2,2023'
dest_dir = r'C:/Users/jecla/OneDrive/Desktop/Notion/Archive'
copy_and_rename_file(root_dir, dest_dir)
