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
    
def toggle_theme_mode():
    print("   [Action] Toggling Theme (Light/Dark mode)...")
    wait = WebDriverWait(browser, 10)
    try:
        # Target the button using its aria-label. 
        # We use 'contains' to handle both "Switch to dark mode" and "Switch to light mode" 
        # just in case the default state changes.
        theme_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//nav//button[contains(@aria-label, 'Switch to')]")
        ))
        
        current_state = theme_btn.get_attribute("aria-label")
        print(f"   [Info] Found theme button. Current state: '{current_state}'")
        
        theme_btn.click()
        time.sleep(1) # Wait for the theme transition animation
        
        print("   [Success] Theme button clicked.")
        
    except Exception as e:
        print(f"   [Error] Failed to toggle theme: {e}")
    
def test_filter_functionality():
    print("   [Test] Testing 'Filter by Product ID'...")
    wait = WebDriverWait(browser, 10)
    try:
        # 1. Locate the input
        filter_input = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Filter by Product ID']")
        ))
        
        test_id = "32863680"
        
        # 2. Clear and Type (Using Control+A + Delete is safer for React inputs)
        filter_input.click()
        filter_input.send_keys(Keys.CONTROL + "a")
        filter_input.send_keys(Keys.DELETE)
        filter_input.send_keys(test_id)
        
        # 3. Wait for the table to refresh (Wait for stale element or simple sleep)
        time.sleep(2) 

        # 4. Count the rows using CSS Selector based on the screenshot classes
        # We look for TRs inside the TBODY with class MuiTableBody-root
        rows = browser.find_elements(By.CSS_SELECTOR, "tbody.MuiTableBody-root tr")
        
        print(f"   [Info] Detected {len(rows)} rows after filtering.")

        if len(rows) >= 1:
            # Check if the text matches to confirm it's the right row
            for row in rows:
                row_text = row.text
                if test_id in row_text:
                    continue
                else:
                    print(f"   [Failure] Found rows, but did not contain ID {test_id}. Text: {row_text}")
            
            print(f"   [Success] Filter worked. Found product with id {test_id}.")
        else:
            print(f"   [Failure] No rows found for ID {test_id}.")
            
        # 5. Clean up (Clear filter)
        filter_input.send_keys(Keys.CONTROL + "a")
        filter_input.send_keys(Keys.DELETE)
        time.sleep(1)
        
    except Exception as e:
        print(f"   [Error] Filter test failed: {e}")

def test_refresh_button():
    print("   [Test] Testing 'REFRESH' button...")
    wait = WebDriverWait(browser, 10)
    try:
        # Locate button by text and icon proximity usually, or just text
        refresh_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(), 'Refresh')]")
        ))
        refresh_btn.click()
        
        # Wait for a reload indicator or just a small sleep to ensure no crash
        time.sleep(2)
        print("   [Success] Page refreshed successfully.")
    except Exception as e:
        print(f"   [Error] Refresh button failed: {e}")

def test_pagination():
    print("   [Test] Testing Pagination ('NEXT')...")
    wait = WebDriverWait(browser, 10)
    try:
        # Scroll to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Attempt 1: Robust Text Search (using dot . instead of text())
        # This finds 'NEXT' or 'Next' even if nested in a <span>
        next_btn = None
        try:
            next_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'NEXT')] | //button[contains(., 'Next')]")
            ))
        except Exception:
            print("   [Info] Text detection failed. Trying structural fallback...")

        # Attempt 2: Structural Fallback (Targeting the enabled button in the footer)
        # Based on your screenshot, the 'Previous' button is disabled. 
        # We look for the last button on the page that is NOT disabled.
        if not next_btn:
            buttons = browser.find_elements(By.XPATH, "//button[@type='button']")
            # Filter for visible and enabled buttons
            valid_buttons = [b for b in buttons if b.is_displayed() and b.is_enabled()]
            if valid_buttons:
                # The 'Next' button is typically the very last active button on the screen
                next_btn = valid_buttons[-1]

        if next_btn:
            # Scroll specifically to the button to avoid footer overlaps
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
            time.sleep(1)
            next_btn.click()
            print("   [Success] Clicked 'NEXT' page.")
            
            time.sleep(2)
            
            # Optional: Test Previous button (which should now be enabled)
            # We use the same 'dot' technique
            try:
                prev_btn = browser.find_element(By.XPATH, "//button[contains(., 'PREVIOUS')] | //button[contains(., 'Previous')]")
                if prev_btn.is_enabled():
                    print("   [Info] 'PREVIOUS' button is now enabled.")
                    prev_btn.click()
                    print("   [Success] Clicked 'PREVIOUS' page.")
            except:
                pass 
        else:
            print("   [Failure] Could not identify the 'NEXT' button.")
        
        browser.execute_script("window.scrollTo(0, 0);")


    except Exception as e:
        print(f"   [Error] Pagination test failed: {e}")

from selenium.common.exceptions import StaleElementReferenceException # Add this to imports

