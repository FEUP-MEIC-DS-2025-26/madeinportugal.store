"""
E2E tests for the Review Analyzer application.
Tests landing page, analysis flow, dashboard components, and API integration.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuration
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://mips-frontend-web-757586835676.europe-west1.run.app")
BACKEND_URL = os.environ.get("BACKEND_URL", "https://comment-analyzer-api-evf254kevq-ew.a.run.app")
WAIT_TIMEOUT = 15

# Start browser session
browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1024, 768)


def navigate_to_frontend():
    """Navigate to the Review Analyzer frontend."""
    print("Navigating to Review Analyzer...")
    browser.get(FRONTEND_URL)
    time.sleep(2)


def wait_for_products_dropdown():
    """Wait for the products dropdown to be populated."""
    print("Waiting for products dropdown...")
    dropdown = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "select"))
    )
    WebDriverWait(browser, WAIT_TIMEOUT).until(
        lambda d: len(dropdown.find_elements(By.TAG_NAME, "option")) > 0
    )
    return dropdown


def click_analyze_button():
    """Click the Analyze Comments button."""
    print("Clicking Analyze Comments button...")
    analyze_button = browser.find_element(
        By.XPATH, "//button[contains(text(), 'Analyze')]"
    )
    analyze_button.click()


def wait_for_analysis_complete():
    """Wait for the analysis to complete."""
    print("Waiting for analysis to complete...")
    WebDriverWait(browser, 30).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "//button[contains(text(), 'Analyze')]"), "Analyze Comments"
        )
    )


def run_analysis():
    """Full analysis flow: navigate, wait for products, click analyze, wait for completion."""
    navigate_to_frontend()
    wait_for_products_dropdown()
    click_analyze_button()
    wait_for_analysis_complete()


def scroll_down():
    """Scroll to bottom of page."""
    print("Scrolling down...")
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def scroll_up():
    """Scroll to top of page."""
    print("Scrolling up...")
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)


def test_header_and_analyze_button():
    """Test 1: Verify the main header and analyze button are displayed."""
    print("\n=== Test 1: Header and Analyze Button ===")
    navigate_to_frontend()
    
    header = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    assert "Review Analyzer" in header.text, "Header should contain 'Review Analyzer'"
    print("✓ Header found")
    
    button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Analyze')]")
        )
    )
    assert button.is_displayed(), "Analyze button should be visible"
    print("✓ Analyze button found")


def test_products_load_from_api():
    """Test 2: Verify products are fetched from Jumpseller API."""
    print("\n=== Test 2: Products Load from API ===")
    navigate_to_frontend()
    
    dropdown = wait_for_products_dropdown()
    options = dropdown.find_elements(By.TAG_NAME, "option")
    assert len(options) > 0, "Jumpseller API should return products"
    print(f"✓ Found {len(options)} products in dropdown")


def test_analyze_shows_loading_state():
    """Test 3: Verify clicking 'Analyze Comments' shows loading state."""
    print("\n=== Test 3: Loading State ===")
    navigate_to_frontend()
    
    dropdown = wait_for_products_dropdown()
    
    # Select first product if multiple options
    select = Select(dropdown)
    if len(select.options) > 1:
        select.select_by_index(1)
    
    analyze_button = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Analyze')]")
        )
    )
    analyze_button.click()
    
    # Check for loading state
    WebDriverWait(browser, 5).until(
        lambda d: "Analyzing" in analyze_button.text
        or analyze_button.find_elements(By.CLASS_NAME, "loading-spinner")
    )
    print("✓ Loading state detected")
    
    # Wait for completion
    wait_for_analysis_complete()
    print("✓ Analysis completed")


def test_sentiment_analysis_results():
    """Test 4: Verify Google Cloud NLP API provides sentiment analysis."""
    print("\n=== Test 4: Sentiment Analysis Results ===")
    run_analysis()
    
    page_text = browser.find_element(By.TAG_NAME, "body").text
    
    assert "Sentiment Distribution" in page_text, "Should show Sentiment Distribution"
    print("✓ Sentiment Distribution section found")
    
    # At least one sentiment type should appear in results
    has_sentiment = (
        page_text.count("Positive") > 1
        or page_text.count("Negative") > 1
        or page_text.count("Neutral") > 1
    )
    assert has_sentiment, "Should display sentiment categories"
    print("✓ Sentiment categories found")


def test_topic_extraction():
    """Test 5: Verify Google Cloud NLP API extracts topics."""
    print("\n=== Test 5: Topic Extraction ===")
    run_analysis()
    
    page_text = browser.find_element(By.TAG_NAME, "body").text
    
    assert "Topics Mentioned" in page_text, "Should show Topics Mentioned"
    print("✓ Topics Mentioned section found")
    
    assert "Impact by Topic" in page_text, "Should show Impact by Topic"
    print("✓ Impact by Topic section found")


def test_all_dashboard_sections():
    """Test 6: Verify all main dashboard sections appear after analysis."""
    print("\n=== Test 6: All Dashboard Sections ===")
    run_analysis()
    scroll_down()
    
    page_text = browser.find_element(By.TAG_NAME, "body").text
    
    sections = ["Topics Mentioned", "Positive Aspects", "Negative Aspects", "Analyzed Comments"]
    for section in sections:
        assert section in page_text, f"Should show {section}"
        print(f"✓ {section} section found")
    
    scroll_up()


def test_comments_with_ratings():
    """Test 7: Verify comments show ratings and sentiment indicators."""
    print("\n=== Test 7: Comments with Ratings ===")
    run_analysis()
    scroll_down()
    
    page_text = browser.find_element(By.TAG_NAME, "body").text
    
    # Check for rating indicators
    assert "⭐" in page_text or "/5" in page_text, "Should display ratings"
    print("✓ Rating indicators found")
    
    # Check for sentiment badges
    has_sentiment = (
        page_text.count("Positive") > 1
        or page_text.count("Negative") > 1
        or page_text.count("Neutral") > 1
    )
    assert has_sentiment, "Should display sentiment badges"
    print("✓ Sentiment badges found")
    
    scroll_up()


def run_all_tests():
    """Run all Review Analyzer E2E tests."""
    print("=" * 60)
    print("REVIEW ANALYZER E2E TESTS")
    print("=" * 60)
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Backend URL: {BACKEND_URL}")
    
    try:
        test_header_and_analyze_button()
        test_products_load_from_api()
        test_analyze_shows_loading_state()
        test_sentiment_analysis_results()
        test_topic_extraction()
        test_all_dashboard_sections()
        test_comments_with_ratings()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    finally:
        browser.quit()


# Run the tests
run_all_tests()
