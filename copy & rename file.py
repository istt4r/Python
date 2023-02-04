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
                        date_without_time = re.sub(r'\s+\d{1,2}:\d{2}\s[APM]+$', '', date)
                        if date_without_time:
                            date = date_without_time
                        else:
                            date = "Update_" + date
                        new_date = date.replace(", ", "_").replace(" ", "_")
                        session_match = re.search(r'(back|biceps|chest|deltoid|forearm|legs_1|legs_2|push_1|push_2|pull_1|pull_2|triceps|abdominals)', path.name)
                        if session_match:
                            session = session_match.group(0)
                            notion_export_id = path.name.split("_")[-1].split(".")[0]
                            new_filename = new_date + "_" + session + ".csv"
                            dest_path = Path(dest_dir)
                            dest_file_path = dest_path / new_filename
                            if not dest_file_path.exists():
                                shutil.copy2(path, dest_file_path)
                                print(f"Copied {path.name} to {dest_file_path}")
                                log.write(f"{new_date},{notion_export_id}\n")
            except FileNotFoundError as e:
                print(f"Error: {e}")

root_dir = r'C:/Users/jecla/OneDrive/Desktop/Notion/Feb 2,2023'
dest_dir = r'C:/Users/jecla/OneDrive/Desktop/Notion/Archive'
copy_and_rename_file(root_dir, dest_dir)
