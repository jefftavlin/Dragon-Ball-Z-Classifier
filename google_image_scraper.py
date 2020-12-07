import requests
import csv
import time
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import pandas as pd
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL import Image
import io
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def open_page(url, search, pages = 0):
    chrome_options = webdriver.ChromeOptions()
    
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options = chrome_options)
    driver.get(url)
    time.sleep(2)
    
    search_bar = driver.find_element_by_css_selector('input.gLFyf')
    search_bar.send_keys(search)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)
    
    
    if pages > 0:
        for i in range(pages):
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(4)
    
    thumbnail_results = driver.find_elements_by_css_selector("img.Q4LuWd")
    
    img_urls = []
    
    for img in thumbnail_results:
        try:
            img.click()
            time.sleep(1)
        except Exception:
            continue

        actual_img = driver.find_elements_by_css_selector('img.n3VNCb')
        for img in actual_img:
            if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                img_urls.append(img.get_attribute('src'))
                
    print(f'Collected {len(img_urls)} urls to download!')            
    driver.quit()
    return img_urls
    
    
url = 'https://www.google.ca/imghp?hl=en&tab=wi&ogbl'

goku_urls = open_page(url,'goku dragon ball z', 10)
goku_v2_urls = open_page(url,'goku super saiyan',10)
piccolo_urls = open_page(url,'piccolo dragon ball z',10)
piccolo_v2_urls = open_page(url,'piccolo dragon ball super',10)
vegeta_urls = open_page(url,'vegeta super saiyan', 10)
vegeta_v2_urls = open_page(url,'vegeta dragon ball z', 10)


goku_final_urls = goku_urls + goku_v2_urls
piccolo_final_urls = piccolo_urls + piccolo_v2_urls
vegeta_final_urls = vegeta_urls + vegeta_v2_urls

print(f'The number of Goku images collected are {len(goku_final_urls)}')
print(f'The number of Piccolo images collected are {len(piccolo_final_urls)}')
print(f'The number of Vegeta images collected are {len(vegeta_final_urls)}')

root = os.getcwd()
goku_path = root + '\\Goku'
piccolo_path = root + '\\Piccolo'
vegeta_path = root + '\\Vegeta'

def download_images_to_folder(path, url_list,):
    name = path.split('\\')[-1]
    os.chdir(path)
    for num, img in enumerate(url_list):
        img = requests.get().content
        with open(f'{name}_{num}.jpg', 'wb') as handler:
            handler.write(img)
    os.chdir(root)
    
download_images_to_folder(goku_path, goku_final_urls)
download_images_to_folder(piccolo_path, piccolo_final_urls)
download_images_to_folder(vegeta_path, vegeta_final_urls)
