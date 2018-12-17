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




#Create DB connection to mysql
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Dell@123",
        database="phish"
        
        )

df = pd.read_sql('SELECT * FROM phish_urls', con=db)
db.close()

print(str(range(len(df))))

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
    #result.append(ComputeUrlFeatures.isPresentHyphenesentAt(path.netloc))
    
    result.append(label)
    
    return result

for i in range(len(df)):
    
    features = GetFeatures(df["url"].loc[i],df["label"].loc[i])
    featureSet.loc[i] = features
    



