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

try:    
    lastrecord=db.casedetail.find({},{'ta_hdn_diary_num':1,'ta_diary_num': 1,'ta_diary_year': 1,'_id': 0}).sort('_id',pymongo.DESCENDING).limit(1)
except:
    raise

for item  in lastrecord:
    print(item)
def Fetch_all_from_mongo():
    try:
        mdccasedetails=db.casedetail.find()
        print ('\n All data from case Database \n')
        for cd in mdccasedetails:
            print( cd)

    except :
        raise

#helperfunction for testing 
def updatemanymongo():
    try:
        criteria = '123'
        ta_diary_year = '2017'
        
        db.casedetail.update_many(
            {"ta_diary_num": criteria},
            {
            "$set": {
                "ta_diary_year":'2019',
            },
            
            }
        )
        print( "Records updated successfully")    
    
    except:
        raise
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
# insert a  record 
#    try:
#        mdccasedetails=db.casedetail
#        dboresult=mdccasedetails.insert_one(diary_results)
#        print('one casedetail: {0}'.format(dboresult.inserted_id))
#    except:
#        print('mongo db error')