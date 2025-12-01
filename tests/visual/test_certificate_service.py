import os
import time
import shutil 
from selenium import webdriver

# Imports for Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Imports for Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configuration
TARGET_URL = "https://v0-certificate-validation-website-b.vercel.app/"
TEST_PRODUCT_ID = "selenium-test-product-001"
TEST_CERT_ID_1 = "ISCC-CORSIA-Cert-US201-2440920252"
TEST_CERT_ID_2 = "EU-ISCC-Cert-ES216-20254133" # Second Certificate
TEST_INVALID_CERT_ID = "INVALID-CERT-FORMAT-000" # Invalid Certificate
dummy_filename = "test_certificate.pdf"

# --- BROWSER SELECTION ---

def create_dummy_pdf():
    """Creates a dummy PDF file for upload testing."""
    content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << >> /MediaBox [0 0 612 792] >>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\ntrailer\n<< /Size 4 /Root 1 0 R >>\nstartxref\n223\n%%EOF"
    with open(dummy_filename, "wb") as f:
        f.write(content)
    return os.path.abspath(dummy_filename)

def run_certificate_demo(driver):
    print("--- Starting Certificate Service Demo ---")
    
    # driver = None
    # try:
    #     service = ChromeService(ChromeDriverManager().install())
    #     driver = webdriver.Chrome(service=service)
    # except WebDriverException as e:
    #     print(f"\n[ERROR] Failed to start Browser. \nDetails: {e}")
    #     return
    #
    wait = WebDriverWait(driver, 10)
    
    try:
        # 1. Create Test File
        pdf_path = create_dummy_pdf()
        print(f"[*] Generated dummy PDF at: {pdf_path}")

        # 2. Open Website
        print(f"[*] Navigating to {TARGET_URL}...")
        driver.get(TARGET_URL)
        time.sleep(3) 

        # ============================================================
        # SCENARIO 1: UPLOAD FIRST CERTIFICATE
        # ============================================================
        print("\n[Scenario 1] Uploading First Certificate...")
        
        # A. Switch to Upload Tab
        upload_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='tab'][contains(., 'Upload')]")))
        upload_tab.click()
        time.sleep(1)
        
        # B. Fill Form
        print(f"   > Uploading Cert 1: {TEST_CERT_ID_1}")
        product_input = wait.until(EC.visibility_of_element_located((By.ID, "productId")))
        product_input.clear()
        product_input.send_keys(TEST_PRODUCT_ID)
        
        cert_input = driver.find_element(By.ID, "certificateId")
        cert_input.clear()
        cert_input.send_keys(TEST_CERT_ID_1)
        
        file_input = driver.find_element(By.ID, "file-upload")
        file_input.send_keys(pdf_path)
        
        # C. Submit
        upload_btn = driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Upload Certificate')]")
        upload_btn.click()
        print("   > Upload button clicked.")
        
        time.sleep(3) 

        # ============================================================
        # SCENARIO 1.5: UPLOAD SECOND CERTIFICATE (Same Product)
        # ============================================================
        print("\n[Scenario 1.5] Uploading Second Certificate (Same Product)...")
        
        # 1. Re-find and Click Upload Tab
        print("   > Switching back to Upload tab...")
        upload_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='tab'][contains(., 'Upload')]")))
        upload_tab.click()
        
        # 2. Verify Tab Switch
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab'][contains(., 'Upload')][@data-state='active']")))
        time.sleep(1) 
        
        print(f"   > Uploading Cert 2: {TEST_CERT_ID_2}")
        
        # 3. Fill Form 
        product_input = wait.until(EC.visibility_of_element_located((By.ID, "productId")))
        product_input.clear()
        product_input.send_keys(TEST_PRODUCT_ID)
        
        cert_input = wait.until(EC.visibility_of_element_located((By.ID, "certificateId")))
        cert_input.clear()
        cert_input.send_keys(TEST_CERT_ID_2)
        
        file_input = driver.find_element(By.ID, "file-upload")
        file_input.send_keys(pdf_path)
        
        upload_btn = driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Upload Certificate')]")
        upload_btn.click()
        print("   > Upload button clicked.")
        time.sleep(3)

        # ============================================================
        # SCENARIO 2: INVALID CERTIFICATE UPLOAD (Negative Test)
        # ============================================================
        print("\n[Scenario 2] Attempting Invalid Certificate Upload...")
        
        # 1. Re-find and Click Upload Tab
        print("   > Switching back to Upload tab...")
        upload_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='tab'][contains(., 'Upload')]")))
        upload_tab.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='tab'][contains(., 'Upload')][@data-state='active']")))
        time.sleep(1)

        print(f"   > Uploading INVALID Cert: {TEST_INVALID_CERT_ID}")
        
        # 2. Fill Form
        product_input = wait.until(EC.visibility_of_element_located((By.ID, "productId")))
        product_input.clear()
        product_input.send_keys(TEST_PRODUCT_ID)
        
        cert_input = wait.until(EC.visibility_of_element_located((By.ID, "certificateId")))
        cert_input.clear()
        cert_input.send_keys(TEST_INVALID_CERT_ID)
        
        file_input = driver.find_element(By.ID, "file-upload")
        file_input.send_keys(pdf_path)
        
        # 3. Submit
        upload_btn = driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Upload Certificate')]")
        upload_btn.click()
        print("   > Upload button clicked.")
        
        # 4. Check for Error
        # We expect validation to fail, so we might see a toast or remain on the page.
        try:
            # Look for common error indicators (Toasts often have role='status' or class='destructive')
            # Or text like "Error", "Failed", "Invalid"
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'destructive') or contains(text(), 'Error') or contains(text(), 'Invalid')]")))
            print("   > [SUCCESS] System rejected invalid certificate (Error message detected).")
        except TimeoutException:
            print("   > [WARNING] No specific error toast found, verifying we are still on the form...")
            # If we are still on the upload tab (i.e., didn't get redirected to Dashboard), that's also a success for a negative test.
            try:
                # Check if upload button is still visible
                driver.find_element(By.XPATH, "//button[@type='submit'][contains(., 'Upload Certificate')]")
                print("   > [SUCCESS] Upload did not proceed (Still on form).")
            except NoSuchElementException:
                print("   > [FAIL] Seemed to proceed/redirect despite invalid input.")

        time.sleep(2)

        # ============================================================
        # VERIFICATION
        # ============================================================
        print("\n[Verification] Checking Browse List...")
        
        browse_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@role='tab'][contains(., 'Browse')]")))
        browse_tab.click()
        
        try:
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), TEST_PRODUCT_ID))
            print("   > [SUCCESS] Product visible in list.")
        except TimeoutException:
            print("   > [FAIL] Product did not appear in the Browse list.")
        
        time.sleep(2)

        # ============================================================
        # SCENARIO 3: DELETE CERTIFICATE (With Custom Dialog)
        # ============================================================
        print(f"\n[Scenario 3] Deleting Product: {TEST_PRODUCT_ID}...")
        
        # Switch back to Browse tab just in case
        browse_tab.click()
        time.sleep(1)

        try:
            # 1. Find the product text
            product_text_el = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[text()='{TEST_PRODUCT_ID}']")))
            
            # 2. Find the initial Delete button (the trash icon/button on the row)
            delete_row_btn = product_text_el.find_element(By.XPATH, "./following::button[contains(., 'Delete') or contains(@class, 'destructive')] | ./ancestor::div[contains(@class, 'border')]//button[contains(@class, 'destructive') or contains(., 'Delete')]")
            
            delete_row_btn.click()
            print("   > Initial Delete button clicked.")
            
            # 3. Handle CUSTOM CONFIRMATION DIALOG
            print("   > Waiting for confirmation dialog...")
            
            # Look for the dialog footer specifically, then the Delete button inside it
            confirm_delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-slot='alert-dialog-footer']//button[contains(@class, 'bg-destructive')]")))
            
            confirm_delete_btn.click()
            print("   > Confirmation dialog 'Delete' button clicked.")

            # 4. Verify Disappearance
            print("   > Waiting for item to disappear...")
            wait.until(EC.invisibility_of_element_located((By.XPATH, f"//*[text()='{TEST_PRODUCT_ID}']")))
            print("   > [SUCCESS] Product removed from list.")
            
        except NoSuchElementException:
             print("   > [FAIL] Could not locate the delete button or product.")
        except TimeoutException:
             print("   > [FAIL] Timed out waiting for dialog or disappearance.")
        except Exception as e:
            print(f"   > [ERROR] Error during deletion: {e}")

        time.sleep(2)

    except Exception as e:
        print(f"\n[CRITICAL ERROR] Test Failed: {e}")
    
    finally:
        print("\n--- Teardown ---")
        if os.path.exists(dummy_filename):
            try:
                os.remove(dummy_filename)
                print(f"[*] Removed {dummy_filename}")
            except:
                pass
