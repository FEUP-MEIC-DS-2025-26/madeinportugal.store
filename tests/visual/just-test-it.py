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
landing_page = 'https://madeinportugal.store'
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

from test_ai_chat import *

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
    # let's do the login
    browser.get(landing_page)
    authenticate()

    try:
        # navigate to landing page
        browser.get(landing_page)
        # retrieve_menu_items_related_with_products()
        go_to_landing_page()
        click_image_search_btn()
        perform_image_search_by_image()
        perform_image_search_by_text()
        go_to_landing_page()
        time.sleep(5)
    except:
        print("Error in image search")

    try:
        # Suggest a product and inventory accept
        test_product_suggestion_page()
        print("Product suggestion submitted.")
        test_inventory_dashboard()
        print("Inventory dashboard processed.")
        test_edit_product_page()
        print("Product edited.")
        test_inventory_dashboard_edit()
        print("Product edition rejected.")
        go_to_landing_page()
        time.sleep(5)
    except:
        print("Error in inventory dashboard or product suggestion")

    # Spam Moderation flow
    try:
        run_moderator_flow()
        go_to_landing_page()
        time.sleep(5)
    except:
        print("Error in spam moderation")

    #Tracking status
    try:
        test_tracking_status()
        go_to_landing_page()
        time.sleep(5)
    except:
        print("Error in tracking status")
    # AI chat
    go_to_landing_page()
    from_landing_page_navigate_to_ai_chat(browser)
    testChatAndResponse(browser)
    time.sleep(5)
    go_to_landing_page()
    time.sleep(5)

    # Wishlist feature
    from test_wishlist import test_wishlist_feature
    try:
        test_wishlist_feature(browser)
        go_to_landing_page()
        time.sleep(5)
    except Exception as e:
        print(f"Error in wishlist feature: {e}")

    # Chat Support
    from test_chat_support import navigate_chat_support
    try:
        wait = WebDriverWait(browser, 3)
        navigate_chat_support(browser, wait)
    except Exception as e:
        print(f"Error in Chat Support feature: {e}")


    # quit
    #browser.quit()

def force_click_element(element):
    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", element)

def find_button_by_scanning(target_text):
    print(f"[Scan] A varrer a página por botões com texto '{target_text}'...")
    candidates = browser.find_elements(By.TAG_NAME, "button") + \
                 browser.find_elements(By.TAG_NAME, "a") + \
                 browser.find_elements(By.CSS_SELECTOR, "[role='button']")
    for btn in candidates:
        try:
            txt = btn.text or btn.get_attribute("innerText")
            if txt and target_text in txt:
                print(f"[Scan] Encontrado! Texto: '{txt}'")
                return btn
        except:
            continue
    return None

def robust_click(text_to_find, description):
    print(f"\n[Ação] A tentar clicar em: '{description}'...")
    wait = WebDriverWait(browser, 10)
    
    try:
        xpath = f"//*[contains(normalize-space(.), '{text_to_find}')]"
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        target = elements[-1] 
        force_click_element(target)
        print(f"[Sucesso] Clique forçado (XPath) em '{description}'.")
        return True
    except Exception:
        print(f"[XPath] Falhou. A tentar varredura manual...")

    target = find_button_by_scanning(text_to_find)
    if target:
        force_click_element(target)
        print(f"[Sucesso] Clique forçado (Scan) em '{description}'.")
        return True

    print(f"Não foi possível encontrar/clicar em '{text_to_find}'.")
    return False

def test_host_product_interaction():
    print("\n--- INICIANDO TESTE: PRODUCT PAGE FLOW ---")
    
    if not robust_click("PRODUCT PAGE CLASS 2 GROUP 2", "Botão Menu Produto"):
        print("Falha crítica: Não consegui entrar na página.")
        return

    print("A aguardar carregamento da página de produto...")
    wait = WebDriverWait(browser, 15)
    try:
        title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        print(f"Página carregada! Produto: {title.text}")
        
        browser.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)

        robust_click("COMPRAR", "Botão Comprar")
        
        time.sleep(2)
        print("Voltando ao menu do Host...")
        browser.back() 
        time.sleep(3) 

    except Exception as e:
        print(f"Erro na interação com o produto: {e}")

