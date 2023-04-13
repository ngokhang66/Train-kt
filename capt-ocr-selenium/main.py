import csv
import time
from ocr_model import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import concurrent.futures
import random

folderPathChrome = 'C:\\Users\\Kang\\PycharmProjects\\ChromeBrowser\\'

def fill_form(i):
    filename = folderPathChrome + 'data' + str(i) + '.csv'
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader, None)  
        for row in csv_reader:
            options = Options()
            # path folder
            s = Service(folderPathChrome + 'chromedriver' + str(i) + '.exe')
            options.binary_location = folderPathChrome + 'GoogleChromePortable' + \
                str(i) + '\\GoogleChromePortable' + str(i) + '.exe'
            options.add_argument('--user-data-dir=' + folderPathChrome +
                                 'GoogleChromePortable' + str(i) + '\\Data\\profile\\')
            options.add_argument('--profile-directory=' + 'Profile ' + '0')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--render-process-limit=1')
            # options.add_argument('--headless')
            options.add_argument("--window-size=700,950")

            browser = webdriver.Chrome(service=s, options=options)
            browser.get("https://www.gptplanet.com/index.php?view=register")

            # wait for form to load
            try:
                time.sleep(2)
              
                captchaImg = WebDriverWait(browser, 25)\
                    .until(EC.presence_of_element_located((By.XPATH, '//*[@id="captchaimg"]')))


                location = captchaImg.location
                print(location)
                size = captchaImg.size
                # save screenshot of entire page
                browser.save_screenshot(folder_path(
                    '') + 'screenshot' + str(i) + '.png')

                x = location['x']
                y = location['y']
                width = location['x']+size['width']
                height = location['y']+size['height']

                print('x ', x, 'y ', y, 'w ', width, 'h ', height)

                img = Image.open(folder_path('') + 'screenshot' + str(i) + '.png')
                img = img.crop((int(x), int(y), int(width), int(height)))
                img.save(folder_path('') + 'captcha' + str(i) +
                         '.png')  

                # ocr captcha
                time.sleep(random.randint(1, 3))
                captchaTxt = classify_image(
                    folder_path('') + 'captcha' + str(i) + '.png')

                time.sleep(1)
                WebDriverWait(browser, 25)\
                    .until(EC.presence_of_element_located((By.XPATH, '//*[@id = "captcha"]')))\
                    .send_keys(captchaTxt)

                time.sleep(5)

                browser.quit()

            except Exception as ERROR:
                print(ERROR)

if __name__ == '__main__':
   fill_form(1)
