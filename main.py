from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import pyperclip
import secret   

# Options you should comment thsi section out if you don't use Proxy 

PROXY = "http://iproxi.man:80"

options = webdriver.EdgeOptions()
options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_argument('--proxy-server=%s' % PROXY)

# ---------------------------------------------------------------

# Your chrome driver path comment out Edge Driver Path
driver_path = "C:/Users/paulg/Documents/Coding/Automation/edgedriver_win64/msedgedriver.exe"
#driver = webdriver.Chrome(chrome_driver_path)
# ---------------------------------------------------------------
# Edge Driver Path
s = Service(driver_path)
driver = webdriver.Edge(service=s, options=options)
# ----------------------------------------------------------------

driver.maximize_window()
wait = WebDriverWait(driver, 60) 
driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords=marketing%20intern&location=London%2C%20England%2C%20United%20Kingdom&redirect=false&position=1&pageNum=0")

# Account Information 
ACCOUNT_EMAIL = secret.EMAIL
ACCOUNT_PASSWORD = secret.PW
PHONE = secret.PHONE
# ----------------------------------------------------------------

# Constants
# If your website is running on another language than german then change "Einloggen" to your shown log in text
LOG_IN_TEXT = "Einloggen"
# Same again if you use another langauge than german then change the submit button text here
SUBMIT_BTN_TEXT = "Weiter"
# ----------------------------------------------------------------


wait.until(EC.element_to_be_clickable((By.LINK_TEXT, LOG_IN_TEXT)))
sign_in_button = driver.find_element(By.LINK_TEXT, LOG_IN_TEXT)
sign_in_button.click()

wait.until(EC.element_to_be_clickable((By.ID, "username")))
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(PHONE)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.loader-overlay#loader[ng-show='loading'][aria-labelledby='loading-msg']")))
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".job-card-container--clickable")))

time.sleep(2)
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

for listing in all_listings:
    print("Started apply process.")
    time.sleep(2)
    listing.click()
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-s-apply button")))
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        apply_button.click()

        time.sleep(3)
        try:
            phone = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div[5]/div/div/div[1]/div/input")
            if phone.text == "":
                phone.send_keys(PHONE)
        except NoSuchElementException:
            print("No Phone needed.")        
        
        try:
            summary = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div[7]/div/div/div[1]/div/textarea")
            summary.send_keys("Hi,\ndas ist nur ein Test wie der Bewerbungsprozess hier funktioniert.\nIch entschuldige mich schonmal, falls die Nachricht wirklich an Sie rasugeht.\n\nBeste Grüße\nGerman Paul")
        except NoSuchElementException:
            print("No Summary needed.")
            
        time.sleep(3) 
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button") 
        try:
            submit_button.click()
        except StaleElementReferenceException:
            print("No Submit Button found.")   
        time.sleep(1)
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()
        time.sleep(2)
        discard_button = driver.find_element(By.CLASS_NAME, "artdeco-button--secondary")
        print(discard_button.text)
        discard_button.click()
        print("For now we skip this application, since they need more information.")
            

    except NoSuchElementException:
        print("No application button, skipped.")
        continue
    except StaleElementReferenceException:
        print("Failed to apply.")
        continue

time.sleep(5)
driver.quit()