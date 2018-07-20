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
#manu mongodb testing code 
client = MongoClient('mongodb://localhost:27017')
db = client.mongo_scdetails

def initialize_earl_court_dict(ta_master_court,ta_diary_num,ta_diary_year):
    diary_earl_court_details['ta_master_court'] =ta_master_court
    diary_earl_court_details['ta_diary_num']=ta_diary_num
    diary_earl_court_details['ta_diary_year']=ta_diary_year 
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

diary_num='431'
diary_year='2018'
d_num=prepare_sc_hidden_internal_diary_num(diary_num,diary_year)
data = [
  ('diaryno', d_num),
]

response = requests.post('https://www.sci.nic.in/php/case_status/get_earlier_court.php', headers=headers, cookies=cookies, data=data,verify=False)
print(response.content)
case_details_pd=pd.read_html(response.content,header=0)
print(case_details_pd)
soup=get_soup(response.content)

# find table , extract data ,
# To Do -- check if table does not exist or there is not any data 
table = soup.find("table")
rows = table.find_all("tr")

table_contents = []   # store your table here
for tr in rows:
    if rows.index(tr) == 0 : 
        row_cells = [ th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '' ]  
    else : 
        row_cells = ([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != '' ] 
    if len(row_cells) > 1 : 
        table_contents += [ row_cells ]

diary_results={}
diary_earl_court_details={}
initialize_earl_court_dict('sc',hdn_sc_diary_num,diary_year)
diary_results['ta_master_court']='SC'
diary_results['ta_diary_num']=diary_num 
diary_results['ta_diary_year']=diary_year 
diary_results['earl_court_details']=table_contents
diary_earl_court_details['earl_court_details']=table_contents

print(diary_results)
# Function to update record to mongo db
def updatemongotest():
    try:
        criteria = '123'
        ta_diary_year = '2017'
        
        db.casedetail.update_one(
            {"ta_diary_num": criteria},
            {
            "$set": {
                "ta_diary_year":'2019',
            }
            
            }
        )
        print( "Records updated successfully")    
    
    except:
        raise
earlcourt=db.earlcourt
Dboresult=earlcourt.insert_one(diary_results)
mdccasedetails=db.earlcourt.find()
print ('\n All data from case Database \n')
for cd in mdccasedetails:
    print( cd)
