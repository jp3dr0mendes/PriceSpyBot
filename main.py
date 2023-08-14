import requests
import time
import json

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
        
        site_soup = bs(search.content)
        
        time.sleep(5)

        self.input = self.browser.find_element(By.XPATH,'//*[@id="APjFqb"]')
        
        if self.input is None:
            print("NoneType Error!")
            return
        print(self.input)
        self.input.send_keys('Hello World!')
        self.input.send_keys(Keys.ENTER)
        time.sleep(10)                    
    def search(self):
        pass        
if __name__ == '__main__':
    PriceSpy('sla')