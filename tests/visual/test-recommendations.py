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
username = "user"
password = "pass"

# start session
browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 960)

def authenticate(): 
    """Login via landing page using the username/password variables."""
    wait = WebDriverWait(browser, 20)

    # Ensure landing page is open
    try:
        if "madeinportugal.store" not in browser.current_url:
            browser.get(landing_page)
            time.sleep(1)
    except Exception:
        browser.get(landing_page)
        time.sleep(1)

    # Click Login
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Login')]")))
    browser.execute_script("arguments[0].click();", login_btn)
    time.sleep(1)

    if not username or not password:
        raise ValueError("Set 'username' and 'password' variables at the top of just-test-it.py")

    # Fill credentials
    user_input = wait.until(EC.presence_of_element_located((By.XPATH, "//form//input[1]")))
    user_input.clear()
    user_input.send_keys(username)

    pass_input = wait.until(EC.presence_of_element_located((By.XPATH, "//form//input[2]")))
    pass_input.clear()
    pass_input.send_keys(password)

    # Submit
    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//button[@type='submit']")))
    browser.execute_script("arguments[0].click();", submit_btn)
    print("Logging in...")
    time.sleep(3)


def navigate():
    browser.get(landing_page)
    time.sleep(1)

    authenticate()

    scroll_to_recommended_products()
    check_recommended_products()
    click_recommended_reason()
    click_recommendations_seemore()

    time.sleep(20)

    browser.quit()

def scroll_to_recommended_products():
    recommended_section = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "recommended")))
    print(recommended_section)

    browser.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        recommended_section
    )
    time.sleep(3)

def check_recommended_products():
    next_button = browser.find_element(By.XPATH, "//section[@id='recommended']//button[@id='rec-next-button']")
    for _ in range(5):
        next_button.click()
        time.sleep(1)
    time.sleep(2)
    
def click_recommended_reason():
    rec_reason_button = browser.find_element(
        By.XPATH, 
        "//section[@id='recommended']//*[@id='rec-carousel-frame']/*[4]//*[@id='rec-reason']"
    )
    rec_reason_button.click()
    time.sleep(5)

def click_recommendations_seemore():
    seemore_button = browser.find_element(By.XPATH, "//section[@id='recommended']//button[@id='rec-see-more-button']")
    seemore_button.click()
    time.sleep(16)
    
    browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )
    
    time.sleep(3)

def go_to_landing_page():
    browser.get(landing_page)
    time.sleep(2)
    
navigate()
