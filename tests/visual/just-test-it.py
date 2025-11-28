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
browser.set_window_size(1024, 768)

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
    # let's do the login
    browser.get(landing_page)
    authenticate()

    # navigate to landing page
    browser.get(landing_page)
    # retrieve_menu_items_related_with_products()
    go_to_landing_page()
    click_image_search_btn()
    perform_image_search_by_image()
    perform_image_search_by_text()
    go_to_landing_page()
    time.sleep(5)

    # Suggest a product and inventory accept
    test_product_suggestion_page()
    test_inventory_dashboard()
    go_to_landing_page()
    time.sleep(5)

    # Spam Moderation flow
    run_moderator_flow()
    go_to_landing_page()
    time.sleep(5)

    #Tracking status
    test_tracking_status()
    go_to_landing_page()
    time.sleep(5)

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
    
    
def perform_image_search_by_image():
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
    time.sleep(2)
    
def perform_image_search_by_text():
    wait = WebDriverWait(browser, 10)

    text_tab = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search by Text']"))
    )
    browser.execute_script("arguments[0].click();", text_tab)
    time.sleep(1)

    textarea = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
    textarea.clear()
    textarea.send_keys("apple")

    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Search']"))
    )
    search_button.click()
    print("Searching by text for 'apple'...")

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.grid img"))
        )
        print("Text search results detected.")
    except Exception:
        print("No text search results detected before timeout.")

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def test_product_suggestion_page():
    page_links = browser.find_elements(By.CSS_SELECTOR, "a")
    for link in page_links:
        if link.text == "Seller Dashboard":
            link.click()
            break

    wait = WebDriverWait(browser, 10)
    wait.until(lambda d: any(b.text == "Suggest a product"
                            for b in d.find_elements(By.CSS_SELECTOR, ".action-content h3")))


    browser.implicitly_wait(0.5)

    dashboard_actions = browser.find_elements(By.CSS_SELECTOR, ".action-content h3")
    for content in dashboard_actions:
        if content.text == "Suggest a product":
            content.click()
            break

    original_window = browser.current_window_handle

    wait.until(EC.number_of_windows_to_be(2))

    for window_handle in browser.window_handles:
        if window_handle != original_window:
            browser.switch_to.window(window_handle)
            break

    wait.until(EC.title_is("Product Submission"))

    time.sleep(2)

    product_name = browser.find_element(By.ID, "name")

    product_name.send_keys("Queijinho da Serra")

    time.sleep(1)

    wait.until(lambda d: any(b.text == "Accept"
                            for b in d.find_elements(By.CSS_SELECTOR, "button")))

    browser.implicitly_wait(10)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text == "Accept":
            button.click()
            time.sleep(0.5)

    time.sleep(2)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text == "Submit Product Suggestion":
            button.click()
            break
        
    time.sleep(5)

def test_inventory_dashboard():
    # TODO(Process-ing): Access from landing page, once the link is available
    browser.get("https://mips-product-configuration-oqwis3m3oa-no.a.run.app/manage/submissions")

    wait = WebDriverWait(browser, 5)
    wait.until(lambda d: any(b.text == "Approve"
                         for b in d.find_elements(By.CSS_SELECTOR, "button")))
    time.sleep(1)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text == "Approve":
            button.click()
            break

    wait = WebDriverWait(browser, 2)
    wait.until(lambda d: any(b.text == "Approve Submission?"
                         for b in d.find_elements(By.CSS_SELECTOR, "h2")))
    time.sleep(1)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons[::-1]:
        if button.text == "Approve":
            button.click()
            break

    wait.until(lambda d: any("Submission Approved" in b.text
                         for b in d.find_elements(By.CSS_SELECTOR, "div")))
    time.sleep(2)

