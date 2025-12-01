from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# urls to use
landing_page = 'https://madeinportugal.store'


# start session
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)
browser.set_window_position(0, 0)
browser.set_window_size(1024, 768)
browser.set_window_position(0, 0)
browser.set_window_size(1024, 768)



def go_to_per_table():
    # look at seller dashboard
    login = "body > div.font-sans.min-h-screen > nav > div.max-w-7xl.mx-auto.px-4.sm\:px-6.lg\:px-8 > div > div.flex.items-center.space-x-4 > button.inline-flex.items-center.px-3.py-1\.5.border.border-gray-300.rounded-md.text-sm.font-medium.text-gray-700.bg-white.hover\:bg-gray-50.hover\:text-gray-900.transition-colors"
    browser.find_element(By.CSS_SELECTOR, login).click()
    time.sleep(2)
    confirm = "body > div.font-sans.min-h-screen > nav > div.max-w-7xl.mx-auto.px-4.sm\:px-6.lg\:px-8 > div > div.flex.items-center.space-x-4 > div > div > div > form > div > button.px-4.py-2.bg-green-700.text-white.rounded-md"
    browser.find_element(By.CSS_SELECTOR, confirm).click()
    time.sleep(2)
    account = "body > div.font-sans.min-h-screen > nav > div.max-w-7xl.mx-auto.px-4.sm\:px-6.lg\:px-8 > div > div.flex.items-center.space-x-4 > div > button > svg"
    browser.find_element(By.CSS_SELECTOR, account).click()
    # browser.find_element(By.CSS_SELECTOR, "[aria-label='Open user menu']").click()

    # go to sellers board
    time.sleep(5)

    original_window = browser.current_window_handle

    SELLERS_BOARD_LOCATOR = (By.CSS_SELECTOR,
                             r"body > div.font-sans.min-h-screen > nav > div.max-w-7xl.mx-auto.px-4.sm\:px-6.lg\:px-8 > div > div.flex.items-center.space-x-4 > div > div > a:nth-child(1)")
    
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(SELLERS_BOARD_LOCATOR)).click()
    except Exception:
        browser.find_element(*SELLERS_BOARD_LOCATOR).click() # Fallback click

    WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))

    for window_handle in browser.window_handles:
        if window_handle != original_window:
            browser.switch_to.window(window_handle)
            break

    time.sleep(4)

    scroll_down_script = "window.scrollBy(0, 200);"
    browser.execute_script(scroll_down_script)

    time.sleep(2)

    DASHBOARD_BUTTON_LOCATOR = (By.CSS_SELECTOR, 
                                r"body > #root > div.container > main.dashboard-main > section.dashboard-section > div.action-grid > button:nth-child(4)")

    button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable(DASHBOARD_BUTTON_LOCATOR)
    )
    button.click()

    time.sleep(5)
    # quit


def navigate():
    browser.get(landing_page)


    go_to_per_table()
    browser.quit()


if __name__ == '__main__':
    navigate()