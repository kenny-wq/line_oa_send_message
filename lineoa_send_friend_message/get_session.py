import pickle
from selenium import webdriver
import time

driver = webdriver.Edge()

url = "https://chat.line.biz/Uec958da29ea7f271b1c8fde2792b95b0/chat/C7321e23767771aa4343d8a9d88955ae4"
driver.get(url)

# login by hand
time.sleep(60)

with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)