from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support import expected_conditions as EC
import time

landing_page = 'https://madeinportugal.store'
browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 960)

def test_top_selling_products_visibility():
    """
    Test that Top Selling Products are visible during scroll
    """    
    # Navega para a página
    browser.get(landing_page)
    time.sleep(3)  # Espera a página carregar

    # Define posições de scroll onde vais testar
    scroll_positions = [0, 500, 1000, 1500, 2000]

    for position in scroll_positions:
        browser.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(2)  # Pequena pausa para renderização
        
        try:
            top_products = browser.find_elements(By.CSS_SELECTOR, "#products")
            
            if top_products:
                print(f"Top Selling Products are visible")
            else:
                print(f"Top Selling Products NOT visible")
        
        except Exception as e:
            print(f"Error checking top products")
    
    # Volta para o topo
    browser.execute_script("window.scrollTo(0, 0);")
    time.sleep(2)
    print("Top Selling Products visibility test completed")

def select_top_selling_category():
    """
    Navega para a landing page, encontra a section de top selling products
    e seleciona as outras categorias.
    """    
    browser.get(landing_page)
    time.sleep(3)
    
    try:
        # Finds products section
        products_section = browser.find_element(By.ID, "products")
        
        # Scroll until section is found
        browser.execute_script("arguments[0].scrollIntoView();", products_section)
        time.sleep(1)
        
        # Finds select inside section
        category_select_elem = products_section.find_element(By.TAG_NAME, "select")
        select = Select(category_select_elem)
        
        # Selects category
        select.select_by_visible_text("Azeites")
        time.sleep(2)
        select.select_by_visible_text("Queijos")
        time.sleep(2)
        select.select_by_visible_text("Doces")
        time.sleep(2)
        select.select_by_visible_text("Conservas")
        time.sleep(2)     
        select.select_by_visible_text("Vinhos")
        time.sleep(2)         
    except Exception as e:
        print(f"Error selecting category: {e}")

test_top_selling_products_visibility()

time.sleep(3)

select_top_selling_category()

browser.quit()
