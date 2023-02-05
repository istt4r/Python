import requests
import datetime
import json
from config import API_KEY, EXPORT_LOG_PATH

# Get the current date
today = datetime.datetime.now().strftime("%Y-%m-%d")

database_url = "https://www.notion.so/c9658e29d153479bab54ae02b01ec1af?v=5e3924e8375f4fb6a3a4e1335fb8e483"      # Fitness - Workout Database URL
maximized_page_url = "https://www.notion.so/Pull-1-6bf18d0da59a41579535c0104333717a"                                      # Pull ONE Page URL
maximized_page_database_url = "https://www.notion.so/b3013e854c4140e28478dcbbc10edf63?v=875bf05e99de4f7888b7a48ac5f97b97" # Pull ONE Page Database URL
page_url = "https://www.notion.so/c9658e29d153479bab54ae02b01ec1af?v=5e3924e8375f4fb6a3a4e1335fb8e483&p=6bf18d0da59a41579535c0104333717a&pm=s"

# Get the database ID and view ID from the URL
database_id = database_url.split("/")[-1].split("?")[0]
view_id = database_url.split("=")[-1]
page_id = "6bf18d0da59a41579535c0104333717a"
property_id = "c9658e29-d153-479b-ab54-ae02b01ec1af"

print(f"database_url: {database_url}")
print(f"database_id: {database_id}")
print(f"view_id: {view_id}")
print(f"page_id: {page_id}")


# Set up the API endpoints to retrieve the database information ?v={view_id}
endpoint_database = f"https://api.notion.com/v1/databases/{database_id}"
endpoint_page = f"https://api.notion.com/v1/pages/{page_id}/properties/{property_id}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json",
    "Notion-Version": "2022-06-28"
}

# Make a GET request to the API endpoint
response = requests.get(endpoint_database, headers=headers)
data = json.loads(response.text)

# Function to write response to a log.txt file
def write_log_file(log_path,data):
    with open(log_path, "w") as log:
        log.write(json.dumps(data, indent=3))

write_log_file(EXPORT_LOG_PATH,data)

# Put on hold, while deciphering Notion API documentation...
"""
# Check if the request was successful
if response.status_code == 200:
    
    # Parse the response JSON data
    data = response.json()
    # Find the page corresponding to the current date
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    page_id = None
    for page in data["results"]:
        if page["title"][0]["text"]["content"] == today:
            page_id = page["id"]
            break
    # Export the information of the page
    if page_id:
        # You can use the Notion API to retrieve the information of the page and export it as needed
        print(f"Page with ID {page_id} was found and corresponds to the current date: {today}")
    else:
        print("No page was found corresponding to the current date.")
else:
    print("Failed to retrieve database information.")
"""

