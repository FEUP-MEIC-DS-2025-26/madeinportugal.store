from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time


def wait_for_new_support_message(driver, last_count, wait, timeout=30):
    return WebDriverWait(driver, timeout).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.message.support")) > last_count
    )


def get_last_support_message(driver):
    messages = driver.find_elements(By.CSS_SELECTOR, "div.message.support")
    if messages:
        spans = messages[-1].find_elements(By.TAG_NAME, "span")
        if len(spans) > 1:
            return spans[1].text
    return None


def send_and_wait(message, driver, wait):
    old_support_count = len(driver.find_elements(By.CSS_SELECTOR, "div.message.support"))

    textarea = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "form.chat-input textarea"))
    )
    textarea.send_keys(message)

    send_button = driver.find_element(By.CSS_SELECTOR, "form.chat-input button[type='submit']")
    send_button.click()

    # Wait for a new message from support
    wait_for_new_support_message(driver, old_support_count, wait)

    reply = get_last_support_message(driver)
    print(f"Support replied: {reply}")


def navigate_chat_support(driver, wait):    
    # Scroll to support button
    support_btn = driver.find_element(By.ID, "support_chat_button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", support_btn)
    time.sleep(2)

    # Open chat window
    support_btn.click()
    time.sleep(2)

    # Click start chat
    start_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "start-chat")))
    start_button.click()

    # Send messages
    send_and_wait("Hello, can you help me?", driver, wait)
    time.sleep(1)
    send_and_wait("How much time do I have to request for a refund?", driver, wait)
    time.sleep(1)
    send_and_wait("What is your refund policy?", driver, wait)
    time.sleep(1)

    # Request human support
    human_btn = driver.find_element(By.CLASS_NAME, "human-support")
    human_btn.click()
    time.sleep(1)

    # Delete chat
    delete_btn = driver.find_element(By.CLASS_NAME, "delete-chat")
    delete_btn.click()
    time.sleep(1)

    confirm_btn = driver.find_element(By.CLASS_NAME, "deletion_button")
    confirm_btn.click()
    time.sleep(1)


if __name__ == "__main__":
    # If you test this file directly
    options = Options()
    service = Service("/usr/local/bin/geckodriver")

    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://madeinportugal.store/")
    navigate_chat_support(driver, wait)

    driver.quit()
