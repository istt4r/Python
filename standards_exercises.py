import time
import random
from pathlib import Path
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL, SS_INFO_PATH
from bs4 import BeautifulSoup
import standards_exercise_table
from urllib.parse import urljoin

# set the path and filename for the output file
info_file = Path(SS_INFO_PATH)
# create a new Firefox browser window
driver = webdriver.Firefox()
driver.maximize_window()
driver.get(URL)

# Get the handle of the original tab or window
original_window_handle = driver.current_window_handle

more_exercises_xpath = "//button[normalize-space()='More Exercises...']"
more_exercises_button = driver.execute_script('return document.querySelector(".py-2 > button:nth-child(1)")')

# click "agree" button in GDPR popup window
def accept_gdpr():
    # wait for the GDPR agreement policy to load and click the button to agree to the terms
    try:
        gdpr_agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-ifAKCX:nth-child(2)'))
        )
        gdpr_agree_button.click()
    except:
        print('GDPR agreement button not found or not clickable\n')
accept_gdpr()

# position the driver view optimally
def scroll_position(xpath):
    element = driver.find_element(By.XPATH, xpath)
    y_coord = element.location['y'] - 300
    driver.execute_script("window.scrollTo(0, {})".format(y_coord))


# click "more exercises" button until all exercises are displayed on page
def expand_exercises():
    while True:
        try:
            time.sleep(random.uniform(0.5, 1))
            driver.execute_script("arguments[0].click();", more_exercises_button)
            scroll_position(more_exercises_xpath)
            if more_exercises_button.is_enabled() == False:
                print("Button is disabled")
                break
        except:
            print("More exercises button not found or not clickable")
            pass
expand_exercises()

# extract the HTML content after all the exercises have been loaded
html_content = driver.page_source

# create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# find all div elements with class="exerciseitem"
exercise_items = soup.find_all('div', {'class': 'exerciseitem'})

exercise_standards = []
def get_exercise_item_data():
    #url = item.find('a')['href']
    url = urljoin("https://strengthlevel.com", item.find('a')['href'])
    img_url = item.find('img')['data-src']
    exercise_name = item.find('span').text.strip()
    exercise_records = item.find_all('span')[1].text.strip()
    
    # writer.writerow([exercise_name, exercise_records, url, img_url])

    # print the extracted information
    print(f'Exercise Name: {exercise_name}')
    print(f'Exercise Records: {exercise_records}')
    print(f'URL: {url}')
    print(f'Image URL: {img_url}\n')
    
    standards_exercise_table.scrape_exercise_data(driver, exercise_name,exercise_records,url,img_url)
    driver.switch_to.window(original_window_handle)
    
for item in exercise_items:
    get_exercise_item_data()

driver.quit()

