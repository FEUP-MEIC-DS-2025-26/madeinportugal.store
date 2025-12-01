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

    # Test product-reviews
    print("Test-product-reviews start:")
    try:
        go_to_host_frontend()
        click_button('Product Reviews Page')
        select_product_prod_reviews(3)
        select_first_user_prod_reviews()
        set_rating_prod_reviews()
        write_review_prod_reviews()
        click_button('Submit Review')
        go_to_host_frontend()
    except:
        print("Error while testing reviews")

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

def select_product_prod_reviews(index=1):
    print(f"Selecting product #{index}...")
    label_id = "product-select-label"
    wait = WebDriverWait(browser, 6)

    try:
        combobox = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'div[role="combobox"][aria-labelledby="{label_id}"]')
        ))

        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
        try:
            combobox.click()
        except:
            browser.execute_script("arguments[0].click();", combobox)

        option_xpath = (
            f"(//ul[@role='listbox' and .//li[@role='option']])[last()]"
            f"//li[@role='option' and not(contains(@class,'Mui-disabled'))][{index}]"
        )

        opt = WebDriverWait(browser, 4).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        browser.execute_script("arguments[0].click();", opt)

        time.sleep(1)
        print(f"Selected product #{index}.")
    except Exception as e:
        print("select_product_prod_reviews failed:", e)

def select_first_user_prod_reviews():
    print("Selecting user...")
    label_id = "customer-select-label"
    wait = WebDriverWait(browser, 6)
    try:
        combobox = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f'div[role="combobox"][aria-labelledby="{label_id}"]')
        ))
        browser.execute_script("arguments[0].scrollIntoView({block:'center'});", combobox)
        try:
            combobox.click()
        except Exception:
            browser.execute_script("arguments[0].click();", combobox)

        option_xpath = (
            "(//ul[@role='listbox' and .//li[@role='option']])[last()]"
            "//li[@role='option' and not(contains(@class,'Mui-disabled'))][1]"
        )
        opt = WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
        browser.execute_script("arguments[0].click();", opt)
        time.sleep(1)
        print("Selected first user.")
    except Exception as e:
        print("select_first_user_prod_reviews failed:", e)
        try:
            lbl_trigger = browser.find_element(By.XPATH, "//label[@id='customer-select-label']")
            alt = lbl_trigger.find_element(By.XPATH, "ancestor::*[contains(@class,'MuiFormControl-root')][1]//div[@role='combobox']")
            alt.send_keys(Keys.SPACE)
            opt = WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, "(//ul[@role='listbox'])[last()]//li[1]")))
            browser.execute_script("arguments[0].click();", opt)
            time.sleep(1)
            print("Selected first user (fallback).")
        except Exception:
            try:
                browser.switch_to.active_element.send_keys(Keys.ESCAPE)
            except Exception:
                pass

def set_rating_prod_reviews(stars = 3):
    print(f"Setting rating to {stars} stars...")

    wait = WebDriverWait(browser, 6)
    try:
        rating_root = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.MuiRating-root")))
    except Exception as e:
        print("Rating root not present (product reviews may not be rendered):", e)

    try:
        labels = rating_root.find_elements(By.TAG_NAME, "label")
        if labels and len(labels) >= stars:
            target_lbl = labels[stars - 1]
            browser.execute_script("arguments[0].scrollIntoView({block:'center'});", target_lbl)
            try:
                target_lbl.click()
            except Exception:
                browser.execute_script("arguments[0].click();", target_lbl)
            time.sleep(1)
            return
    except Exception as e:
        print("Label-in-root attempt failed:", e)

    try:
        txt = f"{stars} Star" if stars == 1 else f"{stars} Stars"
        lbl_xpath = f".//span[contains(normalize-space(.),'{txt}')]/parent::label"
        lbl = None
        try:
            lbl = rating_root.find_element(By.XPATH, lbl_xpath)
        except Exception:
            lbl = browser.find_element(By.XPATH, f"//span[contains(normalize-space(.),'{txt}')]/parent::label")
        if lbl:
            browser.execute_script("arguments[0].scrollIntoView({block:'center'});", lbl)
            try:
                lbl.click()
            except Exception:
                browser.execute_script("arguments[0].click();", lbl)
            time.sleep(1)
            return
    except Exception as e:
        print("Visually-hidden label attempt failed:", e)

    try:
        inp = None
        try:
            inp = rating_root.find_element(By.XPATH, f".//input[@type='radio' and @value='{stars}']")
        except Exception:
            try:
                inp = browser.find_element(By.XPATH, f"//input[@type='radio' and @value='{stars}']")
            except Exception:
                inp = None

        if inp:
            browser.execute_script(
                """
                arguments[0].checked = true;
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """,
                inp,
            )
            time.sleep(1)
            return
    except Exception as e:
        print("JS input-check attempt failed:", e)

    try:
        svgs = browser.find_elements(By.XPATH, "//span[contains(@class,'MuiRating-root')]//svg | //div[contains(@class,'rating')]//svg")
        if svgs and len(svgs) >= stars:
            target_svg = svgs[stars - 1]
            browser.execute_script("arguments[0].scrollIntoView({block:'center'});", target_svg)
            try:
                target_svg.click()
            except Exception:
                browser.execute_script("arguments[0].click();", target_svg)
            time.sleep(1)
            return
    except Exception as e:
        print("SVG click fallback failed:", e)

    print("Failed to set rating. Ensure the review form is rendered (product selected) and inspect the rating DOM.")

def write_review_prod_reviews(text="Good Product!"):
    print("Writting review text...")
    try:
        wait = WebDriverWait(browser, 5)
        ta = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "textarea")))
        ta.clear()
        ta.send_keys(text)
        time.sleep(1)
    except Exception as e:
        print("write_review failed:", e)
    time.sleep(3)

def go_to_host_frontend():
    print("Returning to home page...")
    browser.get(host_MIPS_Frontend)
    time.sleep(2)
    
navigate_host()
