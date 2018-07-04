import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
output_file='scilink7.csv'

cookies = {
    'has_js': '1',
    'PHPSESSID': 'gb6268uaq443ovqt4279nkqj64',
}

headers = {
    'Origin': 'https://sci.nic.in',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://sci.nic.in/case-status',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

data = [
  ('ct', '1'),
  ('cn', '3'),
  ('cy', '2018'),
]
def get_soup(html):
                if html is not None:
                    soup = BeautifulSoup(html, 'lxml')
                    return soup
                else:
                    return
r = requests.post('https://sci.nic.in/php/case_status/case_status_process.php', headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 30))
soup=get_soup(r.content)
case_dne=soup.body.findAll(text='Case Not Found')
print(case_dne)
for item in case_dne:
    print("Dsdsd")
case_details_pd=pd.read_html(r.content,header=0)
print(case_details_pd)

##case_details_pd.to_csv(output_file, sep='\t', encoding='utf-8')
#for i, df in enumerate(case_details_pd):
#    df.to_csv('myfile_%s.csv' % i,mode='a')

## if file does not exist write header 
#if not os.path.isfile('testee.csv'):
#   df.to_csv('testee.csv', header='column_names')
#else: # else it exists so append without writing the header
#   df.to_csv('testee.csv', mode='a', header=False)

#csvfile = "teste.csv"

##Assuming res is a flat list
#with open(csvfile, "w") as output:
#    writer = csv.writer(output, lineterminator='\n')
#    for val in case_details_pd:
#        writer.writerow([val])    

  
