import csv
import datetime
import notion_client
import config
from config import ROOT_DIR

# Initialize a Notion client
notion = notion_client.Client(auth={"token_v2": config.NOTION_API_TOKEN})

# Get the current date
today = datetime.datetime.now().strftime("%Y-%m-%d")

