from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

driver.get("https://naturalmedicines.therapeuticresearch.com/IngredientsTherapiesMonographs")

checkbox = driver.find_element(By.ID, "food-herb-supplement")
checkbox.click()

searchbutton = driver.find_element(By.NAME, "search-monographs")
searchbutton.click()

letters = driver.find_elements(By.CSS_SELECTOR, "#letterTabs .nav-link")

for idx, letter in enumerate(letters):
    try:
        letters = driver.find_elements(By.CSS_SELECTOR, "#letterTabs .nav-link")
        btn = letters[idx]

        text = btn.text.strip()
        print(f"Clicking: {text}")

        driver.execute_script("arguments[0].scrollIntoView(true);", btn)

        btn.click()

        time.sleep(1)

    except Exception as e:
        print(f"Error clicking letter tab")


