#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os
import re

from multiprocessing import Process

def get_already_send():
    pattern = re.compile(r"^already_send_\d+\.txt$")
    already_send = []
    # List all files in the current directory and filter by pattern
    for filename in os.listdir("."):
        if pattern.match(filename):
            file = open(filename,'r',encoding="utf-8")
            lines = file.readlines()
            for line in lines:
                already_send.append(line.strip('\n'))
    already_send = [name for name in already_send if name.startswith("exclude:")==False]

    return already_send

def main(part: int, parts: int) -> None:
    contact_url = "https://chat.line.biz/Uc8c1340a847e08c2be8c06a4e6667ff6/contact"
    # label_name = "已成交客戶"
    outputfile = open(f"output_{part}.txt", "w",encoding="utf-8")
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

    # select scroll container
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "content")))
    scroll_container = driver.find_element(By.ID, "content")

    time.sleep(2)
    
    already_send = get_already_send()
    names_text = open("names.txt", "r",encoding="utf-8").readlines() # 要先跑 get_all_names.py
    names_text = [name.rstrip('\n') for name in names_text]
    names_text = [name for name in names_text if name not in already_send]
    # select group
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'select')))
    select_element = driver.find_element(By.TAG_NAME,'select')
    select_element.click()
    time.sleep(1)
    for i in range(1):
        select_element.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
    select_element.send_keys(Keys.ENTER)
    time.sleep(2)

    # time.sleep(1)
    # 每個process只處理{parts}分之一的名單
    names_text = [name for idx, name in enumerate(names_text) if idx % parts == part]
    for idx, name in enumerate(tqdm(names_text)):
        if idx > len(names_text)//2:
            name_sort = driver.find_element(By.XPATH,f"//thead//span[text()='姓名']")
            driver.execute_script("arguments[0].click();", name_sort)
            time.sleep(1)

        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f"//table/tbody")))
        table = driver.find_element(By.XPATH,f"//table/tbody")
        table_html = driver.execute_script("return arguments[0].innerHTML;", table)
        scroll_container = driver.find_element(By.ID, "content")

        time.sleep(1)
        is_exclude = True
        if name not in table_html:
            # scroll to the name
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "content")))
            time.sleep(1)
            limit = 50
            count = 0
            while count < limit:
                driver.execute_script("arguments[0].scrollTop += 800;", scroll_container)
                time.sleep(1)
                found_names = driver.find_elements(By.XPATH,f'//span[@data-emoji-width and text()="{name}"]')
                if len(found_names) > 0:
                    is_exclude = False
                    break
                count += 1
        else:
            is_exclude = False

        if not is_exclude:
            # 按下聊天按鈕, 進到聊天室
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,f'//span[@data-emoji-width and text()="{name}"]/../../../../../..//td[contains(.,"聊天")]//a')))
            chat = driver.find_element(By.XPATH,f'//span[@data-emoji-width and text()="{name}"]/../../../../../..//td[contains(.,"聊天")]//a')
            driver.execute_script("arguments[0].click();", chat)
            outputfile.write(name+'\n')
            print('name: '+ name)
            time.sleep(1)
            # send message
            message = """
#免費實體講座
未來零售已來想在市場中保持領先、即時洞察消費者意圖，並透過數據分析和AI科技提升行銷成效與顧客價值嗎
【AI戰略 x 未來零售—運用創新思維養成企業整合力】

這場講座將帶你進入AI驅動的零售轉型新時代並發掘數據整合與會員經營的全新視角。從數據探勘、AI科技應用、MarTech 整合力，到未來購物趨勢的預見，帶領企業制定精準的零售策略！

立即報名，搶先掌握AI科技引領的智慧零售新機遇
https://forms.gle/oJP2GdLEkc1iKAaD9

講座圖片
https://reurl.cc/E6kzRn

講座亮點搶先看
1.制定零售轉型策略：運用AI科技與數據驅動，及時應對市場變化

2.提升購物體驗：即時洞察消費者偏好，推薦高關聯商品

3.精準個性化推廣：分析會員數據，量身定制品牌內容，增強顧客黏著度

4.行銷專家 & 知名品牌 分享成功案例與實戰經驗

業界講師陣容
#Showmore 網路開店平台｜Al 加持精準行銷，掌握銷售成長新契機
營運長 / 李浩煒

#KPMG 安侯企管｜邁向負責任 Al 的新零售轉型藍圖
數位創新協理 / 林大中

#阿物科技｜與 Al共舞，掌握銷售智勝關鞬
行銷副總/ 陳岱旻

#Migo Data Solutions｜Al助力活化會員池，品牌數據資產再增值
總經理/ 陳俊甫

這是一次提升品牌價值的絕佳機會！立即報名，與業界精英共聚一堂，掌握最新科技與數據整合的零售策略，迎接成長新未來！
活動資訊
報名連結： https://forms.gle/oJP2GdLEkc1iKAaD9

活動時間：11/20 (三) 14:00-16:00
活動地點：大倉久和 3F 夏秋冬廳

#Showmore #KPMG安侯企管 #阿物科技 #MigoDataSolutions
#AI智慧零售 #未來零售 #個性化行銷 #消費趨勢 #精準行銷 #數據整合        
"""
            message_lines = message.strip().split("\n")
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "editor")))
            textarea = driver.execute_script("return document.querySelector('#editor').shadowRoot.querySelector('textarea')")
            for line in message_lines:
                textarea.send_keys(line)
                textarea.send_keys(Keys.SHIFT, Keys.ENTER)
            textarea.send_keys(Keys.ENTER)
        else:
            outputfile.write('exclude: '+name+'\n')
            print('exclude: '+name)

        # redirect to contact
        time.sleep(1)
        driver.get(contact_url)
        time.sleep(1)
        #select group
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'select')))
        select_element = driver.find_element(By.TAG_NAME,'select')
        select_element.click()
        time.sleep(1)
        for i in range(1):
            select_element.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
        select_element.send_keys(Keys.ENTER)
        time.sleep(1)

if __name__ == '__main__':
    parts = 8
    processes = []
    for i in range(parts):
        p = Process(target=main, args=(i,parts))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
