from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

host_MIPS_Frontend = 'https://microfrontend-host-1054126107932.europe-west1.run.app'

browser = webdriver.Chrome()
browser.set_window_position(0, 0)
browser.set_window_size(1280, 800)

def force_click_element(element):
    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", element)

def find_button_by_scanning(target_text):
    print(f"[Scan] A varrer a página por botões com texto '{target_text}'...")
    
    candidates = browser.find_elements(By.TAG_NAME, "button") + \
                 browser.find_elements(By.TAG_NAME, "a") + \
                 browser.find_elements(By.CSS_SELECTOR, "[role='button']")
                 
    for btn in candidates:
        try:
            txt = btn.text or btn.get_attribute("innerText")
            if txt and target_text in txt:
                print(f"[Scan] Encontrado! Texto: '{txt}'")
                return btn
        except:
            continue
    return None

def robust_click(text_to_find, description):
    print(f"\n[Ação] A tentar clicar em: '{description}'...")
    wait = WebDriverWait(browser, 10)
    
    try:
        xpath = f"//*[contains(normalize-space(.), '{text_to_find}')]"
        
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        
        target = elements[-1]
        
        print(f"[XPath] Elemento encontrado via XPath.")
        force_click_element(target)
        return True
    except Exception as e:
        print(f"[XPath] Falhou. A tentar varredura manual...")

    target = find_button_by_scanning(text_to_find)
    if target:
        force_click_element(target)
        print(f"[Scan] Clique forçado com sucesso.")
        return True
    
    print(f"Não foi possível encontrar o botão '{text_to_find}'.")
    return False

def authenticate_host(): 
    print("A carregar Host...")
    try:
        if "microfrontend-host" not in browser.current_url:
            browser.get(host_MIPS_Frontend)
    except:
        browser.get(host_MIPS_Frontend)
    time.sleep(5) 

def navigate_product_page():
    authenticate_host()

    print("\n--- PASSO 1: ENTRAR NA PÁGINA DE PRODUTO ---")
    
    success = robust_click("PRODUCT PAGE CLASS 2 GROUP 2", "Botão Menu Produto")

    if not success:
        print("Abortando: Falha crítica na navegação.")
        browser.quit()
        return

    print("\n--- PASSO 2: VALIDAR PÁGINA ---")
    wait = WebDriverWait(browser, 15)
    try:
        title = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        print(f"Sucesso! Estamos na página: {title.text}")
        
        browser.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)

        print("\n--- PASSO 3: INTERAÇÃO ---")
        robust_click("COMPRAR", "Botão Comprar")

    except Exception as e:
        print(f"Erro na validação da página: {e}")
        print(f"URL Atual: {browser.current_url}")

    print("\nTeste concluído. A fechar...")
    time.sleep(5)
    browser.quit()

if __name__ == "__main__":
    navigate_product_page()