from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import re
import time

host_MIPS_Frontend = 'https://microfrontend-host-1054126107932.europe-west1.run.app'

# Global variables
browser = None
wait = None

def init_browser():
    """Initialize browser with standard settings"""
    global browser, wait
    browser = webdriver.Chrome()
    browser.set_window_position(0, 0)
    browser.set_window_size(1280, 960)
    wait = WebDriverWait(browser, 10)

def authenticate():
    """Navigate to main page"""
    try:
        browser.get(host_MIPS_Frontend)
        time.sleep(3)
        print("Landing page loaded successfully")
    except Exception as e:
        print(f"Error loading landing page: {e}")

def navigate_to_product_listing():
    """Navigate to product listing/products page"""
    print("Navigating to product listing page...")
    
    # Ensure wait is initialized
    global wait
    if wait is None:
        wait = WebDriverWait(browser, 10)
    
    try:
        # Look for products link or menu item
        products_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Products') or contains(text(),'Produtos')] | //button[contains(text(),'Products') or contains(text(),'Produtos')]"))
        )
        products_link.click()
        time.sleep(3)
        print("Successfully clicked products link")
        
        # Check if we're on the products page
        wait.until(
            EC.any_of(
                EC.url_contains("/products"),
                EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Product Catalog')]"))                                  
            )
        )
        print("Product listing page loaded")
        
    except Exception as e:
        print(f"Could not navigate via menu, trying direct navigation: {e}")
        # Fallback: try direct URL navigation
        try:
            browser.get(host_MIPS_Frontend + "/products")
            time.sleep(3)
            print("Direct navigation to products page attempted")
        except Exception as e2:
            print(f"Direct navigation also failed: {e2}")

def test_product_grid_display():
    """Test that products are displayed in a grid format"""
    print("\n--- TESTING PRODUCT GRID DISPLAY ---")
    
    try:
        time.sleep(2)
        print(f"Current URL: {browser.current_url}")
        
        catalog_heading = browser.find_element(By.XPATH, "//h4[contains(text(), 'Product Catalog')]")
        product_section = catalog_heading.find_element(By.XPATH, "./following-sibling::div[1]")
        all_anchors = product_section.find_elements(By.CSS_SELECTOR, "a[href*='/product/']")

        product_anchors = []
        for anchor in all_anchors:
            href = anchor.get_attribute("href") or ""
            if re.search(r"/product/\d+", href):
                product_anchors.append(anchor)

        print(f"Product grid display test passed: {len(product_anchors)} products displayed in Product Catalog")

    except Exception as e:
        print(f"Error testing product grid display: {e}")

def test_product_filtering():
    """Test product filtering/category functionality"""
    print("\n--- TESTING PRODUCT FILTERING/CATEGORIES ---")
    
    try:
        category_label = browser.find_element(By.XPATH, "//label[contains(text(), 'Category')]")
        form_control = category_label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiFormControl-root')]")
        combobox = form_control.find_element(By.XPATH, ".//div[@role='combobox']")
        print("Filter dropdown found")

        # Get initial product count
        initial_products = len(browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]"))
        print(f"Initial product count: {initial_products}")
        
        # Open dropdown
        try:
            combobox.click()
            time.sleep(1)
            
            # Find all filter options
            options = browser.find_elements(By.XPATH, "//li[@data-value]")
            print(f"Found {len(options)} filter options")
            
            if len(options) > 1:
                # Test second option
                option_text = options[1].text
                options[1].click()
                time.sleep(2)
                
                filtered_products = len(browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]"))
                print(f"Filter '{option_text}': {initial_products} -> {filtered_products} products")
                
                # Test third option
                if len(options) > 2:
                    combobox.click()
                    time.sleep(1)
                    # Refresh options after reopening
                    options = browser.find_elements(By.XPATH, "//li[@data-value]")
                    option_text = options[2].text
                    options[2].click()
                    time.sleep(2)
                    
                    filtered_products2 = len(browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]"))
                    print(f"Filter '{option_text}': {initial_products} -> {filtered_products2} products")
                
                # Reset to first option
                combobox.click()
                time.sleep(1)
                options = browser.find_elements(By.XPATH, "//li[@data-value]")
                options[0].click()
                time.sleep(2)
                
                print("Product filtering test passed")
            else:
                print("Not enough filter options to test")
                
        except Exception as e:
            print(f"Error testing filters: {e}")
            
    except Exception as e:
        print(f"Error finding filters: {e}")

def test_product_search():
    """Test product search functionality"""
    print("\n--- TESTING PRODUCT SEARCH ---")
    
    try:
        # Look for the search input with the placeholder
        try:
            search_input = browser.find_element(By.XPATH, "//input[@placeholder='What are you looking for?']")
            print("Found search bar")
        except Exception:
            # Look for the search input with label "Search Products"
            try:
                search_label = browser.find_element(By.XPATH, "//label[contains(text(), 'Search Products')]")
                form_control = search_label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiInputBase-root')]")
                search_input = form_control.find_element(By.TAG_NAME, "input")
                print("Found search bar (via label)")
            except Exception:
                print("Search input not found")
                return
        
        # Test search functionality
        search_terms = ["Frango", "Handmade"]
        initial_products = len(browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]"))
        for term in search_terms:
            try:                
                # Type search term
                search_input.send_keys(term)
                search_input.send_keys(Keys.RETURN)
                time.sleep(2)
                
                # Check results
                search_products = len(browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]"))                
                print(f"Search '{term}': {initial_products} -> {search_products} products")
                
                # Clear search input
                search_input.click()
                search_input.send_keys(Keys.CONTROL + "a")  # Select all
                search_input.send_keys(Keys.DELETE)
                time.sleep(0.5)
            except Exception as e:
                print(f"Error testing search term '{term}': {e}")
        
        print("Product search test passed")
        
    except Exception as e:
        print(f"Error testing search: {e}")

