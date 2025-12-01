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

    # Test loyalty
    print("Test-loyalty start:")
    try:
        go_to_host_frontend()
        click_button('MIPS Loyalty System')
        toggle_use_points()
        click_button("Place Order (Pay €41.00)")
        go_to_host_frontend()
    except:
        print("Error while testing loyalty")

    # quit
    browser.quit()

def click_button(button_name):
    print(f"Clicking button {button_name}...")
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{button_name}'] | //button[normalize-space()='{button_name}']"))
    )
    button.click()
    time.sleep(3)

def toggle_use_points(use = True):
    print("Toggling checkbox")
    try:
        wait = WebDriverWait(browser, 6)
        checkbox = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".points-box .points-check input[type='checkbox']")
        ))
    except Exception:
        try:
            checkbox = WebDriverWait(browser, 4).until(
                EC.presence_of_element_located((By.XPATH, "//label[contains(normalize-space(.), 'Use my points')]//input[@type='checkbox']"))
            )
        except Exception as e:
            print("toggle_use_points: checkbox not found:", e)
            return

    try:
        current = checkbox.is_selected()
    except Exception:
        current = bool(checkbox.get_attribute("checked"))

    if current == use:
        print(f"toggle_use_points: already {'checked' if use else 'unchecked'}.")
        return

    try:
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        try:
            checkbox.click()
        except Exception:
            browser.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
    except Exception as e:
        print("toggle_use_points: click attempt failed:", e)
        return

    try:
        final = checkbox.is_selected()
    except Exception:
        final = bool(checkbox.get_attribute("checked"))

    if final != use:
        print("toggle_use_points: failed to change state (final != desired).")
        return

    if use:
        try:
            WebDriverWait(browser, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".points-warning, .points-box .points-warning"))
            )
        except Exception:
            print("toggle_use_points: points-warning did not appear (not fatal).")

    print(f"toggle_use_points: checkbox is now {'checked' if final else 'unchecked'}.")
    time.sleep(2)
    return

def go_to_host_frontend():
    print("Returning to home page...")
    browser.get(host_MIPS_Frontend)
    time.sleep(2)
    
navigate_host()
