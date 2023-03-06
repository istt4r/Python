import csv
import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import SS_DATA_PATH


def get_table_data(driver, exercise_name, category, gender, table_xpath, today):
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
            'exercise': exercise_name,
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


def scrape_exercise_data(driver, exercise_name, exercise_records, url, image_url):
    driver.switch_to.new_window('tab')
    driver.get(url)

    # Define the categories and genders to fetch data for
    categories = ["weight", "age"]
    genders = ["male", "female"]

    today = datetime.date.today()

    # Define the xpath for scrolling to the exercise element
    scroll_position_xpath = "//div[@data-tab-group='Standards Exercise']"

    # Scroll to the exercise element
    element = driver.find_element(By.XPATH, scroll_position_xpath)
    y_coord = element.location['y']
    driver.execute_script("window.scrollTo(0, {})".format(y_coord))

    table_data = []
    for gender in genders:
        for category in categories:
            # Get the button for the selected gender
            gender_button = driver.find_element(By.XPATH, f"//li[@data-tab='{gender.capitalize()}']//a")
            gender_button.click()

            if category == "weight":
                # Get the button for selecting data by bodyweight
                weight_button = driver.find_element(By.XPATH, "//a[text()='By Bodyweight' and not(ancestor::div[contains(@class, 'is-hidden')])]")
                weight_button.click()
            elif category == "age":
                # Get the button for selecting data by age
                age_button = driver.find_element(By.XPATH, "//a[text()='By Age' and not(ancestor::div[contains(@class, 'is-hidden')])]")
                age_button.click()

            # Get the table data
            table_xpath = "//table[(ancestor::div[contains(@data-tab-group, 'By Weight and Age')])]//tr"
            if gender == "female":
                table_xpath += "[not(contains(@class, 'male'))]"
            data = get_table_data(driver, exercise_name, category, gender, table_xpath, today)
            table_data.extend(data)

    # Merge all the data into one object
    merged_data = {'data': table_data}

    # Write the data to a CSV file
    merge_path = Path(SS_DATA_PATH) / f"{exercise_name}.csv"
    with merge_path.open(mode='w', newline='') as csvfile:
        if merged_data['data']:
            writer = csv.DictWriter(csvfile, fieldnames=list(merged_data['data'][0].keys()))
            writer.writeheader()
            for row in merged_data['data']:
                writer.writerow(row)
        else:
            print('No data to write to CSV file\n')


    # Save exercise records
    with open(f"{SS_DATA_PATH}/exercise_details.txt", "a") as file:
        file.write(f"{exercise_name},{exercise_records},{url},{image_url}\n")
        
    driver.close()
