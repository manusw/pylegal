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
output_file='casediary.csv'

diary_results={}
diary_office_report={}
#client = MongoClient('mongodb://localhost:27017')
#db = client.pymongo_wtltest

def get_soup(html):
                if html is not None:
                    soup = BeautifulSoup(html, 'lxml')
                    return soup
                else:
                    return
def prepare_sc_hidden_internal_diary_num(diary_num,diary_year):
    # TO DO Write the logic here
    internal_diary_num=diary_num+diary_year
    return(internal_diary_num)

def Call_script_diary(url,headers,cookies,hdn_diarynum):
    data = [
      ('diaryno', hdn_diarynum),
    ]
    try:
        res = requests.post(url, headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 30))
        res.raise_for_status()
    except requests.HTTPError as e:
        logging.warning('SC return non-200 status code')
        raise e
    except requests.RequestException as e:
        logging.warning('Issue retrieving SC results page')
        raise e
    except ConnectionError as e:
        raise e
    else:
        return res

def initialize_office_report_dic(ta_master_court,ta_diary_num,ta_diary_year,ta_hdn_diary):
    diary_office_report['ta_master_court'] =ta_master_court
    diary_office_report['ta_diary_num']=ta_diary_num
    diary_office_report['ta_diary_year']=ta_diary_year  
    diary_office_report['ta_hdn_diary']=ta_hdn_diary




court_code='sc'
diary_num='1'
diary_year='2018'
hdn_sc_diary_num=prepare_sc_hidden_internal_diary_num(diary_num,diary_year)
data = [
  ('diaryno', hdn_sc_diary_num),
]

#def get_OfficeReports_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
url='https://sci.nic.in/php/case_status/get_office_report.php'
cookies = {
    'has_js': '1',
    'PHPSESSID': '8j1pgblhj22d21rejvdinvehg1',
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
result=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
if result and result.status_code == 200:
    #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
    initialize_office_report_dic('sc',diary_num,diary_year,hdn_sc_diary_num)    
    table_contents = [] 

    soup=get_soup(result.content)
    print(soup)
    dne=soup.findAll(text='NOT FOUND')
    if(dne):
            table_contents.append('NOT FOUND')
    else:
        df=pd.read_html(result.content,header=0)
                # find table , extract data ,
        # To Do -- check if table does not exist or there is not any data 
        # To DO -- put accurate table name and class whenever it can be found in SC code
        table = soup.find("table")
        rows = table.find_all("tr")
            # store your table here
        for tr in rows:
            #if rows.index(tr) == 0 : 
            #    row_cells = [ th.getText().strip() for th in tr.find_all('th') if th.getText().strip() != '' ]  
            #else : 
            row_cells = ([ tr.find('th').getText() ] if tr.find('th') else [] ) + [ td.getText().strip() for td in tr.find_all('td') if td.getText().strip() != '' ] 
            if len(row_cells) > 1 : 
                table_contents += [ row_cells ]
    #populate individual dictonaries :- these have to go into mongoDB first we are trying a get slave dictionary for individual and latter we populate master class dictonary
#        diary_results['diary_listing_details']=table_contents
    diary_office_report['diary_office_reports']=table_contents
    print(diary_office_report)     
    print( 'success')
else:
    print( 'fail')

#manu dummy code to test
#for tr in rows:
#  for td in tr.find_all('td'):
#    print(td.getText().strip() )
