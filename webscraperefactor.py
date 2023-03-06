from config import SS_DATA_PATH
import csv
from pathlib import Path
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://strengthlevel.com/strength-standards/squat")
driver.execute_script("document.body.style.zoom='80%'")

# buttons to select to display table data by weight, age, and gender
male_button = driver.find_element(By.XPATH, "//li[@data-tab='Male']//a")
female_button = driver.find_element(By.XPATH, "//li[@data-tab='Female']//a")

# xpath definitions
scroll_position_xpath = "//div[@data-tab-group='Standards Exercise']"
male_weight_xpath = "//body[1]/section[1]/div[1]/div[6]/div[2]/div[1]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr"
male_age_xpath = "//body[1]/section[1]/div[1]/div[6]/div[2]/div[1]/div[3]/div[3]/div[1]/table[1]/tbody[1]/tr"
female_weight_xpath = "//body[1]/section[1]/div[1]/div[6]/div[3]/div[1]/div[3]/div[2]/div[1]/table[1]/tbody[1]/tr"
female_age_xpath = "//body[1]/section[1]/div[1]/div[6]/div[3]/div[1]/div[3]/div[3]/div[1]/table[1]/tbody[1]/tr"

# Define the categories and genders to fetch data for
categories = ["weight", "age"]
genders = ["male", "female"]

# Define the exercise and today's date
exercise = "Squat"
today = datetime.date.today()


# Wait for the GDPR agreement policy to load and click the button to agree to the terms
try:
    gdpr_agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-ifAKCX:nth-child(2)'))
    )
    gdpr_agree_button.click()
except:
    print('GDPR agreement button not found or not clickable\n')

# position the driver view optimally at the head of gender select button
def scroll_position(xpath):
    element = driver.find_element(By.XPATH, xpath)
    y_coord = element.location['y']
    driver.execute_script("window.scrollTo(0, {})".format(y_coord))
scroll_position(scroll_position_xpath)


#or gender not in ["male", "female"]
def get_table_data(exercise, category, gender, table_xpath):
    if category not in ["age", "weight"]:
        raise ValueError("Invalid category specified")

    # Find all the rows in the table
    table_rows = driver.find_elements(By.XPATH, table_xpath)

    table_data = []
    for row in table_rows:
        # Skip the row if it does not contain any text
        if not row.text.strip():
            continue
        columns = row.find_elements(By.TAG_NAME, "td")
        category_data = {
            'exercise': exercise,
            'datecollected': today,
            'category': category,
            'gender': gender,
            'categoryvalue': columns[0].text,
            'beginner': columns[1].text,
            'novice': columns[2].text,
            'intermediate': columns[3].text,
            'advanced': columns[4].text,
            'elite': columns[5].text
        }
        table_data.append(category_data)
    return table_data

table_data = []
for gender in genders:
    for category in categories:
        # Click the appropriate gender button
        if gender == "male":
            male_button.click()
        elif gender == "female":
            female_button.click()

        # Click the appropriate category button
        if category == "weight":
            weight_button = driver.find_element(By.XPATH, "//a[text()='By Bodyweight' and not(ancestor::div[contains(@class, 'is-hidden')])]")
            weight_button.click()
            table_xpath = male_weight_xpath if gender == "male" else female_weight_xpath
        elif category == "age":
            age_button = driver.find_element(By.XPATH, "//a[text()='By Age' and not(ancestor::div[contains(@class, 'is-hidden')])]")
            age_button.click()
            table_xpath = male_age_xpath if gender == "male" else female_age_xpath

        # Get the table data
        data = get_table_data(exercise, category, gender, table_xpath)
        table_data.extend(data)

# Merge all the data into one object
merged_data = {'data': table_data}

# write merged_data to csv
merge_path = Path(SS_DATA_PATH) / "merge.csv"
with merge_path.open(mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=list(merged_data['data'][0].keys()))
    writer.writeheader()
    for row in merged_data['data']:
        writer.writerow(row)


