import csv
import datetime
import notion_client
import config

# Initialize a Notion client
notion = notion_client.Client(auth={"token_v2": config.NOTION_API_TOKEN})

# Get the current date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Search for database entries with a "Date" field equal to today
results = notion.search(filter={"property": "Date", "value": today}).get("results")

# Write the results to a CSV file
with open("entries.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Date", "Description"])
    for result in results:
        writer.writerow([result["title"], result["Date"], result["Description"]])