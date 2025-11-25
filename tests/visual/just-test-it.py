from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
import getpass
import time
# import os
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
    time.sleep(10)

    # quit
    browser.quit()


def retrieve_menu_items_related_with_products():
    items = browser.find_elements(By.LINK_TEXT,"Products")
    print("Visiting menu items...",str(items))
    for item in items:
       print("Menu item:"+item.text)

    return

navigate()
