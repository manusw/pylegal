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
#manu mongodb testing code 
client = MongoClient('mongodb://localhost:27017')
db = client.mongo_scdetails
user_case_detail={}

#case_meta_data = []
def initialize_user_case_history(ta_user_email):

    user_case_detail['ta_user_email']='manu@ta.com'


def initialize_case_metadata(ta_master_court,ta_diary_num,ta_diary_year,ta_hdn_diary):

    case_meta_data['ta_master_court']='SC'
    case_meta_data['ta_diary_num']=ta_diary_num 
    case_meta_data['ta_diary_year']=ta_diary_year 
    case_meta_data['ta_hdn_diary']=hdn_sc_diary_num

   # diary_results['ta_hdn_diary']=hdn_sc_diary_num
for i in range(1,10):
    user_case_detail['ta_user_email']='manu@ta'+str(i)+'.com'
    case_meta_data=[]
    case_meta_data.append('SC')
    case_meta_data.append(str(i))
    case_meta_data.append('2018' )
    case_meta_data.append(str(i)+'2018')
    user_case_detail['ta_case_meta_data']=case_meta_data
    print(user_case_detail)

    usercases=db.usercases
    if '_id' in user_case_detail:
        del user_case_detail['_id'] 
    Dboresult=usercases.insert_one(user_case_detail)
    mdccasedetails=db.user_case_detail.find()
    print ('\n All data from case Database \n')
    for cd in mdccasedetails:
        print( cd)  
  