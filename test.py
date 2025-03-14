
from selenium import webdriver
from info import *


driver = webdriver.Chrome()
driver.get("https://ve.cbi.ir/VC/TasRequestVC.aspx")
driver.implicitly_wait(10)


banks = driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_ddlPBrState')
for x in banks.find_elements(webdriver.common.by.By.TAG_NAME, 'option'):
    print(x.text)
print(type(banks.find_elements(webdriver.common.by.By.TAG_NAME, 'option')))