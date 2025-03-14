from selenium import webdriver
import time, os, subprocess
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from paddleocr import PaddleOCR
from selenium.webdriver.chrome.options import Options

from info import *

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

ocr = PaddleOCR(lang='en', show_log = False)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ve.cbi.ir/VC/TasRequestVC.aspx")
driver.implicitly_wait(10)

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
    ocr = PaddleOCR(lang='en')
    result = ocr.ocr('C:/Users/Mostafa/Desktop/RegisterRobat/image.png')
    # print(result[-1][-1][-1][0])
    return result[-1][-1][-1][0]

def check_alert():
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')

        alert = driver.switch_to.alert
        print("alert : ", alert.text)
        alert.accept()
        return 1
    except TimeoutException:
        print("no alert successful process")
        return 0
    # success

def Enter_User_information():
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

def check_element(xpath):
    try:
        driver.find_element(webdriver.common.by.By.XPATH, xpath)
        print('xccccccccccccccccccccccccccc')
        return True
    except:
        return False

def change_captcha_picture():
    driver.find_element(webdriver.common.by.By.XPATH, r'//*[@id="c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_ReloadIcon"]').click()
    time.sleep(1)
    driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')

def SolveCaptcha(file):
    while True :

        time.sleep(2)
        result = ocr.ocr('C:/Users/Mostafa/Desktop/RegisterRobat/image.png')
        if result[0] != None and  result[-1][-1][-1][0] :
            
            return result[-1][-1][-1][0]
            
        else:
            change_captcha_picture()

def get_the_image_of_captcha():
    # solve the captcha
    while True:
        if check_element('ctl00_ContentPlaceHolder1_tbMobileConfCode')  : 
            return 0
        driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')
        driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').send_keys(SolveCaptcha('image.png'))

        if check_element('ctl00_ContentPlaceHolder1_tbMobileConfCode')  : 
            break
        try : 
            driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_btnSendConfirmCode').click()
        except:
            break

        time.sleep(2)

def set_the_secund_page_information():
    driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_tbMobileConfCode').send_keys(get_last_sms()) # send the verification code
    driver.find_element(webdriver.common.by.By.XPATH, f'//*[@id="ctl00_ContentPlaceHolder1_ddlState"]/option[{ostan_mahal_zendgy + 1}]').click()

def change_captcha_picture_2():
    driver.find_element(webdriver.common.by.By.XPATH, r'//*[@id="c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_ReloadIcon"]').click()
    time.sleep(0.5)
    driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')

def SolveCaptcha_2(file):
    while True :

        time.sleep(0.5)
        result = ocr.ocr('C:/Users/Mostafa/Desktop/RegisterRobat/image.png')
        if result[0] != None and  result[-1][-1][-1][0] :
            
            return result[-1][-1][-1][0]
            
        else:
            change_captcha_picture_2()
    
def solve_captcha_by_send_request():
    try: 
        solver = TwoCaptcha(TwoCaptcha_Token)

        id = solver.send(file='image.png')
        time.sleep(15)

        return solver.get_result(id)
    except: 
        solver = TwoCaptcha(TwoCaptcha_Token)

        id = solver.send(file='image.png')
        time.sleep(15)

        return solver.get_result(id)

def solve_secund_page_captcha():
    counter = 0
    alert_text = ''
    result = True
    while result:
        try:
            driver.find_element(webdriver.common.by.By.ID, 'c_vc_tasrequestvc_ctl00_contentplaceholder1_captcha1_CaptchaImage').screenshot(filename='image.png')
            driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').clear()
            driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').send_keys(SolveCaptcha_2('image.png') if counter < 6 else solve_captcha_by_send_request()) 
            # driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_tbCaptcha1').send_keys(input('>>>>>>>>>>>>>>>>>>')) 
            driver.find_element(webdriver.common.by.By.ID, f'ctl00_ContentPlaceHolder1_btnContinue1').click()
        except : pass
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                'Timed out waiting for PA creation ' +
                                'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert_text += '\n' + alert.text  + '    '
            print("alert : ", alert.text)
            if alert.text.find('بانکی') >= 0 or alert.text.find('ثانیه') >= 0 or alert.text.find('ارسالی') >= 0:
                break
            alert.accept()

        except TimeoutException:
            print("no alert  \n successful process")
                    
            banks = driver.find_element(webdriver.common.by.By.ID, 'ctl00_ContentPlaceHolder1_ddlBankName').find_elements(webdriver.common.by.By.TAG_NAME, 'option')
            exist_banks = [bank.text for bank in banks]
            counter = 1
            for bank in bank_mored_nazare :
                print(bank)
                for exist_bank in exist_banks:
                    if bank in exist_bank:
                        print(exist_bank)
                        while True:
                            os.system('Fire-Alarm-Sound-4.mp3')
                            time.sleep(15)
                    elif counter == len(bank_mored_nazare):
                        break
                counter += 1
        # os.system('cls')
        print(counter)
        print(alert_text)
        counter += 1

def run():
    Enter_User_information()
    get_the_image_of_captcha()
    set_the_secund_page_information()
    solve_secund_page_captcha()

if __name__ == '__main__':
    run()