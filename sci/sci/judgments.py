import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
import requests
import pandas as pd

output_file='judgement_details1.csv'
def get_soup(html):
                if html is not None:
                    soup = BeautifulSoup(html, 'lxml')
                    return soup
                else:
                    return
        ## find data 
def get_data(soup):

                try:
                    title = soup.find('title').get_text().strip().replace('\n','')
                except:
                    title = None

                return title
cookies = {
    'has_js': '1',
}

headers = {
    'Origin': 'https://sci.gov.in',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://sci.gov.in/judgments',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = [
  ('JBJfrom_date', '04-06-2016'),
  ('JBJto_date', '04-06-2018'),
  ('jorrop', 'J'),
]
try:
    r = requests.post('https://sci.gov.in/php/getJBJ.php', headers=headers, cookies=cookies, data=data,verify=False)
    soup=get_soup(r.content)
    case_details_pd=pd.read_html(r.content,header=0);
    
    print(case_details_pd)
    for i, df in enumerate(case_details_pd):
        df.to_csv(output_file,mode='a')   
except requests.exceptions.RequestException as e:  # This is the correct syntax
    print (e)            