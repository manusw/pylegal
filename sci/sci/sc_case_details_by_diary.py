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
diary_earl_court_details={}
diary_taged={}
diary_listing_date={}
hdn_sc_diary_num=1;
class CaseDetails(object):

      
    def __init__(self, diary_num,diary_year):
        self.court_base="SC"
        self.court_sub_case_type=''
        self.case_no=''
        self.case_party=''
        self.petetinor=''
        self.diary_num=diary_num
        self.diary_year=diary_year

def csv_output_test( diary, petetinor):
    with open(output_file, 'a', encoding='utf-8') as outputfile:
        writer = csv.writer(outputfile)
        for key, value in diary_results.items():
                writer.writerow([key, value])

def csv_output( diary, petetinor):

                with open(output_file, 'a', encoding='utf-8') as outputfile:

                    writer = csv.writer(outputfile)
                    writer.writerow([diary, petetinor])

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

def initialize_diary(court_code,diary_num,diary_year):
    # TO DO Write the logic here
    return;

def prepare_sc_hidden_internal_diary_num(diary_num,diary_year):
    # TO DO Write the logic here
    internal_diary_num=diary_num+diary_year
    return(internal_diary_num)

def fetch_sc_hidden_internal_diary_num(soup):
    # TO DO Write the logic here
    #do error handling
    hd_diary_val=soup.find("input",type='hidden',id='diaryno')['value']
    return hd_diary_val;


def get_indexing_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_indexing.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'
         
def initialize_earl_court_dict(ta_master_court,ta_diary_num,ta_diary_year,ta_hdn_diary):
    diary_earl_court_details['ta_master_court'] =ta_master_court
    diary_earl_court_details['ta_diary_num']=ta_diary_num
    diary_earl_court_details['ta_diary_year']=ta_diary_year  
    diary_earl_court_details['ta_hdn_diary']=ta_hdn_diary



def get_EarlierCourtDetails_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_earlier_court.php'
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
        
        initialize_earl_court_dict('sc',hdn_sc_diary_num,diary_year,hdn_sc_diary_num)
        soup=get_soup(result.content)
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
        #populate individual dictonaries :- these have to go into mongoDB first we are trying a get slave dictionary for individual and latter we populate master class dictonary
        diary_earl_court_details['earl_court_details']=table_contents
        diary_results['earl_court_details']=table_contents

        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def initialize_tag_dic(ta_master_court,ta_diary_num,ta_diary_year,ta_hdn_diary):
    diary_taged['ta_master_court'] =ta_master_court
    diary_taged['ta_diary_num']=ta_diary_num
    diary_taged['ta_diary_year']=ta_diary_year  
    diary_taged['ta_hdn_diary']=ta_hdn_diary

def get_TaggedMatter_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_connected.php'
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
        initialize_tag_dic('sc',diary_num,diary_year,hdn_sc_diary_num)
        table_contents = [] 

        soup=get_soup(result.content)
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
        #populate individual dictonaries :- these have to go into mongoDB first we are trying a get slave dictionary for individual and latter we populate master class dictonary
        diary_results['diary_tag']=table_contents
        diary_taged['diary_tag']=table_contents
    
        
        return 'success'
    else:
        return 'fail'

def initialize_listing_date_dic(ta_master_court,ta_diary_num,ta_diary_year,ta_hdn_diary):
    diary_listing_date['ta_master_court'] =ta_master_court
    diary_listing_date['ta_diary_num']=ta_diary_num
    diary_listing_date['ta_diary_year']=ta_diary_year  
    diary_listing_date['ta_hdn_diary']=ta_hdn_diary

def get_ListingDates_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_listings.php'
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
        initialize_listing_date_dic('sc',diary_num,diary_year,hdn_sc_diary_num)    
        table_contents = [] 

        soup=get_soup(result.content)
        print(soup)
        dne=soup.findAll(text='NOT FOUND')
        if(dne):
                table_contents.append('NOT FOUND')
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
        #populate individual dictonaries :- these have to go into mongoDB first we are trying a get slave dictionary for individual and latter we populate master class dictonary
#        diary_results['diary_listing_details']=table_contents
        diary_listing_date['diary_listing_details']=table_contents
        diary_results['diary_listing_details']=table_contents
        #print(diary_listing_date)     
        return 'success'
    else:
        return 'fail'

