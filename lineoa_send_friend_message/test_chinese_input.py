from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import pickle
import time
from selenium.webdriver.common.keys import Keys

contact_url = "https://chat.line.biz/Uec958da29ea7f271b1c8fde2792b95b0/chat/C926d304c4635f8d37b992a951d8c8f82"

options = webdriver.EdgeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自動化偵測
# options.add_argument("--window-size=1920,1080")  # 設定視窗大小
driver = webdriver.Edge(options=options)
driver.maximize_window()
driver.get(contact_url)
with open("./cookies.pkl", "rb") as file:
    cookies = pickle.load(file)
    for cookie in cookies:
        if cookie['domain'] == '.line.biz':
            driver.add_cookie(cookie)
driver.get(contact_url)
driver.refresh()

message = "你好，世界"
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "editor")))
textarea = driver.execute_script("return document.querySelector('#editor').shadowRoot.querySelector('textarea')")
textarea.send_keys(message)
textarea.send_keys(Keys.ENTER)