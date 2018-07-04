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
def get_soup(html):
                if html is not None:
                    soup = BeautifulSoup(html, 'lxml')
                    return soup
                else:
                    return
        ## find data 
def get_display_board_data(soup):

    try:
        table = soup.find_all('table', {"class":"board_id"})
        #print(table)
      
    #title = soup.find('title').get_text().strip().replace('\n','')
    except:
        table = None


def get_displayboard_request(url,headers,cookies):
    try:
        
        
        res = requests.post('https://sci.nic.in/php/display/get_board.php', headers=headers, cookies=cookies,verify=False,timeout=(3, 30))
        res.raise_for_status()
        print(res.content)
        #soup=get_soup(res.content)
        #table = soup.find('table', id="ctl00_SPWebPartManager1_g_c001c0d9_0cb8_4b0f_b75a_7cc3b6f7d790_ctl00_HistoryData1_gridHistoryData_DataGrid1")
    except requests.HTTPError as e:
        logging.warning('SC Display return non-200 status code')
        raise e
    except requests.RequestException as e:
        logging.warning('Issue retrieving SC results page')
        raise e
    except ConnectionError as e:
        raise e
    else:
        return res

def get_sc_displayboard():
    sc_display_url='https://sci.nic.in/php/display/get_board.php'
    cookies = {
        'has_js': '1',
        'PHPSESSID': '8j1pgblhj22d21rejvdinvehg1',
    }

    headers = {
        'Origin': 'https://sci.nic.in',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://sci.nic.in/display-board',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Content-Length': '0',
    }
    response=get_displayboard_request(sc_display_url,headers,cookies)
    return response

res=get_sc_displayboard()
soup=get_soup(res.content)
display_table=get_display_board_data(soup)
print(display_table)
dis=pd.read_html(res.content,header=0)
print (dis)