import time
import random
from pathlib import Path
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL, SS_INFO_PATH

# set the path and filename for the output file
info_file = Path(SS_INFO_PATH)
# create a new Firefox browser window
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(URL)

# wait for the GDPR agreement policy to load and click the button to agree to the terms
try:
    gdpr_agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-ifAKCX:nth-child(2)'))
    )
    gdpr_agree_button.click()
except:
    print('GDPR agreement button not found or not clickable\n')


more_exercises_button = driver.execute_script('return document.querySelector(".py-2 > button:nth-child(1)")')
while True:
    try:
        time.sleep(random.uniform(0.5, 1))
        driver.execute_script("arguments[0].click();", more_exercises_button)
        if more_exercises_button.is_enabled() == False:
            print("Button is disabled")
            break
    except:
        print("More exercises button not found or not clickable")
        pass


# extract the HTML content after all the exercises have been loaded
html_content = driver.page_source

# create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# find all div elements with class="exerciseitem"
exercise_items = soup.find_all('div', {'class': 'exerciseitem'})


def getExerciseItemData():
    # extract the url contained within the anchor tag
    url = item.find('a')['href']

    # extract the url contained in the image tag
    img_url = item.find('img')['data-src']

    # extract the text contained within the span contained within the div of class "media-content"
    exercise_name = item.find('span').text.strip()

    # extract the text contained within the second span contained within the div of class "media-content"
    exercise_records = item.find_all('span')[1].text.strip()
    
    # write the extracted information to the output file
    writer.writerow([exercise_name, exercise_records, url, img_url])

    # print the extracted information
    print(f'Exercise Name: {exercise_name}')
    print(f'Exercise Records: {exercise_records}')
    print(f'URL: {url}')
    print(f'Image URL: {img_url}\n')

# open the output file for writing
with info_file.open(mode='w', newline='', encoding='utf-8') as file:
    # create a CSV writer object
    writer = csv.writer(file)

    # write the header row
    writer.writerow(['Exercise Name', 'Exercise Records', 'URL', 'Image URL'])

    # iterate over each exercise item and extract the required information
    for item in exercise_items:
        getExerciseItemData()


