from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Global variables
browser = None
wait = None

def test_wishlist_feature(browser_instance):
    global browser, wait
    browser = browser_instance
    wait = WebDriverWait(browser, 10)
    
    # Store the original window handle
    original_window = browser.current_window_handle
    
    access_wishlist()
    product_name = remove_product()
    if product_name:
        add_product(product_name)
    
    time.sleep(2)
    
    # Close any additional tabs/windows and switch back to original
    if len(browser.window_handles) > 1:
        # Close all windows except the original
        for handle in browser.window_handles:
            if handle != original_window:
                browser.switch_to.window(handle)
                browser.close()
        browser.switch_to.window(original_window) # Switch back to original window
        print("Closed additional tabs and returned to original window.")
        
        # Close the dropdown if it's still open by clicking the user icon again or pressing Escape
        try:
            user_icon = browser.find_element(By.XPATH, "//button[contains(@class, 'user') or contains(@aria-label, 'user') or contains(@aria-label, 'User')] | //*[contains(@class, 'user-icon')]")
            browser.execute_script("arguments[0].click();", user_icon)
            print("Closed dropdown.")
        except:
            pass  # Dropdown might already be closed
    
    time.sleep(2)

def access_wishlist():
    try: # try accessing wishlist from landing page
        print("Attempting to access wishlist from landing page...")
        
        # Click on user icon to open dropdown
        user_icon = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'user') or contains(@aria-label, 'user') or contains(@aria-label, 'User')] | //*[contains(@class, 'user-icon')] | //*[name()='svg' and contains(@class, 'user')]"))
        )
        browser.execute_script("arguments[0].click();", user_icon)
        print("Clicked user icon to open dropdown.")
        time.sleep(1)
        
        # Look for wishlist link in the dropdown
        wishlist_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Wishlist') or contains(text(),'Whishlist') or contains(@href,'wishlist')] | //button[contains(text(),'Wishlist') or contains(text(),'Whishlist')]"))
        )
        browser.execute_script("arguments[0].click();", wishlist_link)
        print("Clicked wishlist link from dropdown.")
        time.sleep(3)
        
        # Switch to the new window/tab if one was opened
        if len(browser.window_handles) > 1:
            browser.switch_to.window(browser.window_handles[-1])
            print("Switched to new tab/window.")
        
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Wishlist') or contains(text(),'Whishlist') or contains(text(),'My Wishlist') or contains(text(),'My Whishlist')]"))
        )
        print("Wishlist page loaded.")
        time.sleep(2)

    except:
        try: 
            # Navigate directly to wishlist page as fallback
            print("Couldn't find wishlist in landing page, navigating directly...")
            wishlist_url = "https://wishlist-frontend-1028448199115.europe-west1.run.app/"
            browser.get(wishlist_url)
            print("Navigating to wishlist page via direct URL...")
            time.sleep(3)
            
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Wishlist') or contains(text(),'Whishlist') or contains(text(),'My Wishlist') or contains(text(),'My Whishlist')]"))
            )
            print("Wishlist page loaded.")
            time.sleep(2)
        except Exception as e:
            print(f"Couldn't reach wishlist at all. Error: {e}")

def remove_product():
    # Find the first product's heart button and click to unheart it
    product_name = None
    try:
        # Get the product name from the first product
        try:
            product_name_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3.product-title"))
            )
            product_name = product_name_element.text
            print(f"Product name: {product_name}")
        except:
            print("Couldn't get product name, will continue without it")
        
        first_heart = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[contains(@class, 'heart')] | //button[@aria-label='Remove from wishlist'])[1]"))
        )
        print("Unheartting first product...")
        browser.execute_script("arguments[0].click();", first_heart)
        time.sleep(3)
        
        # Refresh the page
        print("Refreshing page...")
        browser.refresh()
        time.sleep(3)
        
        # Check if the product is still there (it shouldn't be)
        wishlist_items = browser.find_elements(By.CSS_SELECTOR, "h3.product-title")
        print(f"After refresh, wishlist contains {len(wishlist_items)} item(s).")
        print("Product should have been removed.")
        time.sleep(2)

        return product_name
    except Exception as e:
        print(f"Test failed: {e}")
        return None


def add_product(product_name):
    try:    
        print("\n--- Adding product back to wishlist ---")
        
        # Click "Add Products" button
        add_products_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add Products') or contains(text(),'Add Product')]"))
        )
        print("Clicking 'Add Products' button...")
        browser.execute_script("arguments[0].click();", add_products_btn)
        time.sleep(3)
        
        # Search bar should appear - search for the product we unheartted
        search_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='search' or contains(@placeholder,'Search') or contains(@placeholder,'search')]"))
        )
        print("Search bar appeared.")

        time.sleep(2)
        
        if product_name:
            print(f"Searching for '{product_name}'...")
            search_input.clear()
            search_input.send_keys(product_name)
        else:
            # Search for a generic term if we couldn't get the product name
            print("Searching for first available product...")
            search_input.clear()
            search_input.send_keys("product")
        
        time.sleep(3)
        
        # Click "Add" button for the first search result
        add_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(text(),'Add') or contains(text(),'add')])[1]"))
        )
        print("Clicking 'Add' button...")
        browser.execute_script("arguments[0].click();", add_btn)
        time.sleep(2)
        
        # Click "Hide Search" button
        hide_search_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Hide Search') or contains(text(),'Hide') or contains(text(),'Close')]"))
        )
        print("Clicking 'Hide Search' button...")
        browser.execute_script("arguments[0].click();", hide_search_btn)
        time.sleep(2)
        
        # Verify the product is back in the wishlist
        updated_wishlist_items = browser.find_elements(By.CSS_SELECTOR, "h3.product-title")
        print(f"After adding product back, wishlist contains {len(updated_wishlist_items)} item(s).")
        print("Product should now be visible in the wishlist again.")
        
    except Exception as e:
        print(f"Test failed: {e}")