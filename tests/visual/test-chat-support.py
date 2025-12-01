from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

def wait_for_new_support_message(driver, last_count, timeout=30):
    wait = WebDriverWait(driver, timeout)
    return wait.until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "div.message.support")) > last_count
    )

def get_last_support_message(driver):
    support_messages = driver.find_elements(By.CSS_SELECTOR, "div.message.support")
    if support_messages:
        return support_messages[-1].find_elements(By.TAG_NAME, "span")[1].text
    return None

def send_and_wait(message, driver):
    old_support_count = len(driver.find_elements(By.CSS_SELECTOR, "div.message.support"))
    textarea = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "form.chat-input textarea"))
    )
    textarea.send_keys(message)
    send_button = driver.find_element(By.CSS_SELECTOR, "form.chat-input button[type='submit']")
    send_button.click()
    wait_for_new_support_message(driver, old_support_count)
    reply = get_last_support_message(driver)
    print(f"Support replied: {reply}")

def navigate_chat_support(driver):
    # Move to the support chat button 
    element = driver.find_element(By.ID, "support_chat_button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(2)

    # Click the support chat button
    element.click()
    time.sleep(2)

    # Start the chat
    start_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "start-chat")))
    start_button.click()

    # Send messages and wait for replies
    send_and_wait("Hello, can you help me?", driver)
    time.sleep(2)
    send_and_wait("How much time do I have to request for a refund?", driver)
    time.sleep(2)
    send_and_wait("What is your refund policy?", driver)
    time.sleep(2)

    # Ask for human support
    element = driver.find_element(By.CLASS_NAME, "human-support")
    element.click()
    time.sleep(2)

    # Delete the chat
    element = driver.find_element(By.CLASS_NAME, "delete-chat")
    element.click()
    time.sleep(2)
    element = driver.find_element(By.CLASS_NAME, "deletion_button")
    element.click()
    time.sleep(2)


if __name__ == "__main__":
    # Test the chat support functionality
    options = Options()
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 20)
    driver.get("https://madeinportugal.store/")
    navigate_chat_support(driver)
    driver.quit()