def run_moderator_flow():
    # Open user menu -> Admin
    original_window = browser.current_window_handle
    wait = WebDriverWait(browser, 20)
    try:
        user_menu = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@aria-label='Open user menu']")
        ))
        browser.execute_script("arguments[0].click();", user_menu)
        time.sleep(1)

        admin_opt = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'Admin')]")
        ))
        browser.execute_script("arguments[0].click();", admin_opt)

        # Switch to new tab
        wait.until(lambda d: len(d.window_handles) > 1)
        browser.switch_to.window(browser.window_handles[-1])
        print("[BOT] Admin page opened.")
        time.sleep(2)

        check_all = wait.until(EC.element_to_be_clickable((By.ID, "analyzeAll")))
        browser.execute_script("arguments[0].click();", check_all)
        print("[BOT] Waiting for analysis...")

        try:
            WebDriverWait(browser, 60).until(EC.alert_is_present())
            alert = browser.switch_to.alert
            print(f"[BOT] Alert: {alert.text}")
            alert.accept()
        except TimeoutException:
            print("[BOT] No alert appeared within timeout.")

    except Exception as e:
        print(f"[BOT] Admin flow error: {e}")
    finally:
        # Close admin tab if opened and return to original window
        try:
            if browser.current_window_handle != original_window:
                browser.close()
                browser.switch_to.window(original_window)
        except Exception:
            pass
    
def test_tracking_status():

    #Enter the orders page from the landing page
    wait = WebDriverWait(browser, 30)
    button = browser.find_element(By.XPATH, "//button[@aria-label='Open user menu']")
    button.click()
    links = browser.find_elements(By.CSS_SELECTOR, "a")
    for link in links:
        if link.text == "My Orders":
            link.click()
            break
    
    tabs = browser.window_handles
    # Switch to the new tab (last one in the list)
    browser.close()
    browser.switch_to.window(tabs[-1])
    
    wait.until(lambda d: any("Orders" in b.text.strip() for b in d.find_elements(By.CSS_SELECTOR, "h1")))


    #Click on the first order
    time.sleep(5)
    button = browser.find_element(By.ID, "order-1")
    button.click()

    wait.until(lambda d: any("Order 1" in b.text.strip() for b in d.find_elements(By.CSS_SELECTOR, "h1")))

    #Sleep for a few seconds to load the page
    time.sleep(5)

    #Focus on the carbon footprint and click on it
    element = browser.find_element(By.ID, "carb-button")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    element.click()
    
    #Some sleep to show the element
    time.sleep(5)

    #Click on the verification button
    element = browser.find_element(By.ID, "verification")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    element.click()
    wait.until(
    EC.element_to_be_clickable((By.ID, "verification")))
    time.sleep(5)

    #Go to the first link and click on it
    element = browser.find_element(By.ID, "link-0")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    element.click()
    time.sleep(8)
    tabs = browser.window_handles
    # Switch to the new tab (last one in the list)
    browser.switch_to.window(tabs[-1])
    browser.close()
    browser.switch_to.window(tabs[0])
    browser.back()


    #Click on the second order
    time.sleep(5)
    button = browser.find_element(By.ID, "order-2")
    button.click()

    wait.until(lambda d: any("Order 2" in b.text.strip() for b in d.find_elements(By.CSS_SELECTOR, "h1")))

    time.sleep(5)

    #Focus on the update button
    element = browser.find_element(By.ID, "update")
    browser.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)
    element.click()

    #Some sleep to show the element
    time.sleep(2)

    #Enter a new address
    element = browser.find_element(By.ID, "delivery-address")
    element.send_keys("Rua Dr. Roberto Frias, Porto, 4200-465 PORTO")
    time.sleep(1)

    #Click on the update button
    element = browser.find_element(By.ID, "send-update")
    element.click()

    #Click cancel to exit the modal
    element = wait.until(
    EC.element_to_be_clickable((By.ID, "cancel-update")))
    time.sleep(2)
    element.click()
    time.sleep(2)

    #Show the updated info
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(8)


    return

def go_to_landing_page():
    browser.get(landing_page)
    time.sleep(2)
    
navigate()
