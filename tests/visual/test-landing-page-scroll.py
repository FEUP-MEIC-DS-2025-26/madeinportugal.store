from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# URLs to use
landing_page = 'https://madeinportugal.store'

# start session
browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 960)

def scroll_landing_page_slowly():
    """
    Navigate to the landing page and scroll slowly from top to bottom
    """
    print("[+] - 🚀 Starting landing page scroll test...")
    
    # Navigate to landing page
    try:
        browser.get(landing_page)
        print(f"[+] - 📄 Opened landing page: {landing_page}")
        time.sleep(3)  # Wait for page to load
    except Exception as e:
        print(f"[+] - ❌ FAILED to open landing page: {e}")
        return False

    # Get page dimensions
    try:
        total_height = browser.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
        viewport_height = browser.execute_script("return window.innerHeight")
        
        print(f"[+] - 📏 Page height: {total_height}px, Viewport height: {viewport_height}px")
    except Exception as e:
        print(f"[+] - ⚠️ Could not get page dimensions: {e}")
        total_height = 5000  # fallback value
        viewport_height = 960

    # Calculate scroll increment (scroll by small chunks)
    scroll_increment = viewport_height // 2  # Scroll by quarter viewport height each time
    current_position = 0
    
    print(f"[+] - 📜 Starting slow scroll (increment: {scroll_increment}px)...")
    
    # Scroll slowly from top to bottom
    while current_position < total_height:
        try:
            # Scroll down by increment
            browser.execute_script(f"window.scrollTo(0, {current_position});")
            
            # Wait between scrolls to simulate slow scrolling
            time.sleep(1.5)  # Adjust this value to make scrolling faster/slower
            
            current_position += scroll_increment
            
            # Get actual scroll position to handle cases where we can't scroll further
            actual_position = browser.execute_script("return window.pageYOffset")
            
            print(f"[+] - 📍 Scrolled to position: {actual_position}px")
            
            # If we haven't moved, we've reached the bottom
            if current_position > scroll_increment and actual_position < current_position - scroll_increment:
                print("[+] - 🏁 Reached bottom of page")
                break
                
        except Exception as e:
            print(f"[+] - ⚠️ Error during scroll: {e}")
            break
    
    # Pause at the bottom
    print("[+] - ⏸️ Pausing at bottom for 3 seconds...")
    time.sleep(3)
    
    # Scroll back to top slowly
    print("[+] - ⬆️ Scrolling back to top...")
    while current_position > 0:
        try:
            current_position -= scroll_increment
            if current_position < 0:
                current_position = 0
                
            browser.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(1)  # Faster scroll back up
            
            actual_position = browser.execute_script("return window.pageYOffset")
            print(f"[+] - 📍 Scrolled back to position: {actual_position}px")
            
        except Exception as e:
            print(f"[+] - ⚠️ Error during scroll back: {e}")
            break
    
    # Final scroll to top
    try:
        browser.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        print("[+] - 🔝 Returned to top of page")
    except Exception as e:
        print(f"[+] - ⚠️ Error scrolling to top: {e}")
    
    print("[+] - ✅ Landing page scroll test completed successfully!")
    return True

def test_page_elements_during_scroll():
    """
    Test that key elements are visible during scroll
    """
    print("[+] - 🔍 Testing page elements visibility during scroll...")
    
    # Navigate to landing page
    try:
        browser.get(landing_page)
        time.sleep(3)
    except Exception as e:
        print(f"[+] - ❌ FAILED to open landing page: {e}")
        return False
    
    # Scroll and check for common elements
    scroll_positions = [0, 500, 1000, 1500, 2000, 2500]  # Test at different scroll positions
    
    for position in scroll_positions:
        try:
            browser.execute_script(f"window.scrollTo(0, {position});")
            time.sleep(2)
            
            # Check if any key elements are visible
            elements_found = []
            
            # Look for common landing page elements
            try:
                if browser.find_elements(By.TAG_NAME, "nav"):
                    elements_found.append("navigation")
            except:
                pass
            
            try:
                if browser.find_elements(By.TAG_NAME, "header"):
                    elements_found.append("header")
            except:
                pass
                
            try:
                if browser.find_elements(By.TAG_NAME, "footer"):
                    elements_found.append("footer")
            except:
                pass
                
            try:
                if browser.find_elements(By.XPATH, "//button[contains(text(),'Login')]"):
                    elements_found.append("login button")
            except:
                pass
            
            if elements_found:
                print(f"[+] - 📍 At position {position}px, found: {', '.join(elements_found)}")
            else:
                print(f"[+] - 📍 At position {position}px, no specific elements detected")
                
        except Exception as e:
            print(f"[+] - ⚠️ Error at position {position}px: {e}")
    
    # Return to top
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    
    print("[+] - ✅ Page elements test completed!")
    return True

def run_all_tests():
    """
    Main function to run all scroll tests
    """
    print("[+] - 🎯 Running Landing Page Scroll Tests")
    print("=" * 50)
    
    try:
        # Test 1: Basic scroll functionality
        if not scroll_landing_page_slowly():
            print("[+] - ❌ Basic scroll test failed")
            return False
        
        print("\n" + "-" * 50 + "\n")
        
        # Test 2: Element visibility during scroll
        if not test_page_elements_during_scroll():
            print("[+] - ❌ Element visibility test failed")
            return False
        
        print("\n" + "=" * 50)
        print("[+] - 🎉 All tests completed successfully!")
        
        # Keep browser open for a moment
        time.sleep(5)
        
    except Exception as e:
        print(f"[+] - ❌ Unexpected error during tests: {e}")
        return False
    
    finally:
        # Close browser
        try:
            browser.quit()
            print("[+] - 🚪 Browser closed")
        except:
            pass
    
    return True

if __name__ == "__main__":
    run_all_tests()
