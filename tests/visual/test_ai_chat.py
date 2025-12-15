from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver as webdriver
import time

# This file now expects the global browser instance from just-test-it.py
# It will be imported *after* browser is created.

def from_landing_page_navigate_to_ai_chat(browser):
    
    time.sleep(1)

    try:
        ai_chat_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/mips-ai-agent']"))
        )
        print("[+] - ✅ Found MIPS Agent button by href")


        ai_chat_btn.click()
        print("[+] - ✅ Successfully clicked MIPS Agent button")
    except Exception as e:
        print("[+] - ❌ FAILED navigation: cannot find MIPS Agent button")
        print(e)

        # Fallback: navigate directly to the chat page
        fallback_url = "https://frontend-service-qfp2o6hkyq-ew.a.run.app/chat"
        print(f"[+] - ⚠️ Navigating directly to fallback AI chat URL: {fallback_url}")
        browser.get(fallback_url)

        return False

    return True


def authenticate(browser):
    """
    Fill in login form with email and password, then click continue button
    """
    try:
        # Wait for and fill in email field
        email_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.clear()
        email_field.send_keys("antonio.abilio2004@hotmail.com")
        print("[+] - ✅ Entered email address")
        
        # Wait for and fill in password field
        password_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys("porfew-ciqguV-8vixzy")
        print("[+] - ✅ Entered password")
        
        time.sleep(1)
        
        # Find and click the continue button
        # Try by button text first
        try:
            continue_btn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
        except:
            # Fallback: find by CSS selector targeting the button with the specific styling
            continue_btn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bg-\\[\\#00B5AA\\]"))
            )
        
        continue_btn.click()
        print("[+] - ✅ Clicked Continue button")
        
        return True
        
    except Exception as e:
        print(f"[+] - ❌ FAILED authentication: {e}")
        return False

def testChatAndResponse(browser, message, wait_for_response_time):
    # Try to find element by ID first
    try:
        elem = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "ChatInputTextArea"))
        )
    except Exception:
        # Fallback: find ANY textarea
        try:
            print("[!] ChatInputTextArea not found. Falling back to any <textarea>…")
            elem = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
        except Exception:
            print("[+] - ❌ FAILED testChatAndResponse (No input element found)")
            return False

    time.sleep(1)
    elem.send_keys(f"{message}\n")
    time.sleep(wait_for_response_time)

    # Wait for AI response
    try:
        ai_message_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "message-1"))
        )
        ai_message = ai_message_element.find_element(By.CSS_SELECTOR, "p").text
    except Exception:
        print("[+] - ❌ FAILED testChatAndResponse (AI message not found)")
        return False

    time.sleep(5)

    if len(ai_message) == 0:
        print("[+] - ❌ FAILED testChatAndResponse")
        return False

    print("[+] - ✅ PASSED testChatAndResponse")
    return True

if __name__ == "__main__":
    # Initialize the browser (example with Chrome)
    browser = webdriver.Chrome()

    # Navigate to the landing page
    browser.get("https://frontend.madeinportugal.store/")

    from_landing_page_navigate_to_ai_chat(
browser)
    time.sleep(2)
    authenticate(browser)
    time.sleep(2)
    from_landing_page_navigate_to_ai_chat(browser)
    message = "Hello. Who are you?"
    testChatAndResponse(browser, message, wait_for_response_time=3)
    message = "Can you show me some products?"
    testChatAndResponse(browser, message, wait_for_response_time=30)


    # Close the browser
    browser.quit()