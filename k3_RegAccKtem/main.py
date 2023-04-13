import search_imap
import random_pwd
import re
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import *

FolderPath = 'C:\\Users\\Kang\\PycharmProjects\\RegAccKtem'

usr = 'nancybyxjane@hotmail.com'
pwd = 'pass'

randomPwd = pwd + "@A|"


def acp_api_send_request(driver, message_type, data={}):
    message = {
		# this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    # run JS code in the web page context
    # preceicely we send a standard window.postMessage method
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))

options = Options()
##### path folder
options.binary_location = FolderPath + '\\GoogleChromePortable\\GoogleChromePortable.exe'
options.add_argument('--user-data-dir=' + FolderPath + '\\GoogleChromePortable\\Data\\profile\\')
options.add_argument('--profile-directory=' + 'Profile 0')
options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument("--incognito")
options.add_extension(FolderPath + '\\anticaptcha.crx')

url = "https://howkteam.vn/account/register"
web = webdriver.Chrome(options=options)
# Go to the empty page for setting the API key through the plugin API request
web.get('https://antcpt.com/blank.html')
acp_api_send_request(
    web,
    'setOptions',
    {'options': {'antiCaptchaApiKey': ''}}
)
time.sleep(3)
# Go to the test form with reCAPTCHA 2
web.get(url)

try:
    InputMail = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]')))
    InputMail.send_keys(usr)
    InputUsr = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="UserName"]')))
    InputUsr.send_keys(usr.split('@')[0])
    InputPwd = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
    InputPwd.send_keys(randomPwd)
    InputPwd2 = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ConfirmPassword"]')))
    InputPwd2.send_keys(randomPwd)
    
    # WebDriverWait(web, 100).until(lambda x: x.find_element(By.CSS_SELECTOR, '.antigate_solver.solved'))
    print("check mail")
    WebDriverWait(web, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="registerForm"]/fieldset/div[5]/button'))).click()
    print("check mail1")

    bodyMail = search_imap(usr, pwd)
    time.sleep(3)
    
    match = re.search(r'\(https?://[^)]+', str(bodyMail))
    confirm_url = match.group()[1:]
    print(confirm_url)
    web.get(confirm_url)
    time.sleep(1)
    web.get("https://howkteam.vn/account/login")
    print("login")
    print(usr + " | " + randomPwd)
    InputMail = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]')))
    InputMail.send_keys(usr)
    InputPwd = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
    InputPwd.send_keys(randomPwd)
    WebDriverWait(web, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/fieldset/div[4]/button'))).click()

    time.sleep(900)
    # web.quit()
except Exception as ERROR:
    print(ERROR)
    # web.quit()

