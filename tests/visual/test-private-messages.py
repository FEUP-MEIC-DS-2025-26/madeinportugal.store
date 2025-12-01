from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

landing_page = "https://madeinportugal.store"
username = "user"
password = "pass"

browser = webdriver.Chrome()
browser.set_window_size(1280, 960)

wait = WebDriverWait(browser, 10)

melancholic_messages = [
    "Há dias em que o peso da tua ausência é tão grande que até o ar parece desistir de entrar.",
    "Guardo tudo por dentro, e às vezes parece que o silêncio me engole antes que eu encontre forças para falar.",
    "A tua falta espalhou-se pela minha rotina como uma sombra que não consigo afastar.",
    "Às vezes acordo e demoro um momento a lembrar-me que continuas longe… e esse momento dói mais do que devia.",
    "É estranho como algo que acabou há tanto tempo ainda consegue mexer com tudo o que eu sou hoje.",
    "O mundo segue e eu sigo também, mas com uma parte de mim arrastada pelo chão.",
    "Sinto que a vida continuou sem me perguntar se eu estava pronto para seguir também.",
    "Há memórias tuas que pesam tanto que até as coisas simples se tornam difíceis.",
    "A tua distância transformou o que era leve em algo espesso, quase impossível de atravessar.",
    "Já tentei encher o vazio que deixaste, mas ele insiste em alargar-se sempre que penso em ti.",
    "Às vezes sinto que carrego demasiado… e mesmo assim continuo, porque não há outro caminho.",
    "É cansativo sentir tantas coisas ao mesmo tempo e não poder explicar nenhuma delas.",
    "A saudade que tenho de ti não é suave é densa, pesada, lenta, difícil de suportar.",
    "O silêncio que ficou depois de ti é tão profundo que parece ter eco próprio.",
    "Há momentos em que tudo parece tão distante que até eu me sinto desfocado.",
    "Percebi que certas ausências não se superam; apenas aprendemos a conviver com o peso.",
    "Às vezes sinto que estou num lugar cheio de gente mas completamente sozinho por dentro.",
    "A tua falta tornou-se uma presença tão constante que já nem sei distinguir o que sinto.",
    "O tempo passa, mas o peso permanece não cresce, não diminui, só fica.",
    "Mesmo quando tento não pensar, a tua ausência encontra forma de se infiltrar no meu dia."
]

def login():
    browser.get(landing_page)
    wait = WebDriverWait(browser, 20)

    login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Login')]")
    ))
    browser.execute_script("arguments[0].click();", login_btn)

    user_input = wait.until(EC.presence_of_element_located((By.XPATH, "//form//input[1]")))
    pass_input = wait.until(EC.presence_of_element_located((By.XPATH, "//form//input[2]")))

    user_input.send_keys(username)
    pass_input.send_keys(password)

    submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//form//button[@type='submit']")))
    browser.execute_script("arguments[0].click();", submit_btn)

    time.sleep(2)

def go_to_my_conversations():
    menu_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Open user menu']"))
    )
    menu_btn.click()
    time.sleep(2)

    conversations_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'My Conversations')]"))
    )
    conversations_link.click()
    time.sleep(2)

    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(2)

def open_chat():
    conversation_item = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'MuiListItemButton-root')][.//strong[text()='Jane Doe']]")
        )
    )

    conversation_item.click()
    time.sleep(2)

def send_message():
    msg_box = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type your message here']"))
    )

    random_message = random.choice(melancholic_messages)
    msg_box.send_keys(random_message)
    time.sleep(1)

    send_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )

    send_btn.click()
    time.sleep(1)

def main():
    time.sleep(5)
    login()
    go_to_my_conversations()
    open_chat()
    send_message()
    time.sleep(20)
    browser.quit()

main()