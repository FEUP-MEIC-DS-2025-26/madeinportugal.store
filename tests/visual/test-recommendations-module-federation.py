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
host_MIPS_Frontend = 'https://frontend.madeinportugal.store'
login_page = ''
federatedLogin = ''

# credentials
username = "user"
password = "pass"

# start session
browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 960)

def authenticate_host(): 
    """Login via landing page using the username/password variables."""
    wait = WebDriverWait(browser, 20)

    # Ensure landing page is open
    try:
        if "microfrontend-host" not in browser.current_url:
            browser.get(host_MIPS_Frontend)
            time.sleep(1)
    except Exception:
        browser.get(host_MIPS_Frontend)
        time.sleep(1)

    print("Logging in...")
    time.sleep(5)

def navigate():
    browser.get(host_MIPS_Frontend)
    change_theme_color()
    authenticate_host()
    click_button("MIPS Recommendations Landing Page Section")
    check_recommended_products()
    click_recommended_reason()
    click_recommendations_seemore()

    go_to_host_MIPS_Frontend()
    click_button("MIPS Recommendations Page")
    time.sleep(20)
    browser.quit()

def change_theme_color():
    button = browser.find_element(By.XPATH, "//button[@id='theme-mode-button']")
    button.click()

def click_button(button_name):
    print(f"Clicking button {button_name}...")
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{button_name}'] | //button[normalize-space()='{button_name}']"))
    )
    button.click()
    time.sleep(3)

def check_recommended_products():
    next_button = browser.find_element(By.XPATH, "//button[@id='rec-next-button']")
    for _ in range(5):
        next_button.click()
        time.sleep(1)
    time.sleep(2)
    
def click_recommended_reason():
    rec_reason_button = browser.find_element(
        By.XPATH, 
        "//*[@id='rec-carousel-frame']/*[4]//*[@id='rec-reason']"
    )
    rec_reason_button.click()
    time.sleep(5)

def click_recommendations_seemore():
    seemore_button = browser.find_element(By.XPATH, "//button[@id='rec-see-more-button']")
    seemore_button.click()
    time.sleep(10)
    
    browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )
    
    time.sleep(10)

def go_to_host_MIPS_Frontend():
    browser.get(host_MIPS_Frontend)
    time.sleep(2)
    
navigate()
