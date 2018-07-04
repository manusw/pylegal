import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
import requests
import pandas as pd
output_file='scilink3.csv'
class CaseDetails(object):

      
    def __init__(self,court_sub_court_type, case_no,dairy_num,case_party):
        self.court_base="SC"
        self.court_sub_court_type=court_sub_court_type
        self.case_no=case_no
        self.case_party=case_party
        self.petetinor=''
        self.diary_num=''
        


def csv_output( diary, petetinor):

                with open(output_file, 'a', encoding='utf-8') as outputfile:

                    writer = csv.writer(outputfile)
                    writer.writerow([diary, petetinor])


        #csv_output('testurl', 'test title')
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
        'PHPSESSID': 'bs4d3459o2r7of6fqg7mipmec0',
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


def get_case_data(court_type,case_num,case_year):
#        court_type='1'
#        case_num='3'
#        case_year='2018'

        data = [
                ('ct', court_type),
                ('cn', case_num),
                ('cy', case_year),
                ]
        try:
            r = requests.post('https://sci.nic.in/php/case_status/case_status_process.php', headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 30))
            print(r.content)
            print(r.text)
            soup=get_soup(r.content)
            a = CaseDetails('1',1,'dairy-123','x vs y');
            details =soup.find_all("h5")
            # check if case exist if it does not exist return a false and break the loop 
            case_dne=soup.body.findAll(text='Case Not Found')
            if case_dne:
              return 0
            case_details_pd=pd.read_html(r.content,header=0);
            print(case_details_pd)
            for item in details:
                     if("Diary No."in item.text):
                          a.diary_num=item.text
                     else:
                        a.petetinor=item.text
        
            csv_output(a.diary_num, a.petetinor)
            print(a.diary_num)
            print(a.petetinor)

                    #case_details_pd.to_csv(output_file, sep='\t', encoding='utf-8')
            for i, df in enumerate(case_details_pd):
                        df.to_csv('myfile_%s.csv' % i,mode='a')   
            return 1

        except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print (e)
                    return 0
                    sys.exit(1)
              

# write a function to scrape the 10 case for each court and every year 
# there are 41 court types and 68 years starting from 1950 to 2018
# case number can be any thing from 1-999999 
#for testing let us fetchfro case number 1-10 for every court and every year
def scrap_case_details():
    print("test")
    for court_year in range(2018,2019):
        for court_type in range(1,41):
            for case_num in range(1,999999):
                case_found=get_case_data(court_type,case_num,court_year)
                if(case_found==0):
                 print("case not found ")
                 break
       
# fetch the case details 
scrap_case_details()
#get_case_data('1','3','2018')


