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

        self.browser = webdriver.Chrome(options = chrome_options)
        # self.browser = webdriver.Chrome()
        self.site    =  'https://www.google.com'
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
        self.itens_list = self.url_search(self.user_product_search)

        if len(self.itens_list) or self.itens_list is not None:
            print(f'urls catches: {len(self.itens_list)}')
        else:
            print('Error: Null')
            return
        
        self.price_search(self.itens_list)

    #bs site html    
    def sopa(self, url:str):

        time.sleep(random.randint(1,3))

        request =  requests.get(url,headers=self.headers)

        if request.status_code == 200:
            print(f'Request Sucess: {request.status_code}')
            return bs(request.text,'html.parser')
        else:
            print(f'Request Error: {request.status_code}')
            return None
        
    
    def url_search(self, product:str) -> list():

        self.input.send_keys(self.user_product_search)
        self.input.send_keys(Keys.ENTER)

        time.sleep(random.randint(1,5))
        
        #catch google shopping url
        site_html                = self.sopa(self.browser.current_url)
        site_html_div_search     = site_html.find_all('div', class_='yuRUbf')        
        itens_url                = list()

        print(f'debug 1: {site_html_div_search}')

        for div in site_html_div_search:
            aux = div.find('a')
            aux_h = aux['href']
            itens_url.append(aux['href'])
        
        print(f'lista de urls: {itens_url}')

        # site_html_div_search     = site_html.find_all('a', class_='plantl pla-unit-title-link')
        
        #catch google normal url
        # for a in site_html_div_search:
        #     itens_url.append(a['href'])
        
        return itens_url
    
    #search price of site 
    def price_search(self, sites: list) -> list:
        
        price_list = list()

        for site in sites:

            time.sleep(random.randint(1,4))
            self.browser.get(site)
            letters            = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            site               = self.sopa(self.browser.current_url)
            site_divs          = site.find_all('div')
            site_divs          = self.browser.find_elements(By.XPATH,"//div[contains(@class, 'price')]")
            site_divs_text     = [div.text.replace('\n','.') for div in site_divs]
            site_divs_text     = [x.replace('R$','') for x in site_divs_text]
            site_divs_text     = [x.replace(' ','') for x in site_divs_text]

            for l in letters:
                site_divs_text = [x.replace(l,'') for x in site_divs_text]
            try:
                price_list.append(float([x for x in site_divs_text if x != ''][0]))
            except:
                try:
                    price_list.append([x for x in site_divs_text if x != ''][0].split('.')[1])
                    price_list[-1] = float(price_list[-1].replace(',','.'))
                    print(price_list)[-1]
                    if '%' in price_list[-1]:
                        price_list.pop() 
                except:
                    pass

            print(price_list[-1])

            try:
                self.browser.back()
            except:
                break 
            
        print(price_list)

if __name__ == '__main__':
    PriceSpy('sla')