def navigate_host():
    # let's do the login
    browser.get(host_MIPS_Frontend)
    authenticate_host()

    # Test product page
    try:
        test_host_product_interaction()
    except Exception as e:
        print(f"Erro no teste Product Page: {e}")

    # Test leaderboards
    print("Test-leaderboards start:")
    try:
        go_to_host_frontend()
        click_button('Product Leaderboards Page')
        scroll_down()
        scroll_up()
        switch_leaderboard_category()
        go_to_host_frontend()
    except:
        print("Error while testing leaderboards")

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

    # this is also applicable for a product section, if it exists in the future it should be moved
    print("Test-certicate-management Service")
    try:
        test_certificate_service()
        go_to_landing_page()
    except:
        print("Error while testing certificate management")

    # quit
    #browser.quit()


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
    wait = WebDriverWait(browser, 20)
    dropdown = browser.find_element(By.CSS_SELECTOR, '[aria-label="Open user menu"]')
    dropdown.click()

    page_links = browser.find_elements(By.CSS_SELECTOR, "a")
    for link in page_links:
        if link.text == "Seller Dashboard":
            link.click()
            break

    time.sleep(2)

    original_window = browser.current_window_handle

    wait.until(EC.number_of_windows_to_be(2))

    for window_handle in browser.window_handles:
        if window_handle != original_window:
            browser.switch_to.window(window_handle)
            break

    wait.until(EC.title_is("Vendor Dashboard"))

    wait.until(
        lambda d: any(
            "suggest" in b.text.strip().lower()
            for b in d.find_elements(By.CSS_SELECTOR, ".action-content h3")
        )
    )

    dashboard_actions = browser.find_elements(By.CSS_SELECTOR, ".action-content")
    for content in dashboard_actions:
        if "suggest" in content.text.strip().lower():
            content.click()
            break

    product_name = browser.find_element(By.ID, "name")

    product_name.send_keys("Queijinho da Serra")

    time.sleep(1)

    wait.until(lambda d: any(b.text == "Accept"
                            for b in d.find_elements(By.CSS_SELECTOR, "button")))

    time.sleep(2)

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
    inventory = browser.find_element(By.CSS_SELECTOR, '[aria-label="Go to Inventory Manager Dashboard"]')
    inventory.click()

    wait = WebDriverWait(browser, 5)
    wait.until(lambda d: any(b.text == "Approve"
                         for b in d.find_elements(By.CSS_SELECTOR, "button")))
    time.sleep(1)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text == "Approve":
            button.click()
            break

    wait = WebDriverWait(browser, 5)
    wait.until(lambda d: any(b.text == "Approve Submission?"
                         for b in d.find_elements(By.CSS_SELECTOR, "h2")))
    time.sleep(1)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons[::-1]:
        if button.text == "Approve":
            button.click()
            break

    time.sleep(3)

    wait = WebDriverWait(browser, 5)
    wait.until(lambda d: any("Submission Approved" in b.text
                         for b in d.find_elements(By.CSS_SELECTOR, "div")))
    time.sleep(3)
    browser.back()
    time.sleep(2)

def test_edit_product_page():
    products = browser.find_element(By.CSS_SELECTOR, '[aria-label="View Products"]')
    products.click()
    time.sleep(2)
    link = browser.find_elements(By.CSS_SELECTOR, "a[href$='edit']")[0]
    link.click()

    time.sleep(2)

    product_name = browser.find_element(By.ID, "name")
    product_name.send_keys(" Edit")

    time.sleep(2)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons:
        if button.text == "Submit Product Suggestion":
            button.click()
            break

    time.sleep(2)
    browser.back()
    time.sleep(1)
    browser.back()
    time.sleep(2)

def test_inventory_dashboard_edit():
    inventory = browser.find_element(By.CSS_SELECTOR, '[aria-label="Go to Inventory Manager Dashboard"]')
    inventory.click()

    time.sleep(2)
    button = browser.find_element(By.XPATH, "//button[normalize-space(text())='Edition Suggestions']")
    button.click()

    time.sleep(2)

    button = browser.find_element(
        By.XPATH,
        "//div[@data-slot='card'][.//h3[contains(normalize-space(.), 'Edit')]]//button[normalize-space(text())='Reject']"
    )
    button.click()

    time.sleep(2)
    wait = WebDriverWait(browser, 2)
    wait.until(lambda d: any(b.text == "Reject Submission?"
                         for b in d.find_elements(By.CSS_SELECTOR, "h2")))
    time.sleep(1)

    buttons = browser.find_elements(By.CSS_SELECTOR, "button")
    for button in buttons[::-1]:
        if button.text == "Reject":
            button.click()
            break

    time.sleep(3)

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

