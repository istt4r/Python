import time
import random
from pathlib import Path
import csv
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import URL, SS_INFO_PATH
import standards_exercise_table


def accept_gdpr(driver):
    """Clicks the "Agree" button in the GDPR popup window."""
    try:
        gdpr_agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-ifAKCX:nth-child(2)'))
        )
        gdpr_agree_button.click()
    except:
        print('GDPR agreement button not found or not clickable\n')


def scroll_position(driver, xpath):
    """Positions the driver view optimally."""
    element = driver.find_element(By.XPATH, xpath)
    y_coord = element.location['y'] - 300
    driver.execute_script("window.scrollTo(0, {})".format(y_coord))


def expand_exercises(driver):
    """Clicks the "More Exercises" button until all exercises are displayed on page."""
    more_exercises_xpath = "//button[normalize-space()='More Exercises...']"
    more_exercises_button = driver.execute_script('return document.querySelector(".py-2 > button:nth-child(1)")')

    while True:
        try:
            time.sleep(random.uniform(0.5, 1))
            driver.execute_script("arguments[0].click();", more_exercises_button)
            scroll_position(driver, more_exercises_xpath)
            if not more_exercises_button.is_enabled():
                print("Button is disabled")
                break
        except:
            print("More exercises button not found or not clickable")
            pass


def get_exercise_item_data(driver, item):
    """Extracts the exercise data from an exercise item."""
    url = urljoin("https://strengthlevel.com", item.find('a')['href'])
    img_url = item.find('img')['data-src']
    exercise_name = item.find('span').text.strip()
    exercise_records = item.find_all('span')[1].text.strip()

    print(f'Exercise Name: {exercise_name}')
    print(f'Exercise Records: {exercise_records}')
    print(f'URL: {url}')
    print(f'Image URL: {img_url}\n')

    standards_exercise_table.scrape_exercise_data(driver, exercise_name, exercise_records, url, img_url)
    driver.switch_to.window(driver.window_handles[0])


# Set the path and filename for the output file
info_file = Path(SS_INFO_PATH)

# Create a new Firefox browser window
with webdriver.Firefox() as driver:
    driver.maximize_window()
    driver.get(URL)

    # Get the handle of the original tab or window
    original_window_handle = driver.current_window_handle

    # Click "Agree" button in GDPR popup window
    accept_gdpr(driver)

    # Click "More Exercises" button until all exercises are displayed on page
    expand_exercises(driver)

    # Extract the HTML content after all the exercises have been loaded
    html_content = driver.page_source

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all div elements with class="exerciseitem"
    exercise_items = soup.find_all('div', {'class': 'exerciseitem'})

    for item in exercise_items:
        get_exercise_item_data(driver, item)

    driver.quit()
