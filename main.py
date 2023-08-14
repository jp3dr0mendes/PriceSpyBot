import requests
import time
import json
import random

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class PriceSpy:

    def __init__(self, item = str,*args, **kwargs):
        
        # headless setings
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("----disable-gpu")

        # self.browser = webdriver.Chrome(options = chrome_options)
        self.browser = webdriver.Chrome()
        self.site =  'https://www.google.com'
        self.headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }

        self.browser.get(self.site)
        
        search = requests.get(self.site)

        if not search.status_code == 200:
            while search.status_code != 200:
                search = search.get(self.site)
        
        time.sleep(5)

        self.input = self.browser.find_element(By.XPATH,'//*[@id="APjFqb"]')
        
        if self.input is None:
            print("NoneType Error!")
            return
        
        self.user_product_search = 'mi band 5'
        self.itens_list = self.search(self.user_product_search)

        if len(self.itens_list):
            print('sucess:', len(self.itens_list))
        else:
            print('Error: Null')

        # self.input.send_keys(self.user_product_search)
        # self.input.send_keys(Keys.ENTER)

        # time.sleep(3)

        # site_html            = self.sopa(self.browser.current_url)

        # #catch google shopping url
        # site_html_div_search = site_html.find_all('div', class_='yuRUbf')        
        # itens_url            = list()

        # for div in site_html_div_search:
        #     aux = div.find('a')
        #     itens_url.append(aux['href'])

        # site_html_div_search = site_html.find_all('a', class_='plantl pla-unit-title-link')
        
        # #catch google normal url
        # for a in site_html_div_search:
        #     itens_url.append(a['href'])

    def sopa(self, url:str):

        request =  requests.get(url,headers=self.headers)

        if request.status_code == 200:
            print(f'Request Sucess: {request.status_code}')
            return bs(request.text,'html.parser')
        else:
            print(f'Request Error: {request.status_code}')
            return None

    def search(self, product:str) -> list():
        self.user_product_search = 'mi band 5'

        self.input.send_keys(self.user_product_search)
        self.input.send_keys(Keys.ENTER)

        time.sleep(3)

        site_html            = self.sopa(self.browser.current_url)

        #catch google shopping url
        site_html_div_search = site_html.find_all('div', class_='yuRUbf')        
        itens_url            = list()

        for div in site_html_div_search:
            aux = div.find('a')
            itens_url.append(aux['href'])

        site_html_div_search = site_html.find_all('a', class_='plantl pla-unit-title-link')
        
        #catch google normal url
        for a in site_html_div_search:
            itens_url.append(a['href'])
        
        return itens_url
        

if __name__ == '__main__':
    PriceSpy('sla')