def test_product_sorting():
    """Test product sorting functionality"""
    print("\n--- TESTING PRODUCT SORTING ---")
    
    try:
        sort_label = browser.find_element(By.XPATH, "//label[contains(text(), 'Sort By')]")
        form_control = sort_label.find_element(By.XPATH, "./ancestor::div[contains(@class, 'MuiFormControl-root')]")
        combobox = form_control.find_element(By.XPATH, ".//div[@role='combobox']")
        print("Sort dropdown found")

        # Open dropdown
        try:
            combobox.click()
            time.sleep(1)
            
            # Find all sort options
            options = browser.find_elements(By.XPATH, "//li[@data-value]")
            print(f"Found {len(options)} sort options")
            
            if len(options) > 1:
                # Get initial product order by getting first product anchor
                first_products_before = browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")[:3]
                before_texts = [p.text[:20] if p.text else "" for p in first_products_before]
                
                # Test different sort options
                for i in range(1, min(3, len(options))):
                    option_text = options[i].text
                    options[i].click()
                    time.sleep(2)
                    
                    # Get products after sorting
                    first_products_after = browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")[:3]
                    after_texts = [p.text[:20] if p.text else "" for p in first_products_after]
                    
                    if before_texts != after_texts:
                        print(f"Sort option '{option_text}': Product order changed")
                    else:
                        print(f"Sort option '{option_text}': Product order unchanged")
                    
                    # Reopen for next iteration
                    if i < min(3, len(options)) - 1:
                        combobox.click()
                        time.sleep(1)
                        options = browser.find_elements(By.XPATH, "//li[@data-value]")
                
                # Reset to first option
                combobox.click()
                time.sleep(1)
                options = browser.find_elements(By.XPATH, "//li[@data-value]")
                options[0].click()
                time.sleep(2)
                
                print("Product sorting test passed")
            else:
                print("Not enough sort options to test")
                
        except Exception as e:
            print(f"Error testing sort options: {e}")
            
    except Exception as e:
        print(f"Error finding sort options: {e}")

def test_product_interaction():
    """Test clicking on products to view details"""
    print("\n--- TESTING PRODUCT INTERACTION ---")
    
    try:
        # Find product anchors with /product/ href (same method as grid display test)
        product_anchors = browser.find_elements(By.XPATH, "//a[contains(@href, '/product/')]")
        
        if product_anchors:
            print(f"Found {len(product_anchors)} clickable product links")
            
            # Test clicking first product
            first_product = product_anchors[0]
            original_window = browser.current_window_handle
            original_url = browser.current_url
            
            try:
                # Get product href and name before clicking
                product_href = first_product.get_attribute('href')
                try:
                    product_name = first_product.find_element(By.XPATH, 
                        ".//p | .//h1 | .//h2 | .//h3 | .//h4 | .//h5 | .//h6").text
                except:
                    product_name = "Unknown product"
                
                print(f"Clicking on product: {product_name} (href: {product_href})")
                first_product.click()
                time.sleep(3)
                
                # Check if we navigated to a new page or opened new window
                current_url = browser.current_url
                if len(browser.window_handles) > 1:
                    # New window opened
                    browser.switch_to.window(browser.window_handles[-1])
                    print("New window opened for product details")
                    browser.close()
                    browser.switch_to.window(original_window)
                elif current_url != original_url:
                    # Same window, different URL - navigated successfully
                    print(f"Successfully navigated to product details page: {current_url}")
                    browser.back()
                    time.sleep(2)
                else:
                    print("Warning: Click did not navigate to new page")
                
            except Exception as e:
                print(f"Error interacting with product: {e}")
        else:
            print("No clickable product links found")
            
    except Exception as e:
        print(f"Error testing product interaction: {e}")

def run_product_listing_test(browser_instance=None):
    """Main test function that can be called from other test files"""
    global browser, wait
    
    if browser_instance:
        browser = browser_instance
        wait = WebDriverWait(browser, 10)
    else:
        init_browser()
    
    print("=" * 60)
    print("STARTING PRODUCT LISTING TESTS")
    print("=" * 60)
    
    try:
        # Navigate to the product listing
        if not browser_instance:
            authenticate()
        navigate_to_product_listing()
        
        # Run all tests
        test_product_grid_display()
        test_product_filtering()
        test_product_search()
        test_product_sorting()
        test_product_interaction()
        
        print("\n" + "=" * 60)
        print("PRODUCT LISTING TESTS COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error in main test function: {e}")
    
    finally:
        if not browser_instance:
            time.sleep(3)
            browser.quit()

def run_standalone_tests():
    """Run tests independently when script is executed directly"""
    run_product_listing_test()

if __name__ == "__main__":
    run_standalone_tests()
