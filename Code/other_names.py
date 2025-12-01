from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

options = Options()
options.add_argument("--start-maximized") 
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True) 

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = "https://naturalmedicines.therapeuticresearch.com/api/sitecore/account/SingleSignOn/?url=%2fHome%2fND"

driver.get(url)

driver.implicitly_wait(10)
box = driver.find_element(By.ID, "username")
box.send_keys("hdavulcu@asu.edu")

driver.find_element(By.ID, "kc-login").click()

box = driver.find_element(By.ID, "password")
box.send_keys("Cour@g3W1ns")

driver.find_element(By.ID, "kc-login").click()

time.sleep(2)

cookiebutton = driver.find_element(By.ID, "onetrust-accept-btn-handler")
cookiebutton.click()

time.sleep(2)

driver.get("https://naturalmedicines.therapeuticresearch.com/IngredientsTherapiesMonographs")

time.sleep(2)

checkbox = driver.find_element(By.ID, "food-herb-supplement")
checkbox.click()

letters = driver.find_elements(By.CSS_SELECTOR, "#letterTabs .nav-link")

time.sleep(2)

data = {}

it = 1

for idx, letter in enumerate(letters):

    with open("../NatMedOtherNames/natmed_other_names" + str(it) + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        it += 1
    
    data = {}

    letters = driver.find_elements(By.CSS_SELECTOR, "#letterTabs .nav-link")
    btn = letters[idx]

    text = btn.text.strip()
    print(f"Clicking: {text}")

    driver.execute_script("arguments[0].click();", btn)

    time.sleep(1)

    items = driver.find_elements(By.CSS_SELECTOR, "#monographList .list__item a")

    for j in range(len(items)):
        letters = driver.find_elements(By.CSS_SELECTOR, "#letterTabs .nav-link")
        btn = letters[idx]
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)
        items = driver.find_elements(By.CSS_SELECTOR, "#monographList .list__item a")
        item = items[j]
        item_name = item.text.strip()
        print(f"   -> Visiting item: {item_name}")
        driver.execute_script("arguments[0].setAttribute('target','_self')", item)

        driver.execute_script("arguments[0].click();", item)
        time.sleep(2)

        #scrape data here
        more_buttons = driver.find_elements(By.CSS_SELECTOR, "button.custom-details-toggle")        
        for more_button in more_buttons:
            driver.execute_script("arguments[0].click();", more_button)

        container = driver.find_element(By.CLASS_NAME, "page-header__content-container")
        other_names = container.text.strip()
        after = other_names.split("OTHER COMMON NAMES", 1)[1].strip()[:-4]
        print(after)
        data[item_name] = after 

        # Go back to the list page
        driver.back()
        time.sleep(1.5)  
        checkbox = driver.find_element(By.ID, "food-herb-supplement")
        checkbox.click()
        checkbox.click()
        time.sleep(1.5)  


    


