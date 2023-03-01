import search_imap
# import random_pwd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from anticaptchaofficial.recaptchav2proxyless import *

FolderPath = 'C:\\Users\\Kang\\PycharmProjects\\RegAccKtem'

usr = 'bes085connie@hotmail.com'
pwd = 'aKwdgs88h'
randomPwd = pwd + "@A|"
print(randomPwd)
# randomPwd = random_pwd()
# print(randomPwd)

options = Options()
##### path folder
options.binary_location = FolderPath + '\\GoogleChromePortable\\GoogleChromePortable.exe'

options.add_argument('--user-data-dir=' + FolderPath + '\\GoogleChromePortable\\Data\\profile\\')
options.add_argument('--profile-directory=' + 'Profile 0')
options.add_argument('--blink-settings=imagesEnabled=false')  # ko hinh anh
options.add_argument("--incognito")

url = "https://howkteam.vn/account/register"
web = webdriver.Chrome(options=options)
wait = WebDriverWait(web, 20)
web.get(url)
time.sleep(0.5)

solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("86549d89f32cec3fef05cfb723a0fd62")
solver.set_website_url(url)
solver.set_website_key("6LcjrlgUAAAAAFlUURyuaYP0jqpip5hAKD56uHNr")
# solver.set_min_score(0.9)

try:
    g_response = solver.solve_and_return_solution()
    InputMail = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]')))
    InputMail.send_keys(usr)
    InputUsr = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="UserName"]')))
    InputUsr.send_keys(usr.split('@')[0])
    InputPwd = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
    InputPwd.send_keys(randomPwd)
    InputPwd2 = WebDriverWait(web, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ConfirmPassword"]')))
    InputPwd2.send_keys(randomPwd)
    if g_response != 0:
        print("g-response: " + g_response)
        WebDriverWait(web, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="registerForm"]/fieldset/div[5]/button'))).click()
    else:
        print("task finished with error " + solver.error_code)

    print("check mail")

    bodyMail = search_imap(usr, pwd)
    time.sleep(1)
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
