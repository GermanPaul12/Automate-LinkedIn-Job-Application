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

# Account Information 
#! Create a file named "secret.py" containing the variables EMAIL, PW and PHONE
ACCOUNT_EMAIL = secret.EMAIL
ACCOUNT_PASSWORD = secret.PW
PHONE = secret.PHONE
#! Change this to your CV Path
CV_PATH = r"C:\Users\paulg\Documents\Unterlagen\CV\German Paul.pdf"
#! Change this to your photo path
PHOTO_PATH = r"C:\Users\paulg\Documents\Unterlagen\CV\Me.jpg"
#! Change this to your Choice
CITY_WHERE_YOU_WANT_TO_WORK = "Bangkok"
COUNTRY_WHERE_YOU_WANT_TO_WORK = "Thailand"
WHAT_KIND_OF_JOB = "Data Science Intern Let's do this"

#! Do not touch this code
JOB_DESCRIPTION_FOR_URL = ""
WHAT_KIND_OF_JOB = WHAT_KIND_OF_JOB.split(" ")
for i in range(len(WHAT_KIND_OF_JOB)):
    if i == len(WHAT_KIND_OF_JOB) - 1:
        JOB_DESCRIPTION_FOR_URL += WHAT_KIND_OF_JOB[i]
    else:
        JOB_DESCRIPTION_FOR_URL += WHAT_KIND_OF_JOB[i] + "%20"
#!----------------------------------------------------------------        
# ----------------------------------------------------------------
driver.get(f"https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491&keywords={JOB_DESCRIPTION_FOR_URL}&location={CITY_WHERE_YOU_WANT_TO_WORK}%2C%20{COUNTRY_WHERE_YOU_WANT_TO_WORK}%2C&redirect=false&position=1&pageNum=0")
# Constants
# If your website is running on another language than german then change "Einloggen" to your shown log in text
LOG_IN_TEXT = "Einloggen"
# ----------------------------------------------------------------


### Functions

def submit():
    try:
        submit_button = driver.find_element(By.CSS_SELECTOR, "footer button.artdeco-button--primary")  
        print(submit_button.text)
        #! If you want your application to be send then remove the if condition and remove the indentation of the click code
        if submit_button.text != "Bewerbung senden":
            submit_button.click()
    except StaleElementReferenceException:
        print("No Submit Button found.")  
    except NoSuchElementException:
        print("No Submit Button found.")    
    time.sleep(2)    

def element_clicker(element):
    try:
        element.click()
    except Exception as e:
        print(f"{e} while trying to click {element.text}")    

def element_writer(element, text_input):
    try:
        element.send_keys(text_input)
    except Exception as e:
        print(f"{e} while trying to write {text_input} in {element.text}")   
# ----------------------------------------------------------------


wait.until(EC.element_to_be_clickable((By.LINK_TEXT, LOG_IN_TEXT)))
element_clicker(driver.find_element(By.LINK_TEXT, LOG_IN_TEXT))

wait.until(EC.element_to_be_clickable((By.ID, "username")))
element_writer(driver.find_element(By.ID, "username"), PHONE)
element_writer(driver.find_element(By.ID, "password"), ACCOUNT_PASSWORD)
element_writer(driver.find_element(By.ID, "password"), Keys.ENTER)

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
        element_clicker(driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button"))

        time.sleep(2)
        element_writer(driver.find_element(By.CSS_SELECTOR, "input[id*='phoneNumber'"), PHONE)

        try:
            summary = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div[7]/div/div/div[1]/div/textarea")
            summary.send_keys("Hi,\ndas ist nur ein Test wie der Bewerbungsprozess hier funktioniert.\nIch entschuldige mich schonmal, falls die Nachricht wirklich an Sie rasugeht.\n\nBeste Grüße\nGerman Paul")
        except NoSuchElementException:
            print("No Summary needed.")
            
        time.sleep(3) 
        submit()
        try:
            address = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div[1]/div/div/div[1]/div/input")
            address.send_keys(secret.ADR)
        except NoSuchElementException:
            print("No address field found.")
        try:
            city = driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div[3]/div/div/div/input")
            city.click()
            city.send_keys(secret.CITY)
            city.click()
            city.send_keys(Keys.DOWN)
            time.sleep(1)
            city.send_keys(Keys.DOWN)
            time.sleep(0.5)
            city.send_keys(Keys.ENTER)
            time.sleep(2)
        except NoSuchElementException:
            print("No city field found.")     
        submit()
        
        time.sleep(2)
        try:
            cv = driver.find_element(By.CSS_SELECTOR, "input[id*='resume'")
            cv.send_keys(CV_PATH) 
        except NoSuchElementException:
            print("No cv field found.")  
        
        try:    
            anschreiben = driver.find_element(By.CSS_SELECTOR, "textarea")
            anschreiben.send_keys("Das ist ein Test für ein Automatiserungsprojekt ich hoffe diese Nachricht wird nicht wirklich an Sie gesendet.")
        except NoSuchElementException:
            print("No anschreiben field found.")
        time.sleep(1)         
        submit()
        try: 
            photo = driver.find_element(By.CSS_SELECTOR, "input[accept*='jpg'")
            photo.send_keys(PHOTO_PATH)
        except NoSuchElementException:
            print("No photo field found.")  
        time.sleep(3)
        # Closes the current application  
        submit()
        submit()
        submit()
        submit()
        try:           
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
            time.sleep(2)
            discard_button = driver.find_element(By.CLASS_NAME, "artdeco-button--secondary")
            discard_button.click()
            print("For now we skip this application, since they need more information.")
        except NoSuchElementException:
            print("No application button, skipped.")
            continue
        except StaleElementReferenceException:
            print("Failed to apply.")
            continue
        #----------------------------------------------------    

    except NoSuchElementException:
        print("No application button, skipped.")
        continue
    except StaleElementReferenceException:
        print("Failed to apply.")
        continue
    
    
time.sleep(5)
driver.quit()