# === Host ===

# Leaderboard

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

# Product Reviews

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

# Loyalty-System

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

# Generic

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

def go_to_host_frontend():
    print("Returning to home page...")
    browser.get(host_MIPS_Frontend)
    time.sleep(2)

def scroll_landing_page_slowly():
    """
    Navigate to the landing page and scroll slowly from top to bottom
    """
    print("[+] - 🚀 Starting landing page scroll test...")

    # Navigate to landing page
    try:
        browser.get(landing_page)
        print(f"[+] - 📄 Opened landing page: {landing_page}")
        time.sleep(3)  # Wait for page to load
    except Exception as e:
        print(f"[+] - ❌ FAILED to open landing page: {e}")
        return False

    # Get page dimensions
    try:
        total_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        viewport_height = browser.execute_script("return window.innerHeight")

        print(f"[+] - 📏 Page height: {total_height}px, Viewport height: {viewport_height}px")
    except Exception as e:
        print(f"[+] - ⚠️ Could not get page dimensions: {e}")
        total_height = 5000  # fallback value
        viewport_height = 960

    # Calculate scroll increment (scroll by small chunks)
    scroll_increment = viewport_height // 2  # Scroll by quarter viewport height each time
    current_position = 0

    print(f"[+] - 📜 Starting slow scroll (increment: {scroll_increment}px)...")

    # Scroll slowly from top to bottom
    while current_position < total_height:
        try:
            # Scroll down by increment
            browser.execute_script(f"window.scrollTo(0, {current_position});")

            # Wait between scrolls to simulate slow scrolling
            time.sleep(1.5)  # Adjust this value to make scrolling faster/slower

            current_position += scroll_increment

            # Get actual scroll position to handle cases where we can't scroll further
            actual_position = browser.execute_script("return window.pageYOffset")

            print(f"[+] - 📍 Scrolled to position: {actual_position}px")

            # If we haven't moved, we've reached the bottom
            if current_position > scroll_increment and actual_position < current_position - scroll_increment:
                print("[+] - 🏁 Reached bottom of page")
                break

        except Exception as e:
            print(f"[+] - ⚠️ Error during scroll: {e}")
            break

    # Pause at the bottom
    print("[+] - ⏸️ Pausing at bottom for 3 seconds...")
    time.sleep(3)

    # Scroll back to top slowly
    print("[+] - ⬆️ Scrolling back to top...")
    while current_position > 0:
        try:
            current_position -= scroll_increment
            if current_position < 0:
                current_position = 0

            browser.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1)  # Faster scroll back up

            actual_position = browser.execute_script("return window.pageYOffset")
            print(f"[+] - 📍 Scrolled back to position: {actual_position}px")

        except Exception as e:
            print(f"[+] - ⚠️ Error during scroll back: {e}")
            break

    # Final scroll to top
    try:
        browser.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        print("[+] - 🔝 Returned to top of page")
    except Exception as e:
        print(f"[+] - ⚠️ Error scrolling to top: {e}")

    print("[+] - ✅ Landing page scroll test completed successfully!")
    return True

def show_landing_page():
    """
    Main function to run all scroll tests
    """
    print("[+] - 🎯 Running Landing Page Scroll Tests")
    print("=" * 50)

    try:
        # Test 1: Basic scroll functionality
        if not scroll_landing_page_slowly():
            print("[+] - ❌ Basic scroll test failed")
            return False

        print("\n" + "-" * 50 + "\n")

        # Test 2: Element visibility during scroll
        if not test_page_elements_during_scroll():
            print("[+] - ❌ Element visibility test failed")
            return False

        print("\n" + "=" * 50)
        print("[+] - 🎉 All tests completed successfully!")

        # Keep browser open for a moment
        time.sleep(5)

    except Exception as e:
        print(f"[+] - ❌ Unexpected error during tests: {e}")
        return False

    # finally:
    #     # Close browser
    #     try:
    #         browser.quit()
    #         print("[+] - 🚪 Browser closed")
    #     except:
    #         pass

    return True

from test_certificate_service import *
def test_certificate_service():
    run_certificate_demo(browser)


show_landing_page()

navigate()

navigate_host()

# quit
browser.quit()
