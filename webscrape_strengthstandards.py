import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# Define the URL of the webpage
url = 'https://strengthlevel.com/strength-standards'

# Define the headers to be sent with the requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Define the minimum and maximum intervals between requests (in seconds)
min_interval = 5
max_interval = 10

# Send a GET request to the webpage and get its HTML content
response = requests.get(url, headers=headers)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the links to the individual exercise pages
exercise_links = soup.find_all('a', class_='ex-link')

# Loop through each exercise link and scrape the table data
for link in exercise_links:
    exercise_name = link.get_text()
    exercise_url = link['href']

    # Generate a random delay before sending the request to avoid detection
    delay = random.randint(min_interval, max_interval)
    time.sleep(delay)

    # Send a GET request to the exercise page and get its HTML content
    exercise_response = requests.get(exercise_url, headers=headers)
    exercise_html_content = exercise_response.content

    # Create a BeautifulSoup object to parse the exercise HTML content
    exercise_soup = BeautifulSoup(exercise_html_content, 'html.parser')

    # Find the table with the strength standards by age and weight
    strength_table = exercise_soup.find('table', class_='table table-striped')

    # If the table exists, extract its data and save it to a CSV file
    if strength_table:
        # Define the name of the output file
        output_file_name = f'{exercise_name}.csv'

        # Open the output file in write mode and create a CSV writer object
        with open(output_file_name, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)

            # Loop through each row in the table and extract its data
            for row in strength_table.find_all('tr'):
                data = [cell.get_text(strip=True) for cell in row.find_all('td')]
                if data:
                    csv_writer.writerow(data)