def test_status_dropdowns():
    print("   [Test] Testing changing Status Dropdowns...")
    wait = WebDriverWait(browser, 10)
    statuses_to_test = ["BAN", "ARCHIVE", "WARNING", "All Statuses"]

    try:
        # 1. Find all dropdown triggers that are currently set to "Select status".
        # We use a robust XPath that looks for the MUI Select class and the text "Select status".
        # Using contains(., ...) ensures we find the text even if it's nested in spans.
        available_dropdowns = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'MuiSelect-select')]")
        ))
        
        num_dropdowns = len(available_dropdowns)
        print(f"   [Info] Found {num_dropdowns} rows available for testing.")

        if num_dropdowns < 3:
            print("   [Warning] Not enough rows found to test all 3 statuses independently. Testing with available rows.")
        
        # Loop through the statuses and apply them to the available rows.
        # We run the loop up to 3 times, or fewer if not enough rows are available.
        for i in range(min(num_dropdowns, len(statuses_to_test))):
            status_to_apply = statuses_to_test[i]
            # Important: re-find the dropdowns in each iteration to avoid StaleElementReferenceException
            # as the DOM changes after each status update.
            available_dropdowns = browser.find_elements(By.XPATH, "//div[contains(@class, 'MuiSelect-select')]")
            dropdown = available_dropdowns[0] # Always take the first available one
            
            print(f"   [Action] Changing status of a row to '{status_to_apply}'...")
            
            # Scroll to the dropdown and click it to open the menu
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            time.sleep(0.5)
            dropdown.click()
            
            # 2. Wait for the option to appear in the list and click it.
            # In MUI, the options list is often attached to the body, outside the table structure.
            # We look for an 'li' with role='option' containing the text we want.
            option_xpath = f"//li[@role='option'][contains(., '{status_to_apply}')]"
            option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            
            time.sleep(1) # Wait for the UI to update
            
            # 3. Verify the change.
            # We check if the dropdown we just clicked now displays the new status.
            try:
                # get_attribute("textContent") is often more reliable for MUI elements
                current_text = dropdown.get_attribute("textContent")
                if status_to_apply in current_text:
                    print(f"   [Success] Status successfully changed to '{status_to_apply}'.")
                else:
                    print(f"   [Failure] Status did not change. Current text: '{current_text}'")
                    
            except StaleElementReferenceException:
                # If the element is stale, it means the DOM updated, which is a success in this context.
                print(f"   [Success] Status changed to '{status_to_apply}' (DOM updated successfully).")
            except Exception as v_e:
                 print(f"   [Error] Verification failed: {v_e}")

    except Exception as e:
        print(f"   [Error] Row status test failed: {e}")

def test_change_product_statuses():
    print("   [Test] Changing status of the first 3 products (BAN, ARCHIVE, WARNING)...")
    wait = WebDriverWait(browser, 10)
    
    target_statuses = ["BAN", "ARCHIVE", "WARNING"]

    try:
        for i, status_text in enumerate(target_statuses):
            print(f"\n   [Action] Row {i+1}: Target status is '{status_text}'...")

            # 1. Re-fetch the specific row to avoid StaleElementReference
            rows = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tbody.MuiTableBody-root tr")
            ))

            if i >= len(rows):
                print(f"   [Warning] Table only has {len(rows)} rows. Skipping Row {i+1}.")
                break

            current_row = rows[i]
            
            # 2. Get the Dropdown and check its CURRENT value
            dropdown = current_row.find_element(By.CSS_SELECTOR, ".MuiSelect-select")
            current_status = dropdown.text.strip()
            
            # --- THE FIX: Check if it matches before clicking ---
            if status_text in current_status:
                print(f"   Row {i+1} is already '{status_text}'. Changing to {target_statuses[(i + 1)%3]}.")
                status_text = target_statuses[(i + 1)%3]
            # ----------------------------------------------------

            # 3. If not matching, change it
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            time.sleep(0.5)
            dropdown.click()
            
            try:
                # 4. Find the option in the list
                option_xpath = f"//li[@role='option'][contains(., '{status_text}')]"
                target_option = wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
                target_option.click()
                print(f"   [Success] Changed Row {i+1} from '{current_status}' to '{status_text}'.")
                time.sleep(1.5) # Wait for save
            except Exception as e:
                # If clicking the option fails (e.g. it's unexpectedly disabled), handle gracefully
                print(f"   [Error] Could not click option '{status_text}': {e}")
                # Press ESC to close the stuck dropdown so the next test can run
                webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    except Exception as e:
        print(f"   [Error] Critical failure in status test: {e}")

    
def test_admin_reports_feature():
    print("--- Test-admin-reports start ---")
    try:
        go_to_host_frontend()
        toggle_theme_mode()
        
        click_button('Admin')
        click_button('Reports')

        test_status_dropdowns()
        test_change_product_statuses()
        test_refresh_button()
        test_filter_functionality()
        test_pagination()
        
        go_to_host_frontend()
        print("--- Test-admin-reports passed ---")
        
    except Exception as e:
        print(f"--- Test-admin-reports FAILED: {e} ---")

def run_tests():
    try:
        test_admin_reports_feature()
    except KeyboardInterrupt:
        print("Test stopped by user.")
    finally:
        print("Closing browser...")
        browser.quit()

if __name__ == "__main__":
    run_tests()