from selenium import webdriver
import time, os, subprocess
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from paddleocr import PaddleOCR


# ocr = PaddleOCR(lang='en')
# result = ocr.ocr('C:/Users/Mostafa/Desktop/RegisterRobat/image.png')
# print(result)

# reader = easyocr.Reader(['en']) 
# result = reader.readtext('C:/Users/Mostafa/Desktop/RegisterRobat/image.png')
# print(result)
# # for detection in result:
# #     print(detection[1])

def get_last_sms():
    command = "adb shell content query --uri content://sms/inbox "
    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    result = result[result.find('body')+5 : result.find('body')+50].replace(',',' ').split(' ')
    print(result)
    for x in result:
        if x.isdigit():
            last_sms = int(x)
            break
        
    return last_sms

print(get_last_sms())