from config import SS_DATA_PATH
import csv
from pathlib import Path


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://strengthlevel.com/strength-standards/bench-press")

# Wait for the GDPR agreement policy to load and click the button to agree to the terms
try:
    gdpr_agree_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.sc-ifAKCX:nth-child(2)'))
    )
    gdpr_agree_button.click()
except:
    print('GDPR agreement button not found or not clickable\n')

# Scroll to the bottom of the page to load all the table data
driver.execute_script("window.scrollTo(0, 1443)")

#or gender not in ["male", "female"]
def get_strength_table_data(category,table_xpath):
    if category not in ["age", "weight"]:
        raise ValueError("Invalid category or gender specified")

    # Find all the rows in the table
    table_rows = driver.find_elements(By.XPATH, table_xpath)

    table_data = []
    for row in table_rows:
        # Skip the row if it does not contain any text
        if not row.text.strip():
            continue
        columns = row.find_elements(By.TAG_NAME, "td")
        category_data = {}
        for i, column in enumerate(columns):
            # Skip the first column as it contains the category
            if i == 0:
                category_data[category] = column.text
                continue
            # Map each column to its corresponding strength level category
            categories = ["beginner", "novice", "intermediate", "advanced", "elite"]
            category_label = categories[i-1]
            category_data[category_label] = column.text
        table_data.append(category_data)
    return table_data


male_weight_xpath = "/html/body/section/div/div[6]/div[2]/div/div[3]/div[2]/div/table/tbody/tr"
male_weight_table_data = get_strength_table_data("weight",male_weight_xpath)
for row in male_weight_table_data:
    print(row)

male_age_xpath = "/html/body/section/div/div[6]/div[2]/div/div[3]/div[3]/div/table/tbody/tr"
male_age_table_data = get_strength_table_data("age",male_age_xpath)
for row in male_age_table_data:
    print(row)


female_weight_xpath = "/html/body/section/div/div[6]/div[3]/div/div[3]/div[2]/div/table/tbody/tr"
female_weight_table_data = get_strength_table_data("weight",female_weight_xpath)
for row in female_weight_table_data:
    print(row)
    
female_age_xpath = "html/body/section/div/div[6]/div[3]/div/div[3]/div[3]/div/table/tbody/tr"
female_age_table_data = get_strength_table_data("weight",female_age_xpath)
for row in female_weight_table_data:
    print(row)


# write male weight data to CSV file
male_weight_path = Path(SS_DATA_PATH) / "male_weight.csv"
with male_weight_path.open(mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=male_weight_table_data[0].keys())
    writer.writeheader()
    writer.writerows(male_weight_table_data)

# write male age data to CSV file
male_age_path = Path(SS_DATA_PATH) / "male_age.csv"
with male_age_path.open(mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=male_age_table_data[0].keys())
    writer.writeheader()
    writer.writerows(male_age_table_data)

# write female weight data to CSV file
female_weight_path = Path(SS_DATA_PATH) / "female_weight.csv"
with female_weight_path.open(mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=female_weight_table_data[0].keys())
    writer.writeheader()
    writer.writerows(female_weight_table_data)

# write female age data to CSV file
female_age_path = Path(SS_DATA_PATH) / "female_age.csv"
with female_age_path.open(mode='w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=female_age_table_data[0].keys())
    writer.writeheader()
    writer.writerows(female_age_table_data)