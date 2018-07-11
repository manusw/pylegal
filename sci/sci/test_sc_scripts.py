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
import re
import time
import pymongo
import pymongo
from pymongo import MongoClient

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

data = [
  ('d_no', '1'),
  ('d_yr', '2017'),
]
response = requests.post('https://sci.nic.in/php/case_status/case_status_process.php', headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 120))

#response = requests.post('https://www.sci.nic.in/php/case_status/case_status_process.php', headers=headers, cookies=cookies, data=data,verify=False,timeout=(3, 120))
print(response.content)
