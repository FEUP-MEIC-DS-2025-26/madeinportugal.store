from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure Chrome to run headless
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://frontend.madeinportugal.store/")

wait = WebDriverWait(driver, 10)

try:
    # 1. Click the notifications bell
    bell = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".notifications-container .bell-button"))
    )
    bell.click()

    # 2. Wait until dropdown becomes visible
    dropdown = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".notifications-container .dropdown"))
    )
    print("Dropdown opened successfully")

    # 3. Click the settings button
    settings_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".notifications-container .dropdown .settings-btn"))
    )
    settings_btn.click()

    # 4. Wait for the preferences UI to appear
    prefs_panel = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".preferences-container"))
    )
    print("Preferences panel opened successfully")

    # Check for the text elements
    expected_texts = [
        "Preferences",
        "Back",
        "Notification Preferences",
        "Email Notifications",
        "Push Notifications",
        "Sound Enabled"
    ]

    for text in expected_texts:
        elem = wait.until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(), '{text}')]"))
        )
        print(f"Found element with text: '{text}'")

finally:
    driver.quit()