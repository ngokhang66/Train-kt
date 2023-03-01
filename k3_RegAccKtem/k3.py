from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
import imaplib
import email
import re

def send_recapcha(data_sitekey, page_url):
    API_ENDPOINT = "http://azcaptcha.com/in.php"
    API_KEY = "wfhxr6mvfpr7ncl8yykvb2gxt93bwhp4"
    data = {"key":API_KEY, "method": "userrecaptcha", "googlekey": data_sitekey, "pageurl": page_url, "invisible": 1, "json": "1"}
    r = requests.post(url = API_ENDPOINT, data = data)
    pastebin_url = r
    print(pastebin_url.text)
    return pastebin_url.json()["request"]

def get_solve(id):
    API_ENDPOINT = "http://azcaptcha.com/res.php"
    API_KEY = "wfhxr6mvfpr7ncl8yykvb2gxt93bwhp4"
    data = {"key":API_KEY, "action": "get", "id": id, "json": "0"}
    r = requests.post(url = API_ENDPOINT, data = data)
    print(r.text)
    return r.text

# 1. Khai bao bien browser
browser = webdriver.Chrome('C:\D\Tool\chromedriver.exe')
browser.set_window_size(700, 800)

EMAIL = "eriksaleida526@hotmail.com"
USERNAME = "fn78F2GdAg"
PASSWORD = "Admin@123"

print("EMAIL: ", EMAIL)
print("USERNAME: ", USERNAME)
print("PASSWORD: ", PASSWORD)

# 2. Mo trang web
browser.get("https://howkteam.vn/account/register")

browser.find_element(By.ID, 'Email').send_keys(EMAIL)
browser.find_element(By.ID, 'UserName').send_keys(USERNAME)
browser.find_element(By.ID, 'Password').send_keys(PASSWORD)
browser.find_element(By.ID, 'ConfirmPassword').send_keys(PASSWORD)
browser.find_element(By.CLASS_NAME, 'btn-block').click()

data_sitekey = browser.find_element(By.CLASS_NAME, 'btn-block').get_attribute('data-sitekey')
page_url = 'https://howkteam.vn/account/register'

print("Solving capcha......")
id = send_recapcha(data_sitekey, page_url)

sleep(10)

solve = get_solve(id)
while (solve == "CAPCHA_NOT_READY"):
    sleep(5)
    solve = get_solve(id)
solve = solve[3:]

a = 'document.getElementById("g-recaptcha-response").innerHTML="'+ solve +'";'
browser.execute_script(a)
browser.execute_script("onRegister('token');")
print("Done capcha......")

sleep(5)

print("Read mail & GET_LINK")
imap_host = 'outlook.office365.com'
imap_user = EMAIL
imap_pass = USERNAME

# Connect to the server
imap_server = imaplib.IMAP4_SSL(imap_host)

# Login to the account
imap_server.login(imap_user, imap_pass)

# Select the mailbox you want to read from
imap_server.select('INBOX')

# Search for emails from the specified sender
status, messages = imap_server.search(None, 'FROM "kteamse@gmail.com"')

# Fetch the email in the list
status, data = imap_server.fetch(messages[0].split()[0], '(RFC822)')

# Parse the email
msg = email.message_from_bytes(data[0][1])

html = msg.get_payload(decode=True)

href_pattern = re.compile(r'href="(.+?)"')
link = href_pattern.search(html.decode()).group(1)

imap_server.close()
imap_server.logout()

# Replace "&amp;" with "&"
link = link.replace("&amp;", "&")
print("LINK: ", link)

sleep(5)

# opens in a new browser tab
browser.execute_script("window.open('about:blank', 'secondtab');")
                          
# It is switching to second tab now
browser.switch_to.window("secondtab")
  
# In the second tab, it opens 
browser.get(link)

sleep(10)

browser.find_element(By.ID, 'loginLink').click()

# login now
print("Loging....")
browser.find_element(By.ID, 'Email').send_keys(EMAIL)
browser.find_element(By.ID, 'Password').send_keys(PASSWORD)
browser.find_element(By.CLASS_NAME, 'btn-block').click()

print("Done!")
input()
browser.quit()