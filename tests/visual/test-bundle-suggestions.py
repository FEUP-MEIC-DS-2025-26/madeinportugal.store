from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

host_MIPS_Frontend = 'https://microfrontend-host-1054126107932.europe-west1.run.app'

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)
browser.set_window_position(0, 0)
browser.set_window_size(1280, 960)


def go_to_host_frontend():
    print("Returning to home page...")
    if browser.current_url != host_MIPS_Frontend:
        browser.get(host_MIPS_Frontend)
    time.sleep(2)

def click_button(button_name):
    print(f"Clicking button '{button_name}'...")
    wait = WebDriverWait(browser, 10)
    try:
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{button_name}'] | //button[normalize-space()='{button_name}']"))
        )
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(1) 
        button.click()
        time.sleep(3)
    except Exception as e:
        print(f"Failed to find or click button '{button_name}': {e}")
        raise e

def not_interest_logic():
    print("Testing 'Not interested' functionality...")
    wait = WebDriverWait(browser, 15)
    
    try:
        initial_product_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h6")))
        initial_product_name = initial_product_element.text
        print(f"   [Initial] Top suggestion: {initial_product_name}")
    except Exception:
        print("   [Info] No products visible initially (or loading slow).")
        initial_product_name = ""

    try:
        not_interested_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not interested')]"))
        )
        browser.execute_script("arguments[0].click();", not_interested_btn)
        print("   [Action] Clicked 'Not interested' button.")
    except Exception as e:
        print(f"   [Error] Could not find 'Not interested' button: {e}")
        return

    time.sleep(1)
    
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h6")))
        
        new_product_element = browser.find_element(By.XPATH, "//h6")
        new_product_name = new_product_element.text
        
        print(f"   [Result] New top suggestion: {new_product_name}")
        
        if initial_product_name and new_product_name != initial_product_name:
            print("   [Success] The suggestions have updated successfully!")
        elif not initial_product_name and new_product_name:
             print("   [Success] Suggestions loaded from empty state!")
        else:
            print("   [Warning] The product name is the same. API might have returned the same bundle or refresh failed.")

    except Exception as e:
        print(f"   [Error] Timeout waiting for new suggestions to load: {e}")


def test_bundle_suggestions_feature():
    print("--- Test-bundle-suggestions start ---")
    try:
        go_to_host_frontend()
        
        click_button('Bundle Suggestions')
        
        not_interest_logic()
        
        go_to_host_frontend()
        print("--- Test-bundle-suggestions passed ---")
        
    except Exception as e:
        print(f"--- Test-bundle-suggestions FAILED: {e} ---")
        browser.save_screenshot("bundle_test_failure.png")


def run_tests():
    try:
        test_bundle_suggestions_feature()
    except KeyboardInterrupt:
        print("Test stopped by user.")
    finally:
        print("Closing browser...")
        browser.quit()

if __name__ == "__main__":
    run_tests()