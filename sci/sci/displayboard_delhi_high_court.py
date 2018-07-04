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
        
        
        res = requests.get('http://delhihighcourt.nic.in/displayboardM.asp', headers=headers, cookies=cookies,timeout=(3, 30))
        res.raise_for_status()
        print(res.content)
        #soup=get_soup(res.content)
        #table = soup.find('table', id="ctl00_SPWebPartManager1_g_c001c0d9_0cb8_4b0f_b75a_7cc3b6f7d790_ctl00_HistoryData1_gridHistoryData_DataGrid1")
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

def get_delhi_hc_displayboard():
    dhc_display_url='http://delhihighcourt.nic.in/displayboardM.asp'
    cookies = {
        'ASPSESSIONIDCQACCSRD': 'JJKGBPLDLJFNDEGCMPFJHOIM',
        'ASPSESSIONIDCQBBCTRC': 'GJDHABMDOPEGFKOCGALEDDJG',
        'ASPSESSIONIDASDBDTRD': 'PDNLADMDDMFOLLLCPIAABDKN',
        'ASPSESSIONIDCSCACSQC': 'GPJNAFMDKAEPDLDKBAOOHMEG',
        'ASPSESSIONIDCSDDBSQC': 'NKKLAHMDFBAGCIKNCLEHICGL',
        'ASPSESSIONIDAQCABTRC': 'MEHBBJMDKJDHFJLKEOGHADLB',
        'ASPSESSIONIDASCCASQD': 'JJOCALMDEGMPFEOEMGIDELJO',
        'ASPSESSIONIDASDDDSQD': 'KJKEBNMDCKPKOHBFDAPDNGGG',
        'ASPSESSIONIDCQDACSRC': 'KOOJPOMDFAHNEBKEJOAFDLPL',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response=get_displayboard_request(dhc_display_url,headers,cookies)
    return response

res=get_delhi_hc_displayboard()
soup=get_soup(res.content)
display_table=get_display_board_data(soup)
print(display_table)
dis=pd.read_html(res.content,header=0)
print (dis)
