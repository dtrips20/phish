#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 19:35:03 2018

@author: deepaktripathi

This will create feature set with label
"""

import pandas as pd
import mysql.connector
from ComputeUrlFeatures import countdots,isPresentHyphen
from urllib.parse import urlparse
import tldextract
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle as pkl
from pandas.io import sql
from mysql_connect import MysqlPython




featureSet = pd.DataFrame(columns=("url", \
                                   "number of dots in sub-domain", \
                                   "is hyphen present", \
                                   "length of the url", \
                                   "label"))

def GetFeatures(url,label):
    result = []
    #url = str(url)
    #print(url)
    #append the url to the result feature
    result.append(url)
    
    #parse the URL and extract the domain information
    path = urlparse(url)
    #ext = tldextract.extract(url)
    
    #counting number of dots in subdomain
    result.append(countdots(url))
    
    #checking hyphen in domain   
    result.append(isPresentHyphen(path.netloc))
    
    #length of URL    
    result.append(len(url))
    
    #checking @ in the url    
    #result.append(ComputeUrlFeatures.isPresentHyphen(path.netloc))
    
    result.append(label)
    
    return result

if __name__=='__main__':
    
     connect_mysql = MysqlPython()
     
     items = connect_mysql.select('urls', None,'url','label')
     #print(items)
     #df = pd.DataFrame.from_records(items)
     #print(range(len(df)))
     #df = pd.DataFrame(items)
     i=0
     for item in items:
         #print(item[0],item[1])
         features = GetFeatures(item[0],item[1])
         featureSet.loc[i] = features
         i=i+1
        
    #sql.write_frame(df,con=db, name='table_name_for_df', if_exists='replace', flavor='mysql')


