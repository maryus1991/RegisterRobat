from selenium import webdriver
import time, os, subprocess
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# the below information should filled in info.py file  
# code_MELI_pedar = '5*********2'
# sall_tavalide_pedar = '1355'
# roze_tavalode_pedar = 1
# mah_tavalode_pedar = 1
# ostan_tavalode_pedar = 14
# shahr_tavalod_pedar = 22
# shomareh = '099***********' 
# code_MELI_farzand = '526**2***22'
# sall_tavalide_farzand = '1403'
# roze_tavalode_farzand = 3
# mah_tavalode_farzand = 9
# ostan_tavalode_farzand = 13
# shahr_tavalod_farzand = 22
# shomareh_farzand = 5
# ostan_mahal_zendgy = 13

# TwoCaptcha_Token = '1eef21*****************************4'

from info import *

def get_last_sms():
    command = "adb shell content query --uri content://sms/inbox "
    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    result = result[result.find('body')+5 : result.find('body')+50].replace(',',' ').split(' ')
    
    for x in result:
        if x.isdigit():
            last_sms = int(x)
            break
        
    return last_sms

def SolveCaptcha(file):
    try: 
        solver = TwoCaptcha(TwoCaptcha_Token)

        id = solver.send(file=file)
        time.sleep(20)

        return solver.get_result(id)
    except : 
        solver = TwoCaptcha(TwoCaptcha_Token)

        id = solver.send(file=file)
        time.sleep(20)

        return solver.get_result(id)

driver = webdriver.Chrome()





driver.get("https://ve.cbi.ir/VC/TasRequestVC.aspx")
driver.implicitly_wait(10)
# send the user information to website
driver.find_element(webdriver.common.by.By.ID,'ctl00_ContentPlaceHolder1_tbPIDNo').send_keys(code_MELI_pedar)
driver.find_element(webdriver.common.by.By.ID,'ctl00_ContentPlaceHolder1_tbPBrYear').send_keys(sall_tavalide_pedar)
driver.find_element(webdriver.common.by.By.XPATH,f'/html/body/form/center/table/tbody/tr/td[3]/center/div/div/div/div[2]/table/tbody/tr[2]/td[2]/select[1]/option[{ roze_tavalode_pedar + 1 }]').click()
driver.find_element(webdriver.common.by.By.XPATH,f'/html/body/form/center/table/tbody/tr/td[3]/center/div/div/div/div[2]/table/tbody/tr[2]/td[2]/select[2]/option[{ mah_tavalode_pedar + 1}]').click()
driver.find_element(webdriver.common.by.By.XPATH,f'//*[@id="ctl00_ContentPlaceHolder1_ddlPBrState"]/option[{ ostan_tavalode_pedar + 1}]').click()
driver.find_element(webdriver.common.by.By.XPATH,f'/html/body/form/center/table/tbody/tr/td[3]/center/div/div/div/div[2]/table/tbody/tr[4]/td[2]/select/option[{ shahr_tavalod_pedar + 1 }]').click()
driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbMobileNo').send_keys(shomareh)
driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCIDNo').send_keys(code_MELI_farzand)
driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCBrYear').send_keys(sall_tavalide_farzand)
driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlCBrMonth"]/option[{ mah_tavalode_farzand + 1 }]').click()
driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlCBrDay"]/option[{ roze_tavalode_farzand + 1 }]').click()
driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlCBrState"]/option[{ostan_tavalode_farzand + 1 }]').click()
driver.find_element(webdriver.common.by.By.XPATH, f'/html/body/form/center/table/tbody/tr/td[3]/center/div/div/div/div[2]/table/tbody/tr[10]/td[2]/select/option[{ shahr_tavalod_farzand + 1 }]').click()
driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlChildNo"]/option[{ shomareh_farzand + 1 }]').click()

# solve the captcha
driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')

driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').send_keys(SolveCaptcha('image.png'))

# submit the form
driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_btnSendConfirmCode').click()


driver.switch_to.alert.accept()

time.sleep(20)

driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_tbMobileConfCode').send_keys(get_last_sms()) # send the verification code
driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlState"]/option[{ostan_mahal_zendgy + 1}]').click()

# solve the captcha of second page  
driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')
driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').send_keys(SolveCaptcha('image.png'))


driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_btnContinue1').click()

# check if any alert exist 
# if any alert exit the process fail and should rerun it
# if no alert the process succeed
try:
    WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')

    alert = driver.switch_to.alert
    print("alert : ", alert.text)
    alert.accept()
    driver.quit()
except TimeoutException:
    print("no alert successful process")
    while True:
        os.system('Fire-Alarm-Sound-4.mp3')
        time.sleep(15)
    # success






