from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
import getpass
import time
import os
# import re


# urls to use
landing_page = 'https://madeinportugal.store'
login_page = ''
federatedLogin = ''

# credentials
username = ""
password = ""

# start session
browser = webdriver.Chrome()

def authenticate(): 
    browser.get(login_page)

    # Wait for the login page to load (adjust the timeout as needed)
    wait = WebDriverWait(browser, 30)
    wait.until(EC.title_contains("Entering the website"))

    print(browser.current_url)

    # navigate to Web Login Service
    browser.get(federatedLogin)
    wait.until(EC.title_contains("Web Login Service"))
    print(browser.current_url)
    time.sleep(2)

    # Enter the credentials
    username_field = browser.find_element(By.ID, "username")
    password_field = browser.find_element(By.ID, "password")
    username_field.send_keys(username)
    # password = getpass.getpass('Password:')
    password_field.send_keys(password)

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Now you're logged in!
    print("Logging in...")
    time.sleep(2)


def navigate():
    # let's do the login
    # authenticate()

    # navigate to landing page
    browser.get(landing_page)
    # retrieve_menu_items_related_with_products()
    go_to_landing_page()
    click_image_search_btn()
    perform_image_search()
    go_to_landing_page()
    time.sleep(10)

    # quit
    browser.quit()


def retrieve_menu_items_related_with_products():
    items = browser.find_elements(By.LINK_TEXT,"Products")
    print("Visiting menu items...",str(items))
    for item in items:
       print("Menu item:"+item.text)

    return

def click_image_search_btn():
    image_search_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Image Search'] | //button[normalize-space()='Image Search']"))
    )
    image_search_button.click()
    time.sleep(2)  
    
    
def perform_image_search():
    file_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    browser.execute_script(
        "arguments[0].removeAttribute('hidden'); arguments[0].style.display = 'block';",
        file_input,
    )

    image_path = os.path.abspath("test_image.jpg")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Could not find image at {image_path}")

    file_input.send_keys(image_path)
    print("Uploaded image:", image_path)

    browser.execute_script(
        "arguments[0].setAttribute('hidden', 'true'); arguments[0].style.display = 'none';",
        file_input,
    )
    search_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']"))
    )
    time.sleep(2) 
    search_button.click()

    time.sleep(2)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        results_input = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']"))
        )
        results_input.send_keys(Keys.PAGE_DOWN)
    except Exception:
        print("Could not send PAGE_DOWN to number input; continuing")

    time.sleep(20)

def go_to_landing_page():
    browser.get(landing_page)
    time.sleep(2)
    
navigate()
