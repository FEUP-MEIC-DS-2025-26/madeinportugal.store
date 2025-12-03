from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random


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

def go_to_my_conversations(browser):
    menu_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Open user menu']"))
    )
    menu_btn.click()
    time.sleep(2)

    conversations_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'My Conversations')]"))
    )
    conversations_link.click()
    time.sleep(2)

    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(2)

def open_chat(browser):
    conversation_item = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'MuiListItemButton-root')][.//strong[text()='Jane Doe']]")
        )
    )

    conversation_item.click()
    time.sleep(2)

def send_message(browser):
    msg_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Type your message here']"))
    )

    random_message = random.choice(melancholic_messages)
    msg_box.send_keys(random_message)
    time.sleep(1)

    send_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )

    send_btn.click()
    time.sleep(5)

    current_tab = browser.current_window_handle
    all_tabs = browser.window_handles

    if len(all_tabs) > 1:
        for tab in all_tabs:
            if tab != current_tab:
                previous_tab = tab
                break

        browser.close()
        browser.switch_to.window(previous_tab)


def navigate_private_messages(browser):
    go_to_my_conversations(browser)
    open_chat(browser)
    send_message(browser)