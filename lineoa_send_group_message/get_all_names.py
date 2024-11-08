#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

contact_url = "https://chat.line.biz/Uc8c1340a847e08c2be8c06a4e6667ff6/contact"
label_name = "已成交客戶"

# login
options = webdriver.EdgeOptions()
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

#select group
# WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'select')))
# select_element = driver.find_element(By.TAG_NAME,'select')
# select_element.click()
# time.sleep(1)
# for i in range(3):
#     select_element.send_keys(Keys.ARROW_DOWN)
# select_element.send_keys(Keys.ENTER)

time.sleep(1)

# select scroll container
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "content")))
scroll_container = driver.find_element(By.ID, "content")

time.sleep(2)

#scroll to the bottom
max_attempts = 1000
attempt = 0
last_height = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
while attempt < max_attempts:
    driver.execute_script("arguments[0].scrollTop += 800;", scroll_container)
    time.sleep(0.8)
    new_height = driver.execute_script("return arguments[0].scrollTop;", scroll_container)
    if new_height == last_height:
        break
    last_height = new_height
    attempt += 1

# get names
names = driver.find_elements(By.XPATH,f"//table/tbody/tr/td[position()=2 and contains(.,'{label_name}')]/../td[1]//span[@data-emoji-width]")
names_text = [name.get_attribute("innerText") for name in names]

outputfile = open('names.txt', 'w', encoding='utf-8')
outputfile.write('\n'.join(names_text))

