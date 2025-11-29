from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# This file now expects the global browser instance from just-test-it.py
# It will be imported *after* browser is created.

def from_landing_page_navigate_to_ai_chat(browser):
    
    time.sleep(1)

    try:
        ai_chat_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "ai_chat_button"))
        )
        ai_chat_btn.click()
    except Exception as e:
        print("[+] - ❌ FAILED navigation: cannot find ai_chat_button")
        print(e)

        # Fallback: navigate directly to the chat page
        fallback_url = "https://frontend-service-qfp2o6hkyq-ew.a.run.app/chat"
        print(f"[+] - ⚠️ Navigating directly to fallback AI chat URL: {fallback_url}")
        browser.get(fallback_url)

        return False

    time.sleep(5)
    return True



def testChatAndResponse(browser):

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
    elem.send_keys("Hello. Who are you?\n")
    time.sleep(5)

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
