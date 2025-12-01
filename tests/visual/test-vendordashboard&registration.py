from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Send keybinds N,P,O,I,A and visit the resulting subpages, then return
VENDOR_DASHBOARD_URL = "https://vendor-frontend-786191016787.europe-west1.run.app/dashboard"

browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 900)


def visit_vendor_dashboard(keys=('n', 'p', 'o', 'i', 'a')):
    browser.get(VENDOR_DASHBOARD_URL)
    time.sleep(1)
    origin = browser.current_url
    print('Opened dashboard:', origin)

    # ensure a body element exists
    try:
        body = browser.find_element(By.TAG_NAME, 'body')
    except Exception:
        body = None

    for k in keys:
        try:
            if body:
                body.send_keys(k)
            else:
                # fallback: send via execute_script
                browser.execute_script("document.body.dispatchEvent(new KeyboardEvent('keydown',{key: arguments[0]}));", k)
        except Exception:
            try:
                browser.execute_script("document.body.dispatchEvent(new KeyboardEvent('keydown',{key: arguments[0]}));", k)
            except Exception:
                pass

        # wait briefly for navigation or new tab
        time.sleep(1)

        handled = False
        # if a new tab opened, switch to it, log, close it, return to origin
        if len(browser.window_handles) > 1:
            orig_handle = browser.current_window_handle
            for h in browser.window_handles:
                if h != orig_handle:
                    browser.switch_to.window(h)
                    time.sleep(0.7)
                    print(f"Key '{k}' opened new tab: {browser.current_url}")
                    # If this is the registration flow (n), try filling the form
                    if k.lower() == 'n':
                        try:
                            fill_registration()
                        except Exception as e:
                            print('Registration fill error on new tab:', e)
                        time.sleep(0.5)
                    try:
                        browser.close()
                    except Exception:
                        pass
                    browser.switch_to.window(orig_handle)
                    handled = True
                    break

        # if same-tab navigation occurred
        if not handled:
            try:
                cur = browser.current_url
                if cur != origin:
                    print(f"Key '{k}' navigated to: {cur}")
                    # if this is registration, try filling before going back
                    if k.lower() == 'n':
                        try:
                            fill_registration()
                        except Exception as e:
                            print('Registration fill error on same tab:', e)
                        time.sleep(0.5)
                    # go back to origin
                    try:
                        browser.back()
                        time.sleep(0.5)
                        print(f"Returned from key '{k}'")
                    except Exception:
                        pass
                    handled = True
                else:
                    print(f"Key '{k}' did not navigate")
            except Exception:
                print(f"Key '{k}' handling error")

        # brief pause between keys
        time.sleep(0.5)


def fill_registration():
    """Attempt to fill a visible registration form on the current page and submit."""
    print('Attempting to fill registration form...')
    time.sleep(0.5)
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
        except Exception:
            pass

        # submit
        try:
            submit = form.find_element(By.XPATH, ".//button[@type='submit'] | .//button[contains(normalize-space(.),'Submit')]")
            try:
                submit.click()
            except Exception:
                browser.execute_script('arguments[0].click();', submit)
            time.sleep(1)
            print('Submitted registration form (attempted)')
        except Exception:
            print('No submit button found')

    except Exception as e:
        print('fill_registration error:', e)


if __name__ == '__main__':
    try:
        visit_vendor_dashboard()
    finally:
        browser.quit()

