from lxml import html
import requests
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta
import sys
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',

'Content-Length': '18',
#'Cookie' : 'has_js=1; PHPSESSID=tuj8j2vr07fmpq5vc12ge170q4',
#'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',

}



url = "https://sci.nic.in/php/case_status/case_status_process.php"

CaseType ="7"
CaseNumber="12"
CaseYear="2018"
#s = requests.Session()
login_url= "https://sci.nic.in/php/case_status/case_status_process.php"
login_data="{ct: CaseType, cn: CaseNumber, cy: CaseYear}"
#s.post(login_url, data=login_data)
#verify=False

content = requests.post(url, data=login_data, headers=headers,verify=False)
