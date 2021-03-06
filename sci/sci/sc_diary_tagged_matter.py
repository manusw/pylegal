import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import json
import pymongo
from pymongo import MongoClient
#manu mongodb testing code 
client = MongoClient('mongodb://localhost:27017')
db = client.pymongo_wtltest
diary_results={}
diary_taged={}
def initialize_tag_dic(ta_master_court,ta_diary_num,ta_diary_year):
    diary_taged['ta_master_court'] =ta_master_court
    diary_taged['ta_diary_num']=ta_diary_num
    diary_taged['ta_diary_year']=ta_diary_year 
#end mongodb testing 
def prepare_sc_hidden_internal_diary_num(diary_num,diary_year):
    # TO DO Write the logic here
    internal_diary_num=diary_num+diary_year
    return(internal_diary_num)
def get_soup(html):
                if html is not None:
                    soup = BeautifulSoup(html, 'lxml')
                    return soup
                else:
                    return
        ## find data 

cookies = {
    'has_js': '1',
    'PHPSESSID': '0e5bqhve725ogotfvj9iomhkj6',
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

diary_num='123'
diary_year='2018'
d_num=prepare_sc_hidden_internal_diary_num(diary_num,diary_year)
data = [
  ('diaryno', d_num),
]

response = requests.post('https://sci.nic.in/php/case_status/get_connected.php', headers=headers, cookies=cookies, data=data,verify=False)
print(response.content)
#case_details_pd=pd.read_html(response.content,header=0)
#print(case_details_pd)

table_contents = [] 

soup=get_soup(response.content)
dne=soup.findAll(text='CONNECTED MATTERS NOT FOUND')
if(dne):
        table_contents.append('CONNECTED MATTERS NOT FOUND')


else:
         # find table , extract data ,
    # To Do -- check if table does not exist or there is not any data 
    table = soup.find("table")
    rows = table.find_all("tr")

      # store your table here
    for tr in rows:
        if rows.index(tr) == 0 : 
            row_cells = [ th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '' ]  
        else : 
            row_cells = ([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != '' ] 
        if len(row_cells) > 1 : 
            table_contents += [ row_cells ]
hdn_sc_diary_num=d_num
initialize_tag_dic('sc',hdn_sc_diary_num,diary_year)
diary_results['ta_master_court']='SC'
diary_results['ta_diary_num']=diary_num 
diary_results['ta_diary_year']=diary_year 
diary_results['diary_tag']=table_contents
diary_taged['diary_tag']=table_contents
print(diary_taged)