def get_InterlocutoryAD_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_ia.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_CourtFees_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_court_fees.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_Notices_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_notices.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'
def get_Defects_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_default.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_JudgementsOrder_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_judgement_order.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_Mentions_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_mention_memo.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_RestorationDeatils_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_restore.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_DropNote_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_drop.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_Appearances_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_appearance.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_OfficeReports_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_Similaritiy_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_similarities.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'

def get_Caveat_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num):
    # TO DO Write the logic here
    url='https://sci.nic.in/php/case_status/get_caveat.php'
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
    res=Call_script_diary(url,headers,cookies,hdn_sc_diary_num)
    result = res.result()
    ## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
    if result and result.status_code == 200:
        #Go ahead and parse the results Populate relevnnt details in dictonary and latter on database
        return 'success'
    else:
        return 'fail'
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
        ## find data 
def case_details_by_diary(url,headers,cookies,diary_num,diary_year):
    data = [
      ('d_no', diary_num),
      ('d_yr', diary_year),
    ]
    try:
        res = requests.post('https://sci.nic.in/php/case_status/case_status_process.php', headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 30))
        res.raise_for_status()
    except requests.HTTPError as e:
        logging.warning('delhi HC Display return non-200 status code')
        raise e
    except requests.RequestException as e:
        logging.warning('Issue retrieving HC results page')
        raise e
    except ConnectionError as e:
        raise e
    else:
        return res

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
diary_detail_url='https://sci.nic.in/php/case_status/case_status_process.php'


diary_num='123'
diary_year='2018'
response= case_details_by_diary(diary_detail_url,headers,cookies,diary_num,diary_year)
print(response)
result = response.result()
## TO DO --when we organize the class the result should be taken care for every thread and if result is 200 then only it should call supporting details
if result and result.status_code == 200:
    print("ok ")
else:
   print("BAD Response")
# handle if case does not exist 'case not found'
soup=get_soup(response.content)
case_dne=soup.body.findAll(text='Case Not Found')
if case_dne:
    print("case does not exist")
else:
    print("printing case details")
    case_heading_details =soup.find_all("h5")
    case_diary_data=CaseDetails(diary_num,diary_year)
    for item in case_heading_details:
                if("Diary No."in item.text):
                    case_diary_data.diary_num=item.text
                    diary_results['ta_diary_num']=item.text
                else:
                    case_diary_data.petetinor=item.text
                    diary_results['ta_diary_heading']=item.text
    df_pd=pd.read_html(response.content,header=None)
    print(df_pd[0])

# try table extraction 
#results = {}
#for row in soup.findAll('tr'):
#    aux = row.findAll('td')
#    results[aux[0].string] = aux[1].string
df1=df_pd[0]
# initialize the diary dictionary with own dataset 
#TO-DO - first identify if the scrapped ressults are valid or not , for example validate if it contains proper values or not 
diary_results['ta_master_court']='SC'
diary_results['ta_diary_num']=diary_num 
diary_results['ta_diary_year']=diary_year 
diary_results['ta_hdn_diary']=hdn_sc_diary_num
for index,row in df1.iterrows():
  diary_results[row[0]]=row[1]
  #print(row[0], row[1])
print (diary_results)

for key,val in diary_results.items():
 print(key,'====',val )
 #print(item)


####### gettting extended scripts for more details about diary
hdn_sc_diary_num=fetch_sc_hidden_internal_diary_num(soup)
diary_results['ta_hdn_diary_num']=hdn_sc_diary_num
print(hdn_sc_diary_num)
### getindexing details
#ret_code=get_indexing_by_diary('sc',hdn_sc_diary_num,diary_year,hdn_sc_diary_num)
court_code='sc'
ret_code=get_EarlierCourtDetails_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num)
print('earlier court details'+ret_code)
print(diary_earl_court_details)
ret_code=get_TaggedMatter_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num)
print('tagged matter'+ret_code)
print(diary_results)
ret_code=get_ListingDates_by_diary(court_code,diary_num,diary_year,hdn_sc_diary_num)
print('listing details'+ret_code)
print(diary_results)
print(diary_listing_date)




csv_output_test('','')