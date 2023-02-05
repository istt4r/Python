import requests
import datetime
import json
from config import API_KEY

# Get the current date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Fitness - Workout Database
database_url = "https://www.notion.so/c9658e29d153479bab54ae02b01ec1af?v=5e3924e8375f4fb6a3a4e1335fb8e483"

# Get the database ID and view ID from the URL
database_id = database_url.split("/")[-1].split("?")[0]
view_id = database_url.split("=")[-1]

print(f"database_url: {database_url}")
print(f"database_id: {database_id}")
print(f"view_id: {view_id}")

# Set up the API endpoint to retrieve the database information ?v={view_id}
endpoint = f"https://api.notion.com/v1/databases/{database_id}"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json",
    "Notion-Version": "2022-06-28"
}

# Make a GET request to the API endpoint
response = requests.get(endpoint, headers=headers)
data = json.loads(response.text)

# Check if the request was successful
if response.status_code == 200:
    
    print(json.dumps(data,indent=4))
    """
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
        print("No page was found corresponding to the current date.")"""
else:
    print("Failed to retrieve database information.")
    print(json.dumps(response,indent=4))

