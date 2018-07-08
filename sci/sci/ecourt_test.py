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


cookies = {
    'PHPSESSID': 'lcp5jrvo4pjab8mkmafn7h1i45',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://services.ecourts.gov.in/ecourtindia_v5.1/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('case_no', '203601009012015'),
    ('state_cd', '1'),
    ('dist_cd', '19'),
    ('court_code', '4'),
    ('appFlag', ''),
    ('national_court_code', 'MHAU01'),
    ('court_complex_code', ''),
    ('cino', 'MHAU010000112015'),
)

response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_civil_case_history.php', headers=headers, params=params, cookies=cookies)
print(response)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://services.ecourts.gov.in/ecourtindia_v5.1/cases_qry/o_civil_case_history.php?case_no=203601009012015^&state_cd=1^&dist_cd=19^&court_code=4^&appFlag=^&national_court_code=MHAU01^&court_complex_code=^&cino=MHAU010000012015', headers=headers, cookies=cookies)