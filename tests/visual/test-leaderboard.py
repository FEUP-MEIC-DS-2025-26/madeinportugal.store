from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
browser.set_window_size(1024, 768)


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

def navigate_host():
    # let's do the login
    browser.get(host_MIPS_Frontend)
    authenticate_host()

    # Test leaderboards
    print("Test-leaderboards start:")
    try:
        go_to_host_frontend()
        click_button('Product Leaderboards Page')
        scroll_down()
        scroll_up()
        switch_leaderboard_category()
        go_to_host_frontend()
        time.sleep(5)
    except:
        print("Error while testing leaderboards")

    # quit
    browser.quit()

def click_button(button_name):
    print(f"Clicking button {button_name}...")
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{button_name}'] | //button[normalize-space()='{button_name}']"))
    )
    button.click()
    time.sleep(3)
    
def scroll_down():
    print("Scrolling down...")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scroll_up():
    print("Scrolling up...")
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)

def switch_leaderboard_category(next_index = None):
    print("Changing leaderboard category...")
    try:
        sel_el = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, "leaderboard-select"))
        )
        sel = Select(sel_el)
        opts = sel.options
        if not opts:
            print("No options in select.")
            return

        if next_index is None:
            current_val = sel_el.get_attribute("value")
            current_idx = next((i for i,o in enumerate(opts) if o.get_attribute("value") == current_val), 0)
            target = current_idx + 1 if current_idx + 1 < len(opts) else 0
        else:
            target = max(0, min(next_index, len(opts) - 1))

        print(f"selecting option #{target} -> {opts[target].text}")
        sel.select_by_index(target)
        time.sleep(3)
    except Exception as e:
        print("switch_leaderboard_category failed:", e)

def go_to_host_frontend():
    print("Returning to home page...")
    browser.get(host_MIPS_Frontend)
    time.sleep(2)
    
navigate_host()
