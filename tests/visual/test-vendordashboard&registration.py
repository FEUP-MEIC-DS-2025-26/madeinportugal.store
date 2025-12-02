from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import traceback

# Send keybinds N,P,O,I,A and visit the resulting subpages, then return
VENDOR_DASHBOARD_URL = "https://microfrontend-host-1054126107932.europe-west1.run.app/vendor/dashboard"
REGISTER_URL = "https://microfrontend-host-1054126107932.europe-west1.run.app/vendor/registration"

browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 900)


def scroll_full_page(duration=2.0, steps=10):
    """Scroll down the page in steps over `duration` seconds so a human can see content."""
    try:
        height = browser.execute_script("return document.body.scrollHeight") or 0
        if not height:
            return
        for i in range(steps):
            y = int(height * (i + 1) / steps)
            browser.execute_script("window.scrollTo(0, arguments[0]);", y)
            time.sleep(max(0.01, duration / steps))
        # pause at bottom briefly
        time.sleep(0.3)
        # scroll back to top so subsequent screenshots/navigation start at top
        browser.execute_script("window.scrollTo(0, 0);")
    except Exception:
        pass


def visit_vendor_dashboard(keys=('n', 'p', 'o', 'i', 'a')):
    browser.get(VENDOR_DASHBOARD_URL)
    time.sleep(2)
    # scroll so a user can see the whole page briefly
    scroll_full_page(duration=2.0, steps=12)
    origin = browser.current_url
    print('Opened dashboard:', origin)
    time.sleep(2)


def fill_registration():
    """Open the dedicated registration page (`REGISTER_URL`), then fill and submit its form."""
    print('Opening registration page:', REGISTER_URL)
    try:
        browser.get(REGISTER_URL)
        time.sleep(2)
        scroll_full_page(duration=2.0, steps=12)
    except Exception as e:
        print('Error navigating to REGISTER_URL:', e)
        return

    print('Attempting to fill registration form...')
    time.sleep(2)
    try:
        # prefer a register-form if present
        try:
            form = browser.find_element(By.CSS_SELECTOR, 'form.register-form')
        except Exception:
            form = browser.find_element(By.TAG_NAME, 'form')

        # simple mapping of expected fields
        values = {
            'name': 'Automation Store',
            'website': 'https://example.test',
            'about': 'Automated store for testing.',
            'owner_name': 'Automation Owner',
            'email': 'vendor+test@example.com',
            'phone': '+351912345678',
            'country': 'Portugal',
            'tax_id': '123456789'
        }

        for key, val in values.items():
            print(f"Filling field '{key}' with value '{val}'...")
            try:
                el = form.find_element(By.NAME, key)
                tag = el.tag_name.lower()
                if tag == 'select':
                    try:
                        Select(el).select_by_visible_text(val)
                    except Exception:
                        try:
                            Select(el).select_by_index(1)
                        except Exception:
                            pass
                else:
                    el.clear()
                    el.send_keys(val)
                time.sleep(0.5)
            except Exception:
                try:
                    el = form.find_element(By.ID, key)
                    el.clear()
                    el.send_keys(val)
                except Exception:
                    # try placeholder/aria-label
                    try:
                        el = form.find_element(By.XPATH, f".//input[contains(@placeholder, '{key}') or contains(@aria-label, '{key}')] | .//textarea[contains(@placeholder, '{key}') or contains(@aria-label, '{key}')]")
                        el.clear()
                        el.send_keys(val)
                    except Exception:
                        pass

        # fill textareas
        try:
            textareas = form.find_elements(By.TAG_NAME, 'textarea')
            answer = 'We deliver via local courier and tracked postal services.'
            for ta in textareas:
                try:
                    ta.clear()
                    ta.send_keys(answer)
                except Exception:
                    pass
                time.sleep(0.5)
        except Exception:
            pass

        # submit
        try:
            submit = form.find_element(By.XPATH, ".//button[@type='submit'] | .//button[contains(normalize-space(.),'Submit')]")
            try:
                submit.click()
            except Exception:
                browser.execute_script('arguments[0].click();', submit)
            time.sleep(6)
            print('Submitted registration form (attempted)')
        except Exception:
            print('No submit button found')

    except Exception as e:
        print('fill_registration error:', e)


if __name__ == '__main__':
    try:
        visit_vendor_dashboard()
        fill_registration()
    finally:
        browser.quit()

