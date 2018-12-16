#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 17:41:08 2018

@author: deepaktripathi
"""
import mysql.connector
import ipaddress  as ip
from urllib.parse import urlparse
import tldextract
import whois
from os.path import splitext


# Feature 1 : Method to count number of dots
def countdots(url):  
    return url.count('.')

# Feature 2 : Method to count number of delimeters
def countdelim(url):
    count = 0
    delim=[';','_','?','=','&']
    for each in url:
        if each in delim:
            count = count + 1
    
    return count

# Is IP addr present as th hostname, let's validate
def isip(uri):
    try:
        if ip.ip_address(uri):
            return 1
    except:
        return 0
    
#method to check the presence of hyphens
def isPresentHyphen(url):
    return url.count('-')

#count number of sub-directories
def countSubDir(url):
    return url.count('/')

def get_ext(url):
    """Return the filename extension from url, or ''."""
    
    root, ext = splitext(url)
    return ext

#count sub domains
def countSubDomain(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))

#count queries
def countQueries(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))
    
    

#end of features , start saving it.
#Create DB connection to mysql
db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Dell@123",
        database="phish"
        
        )

#set the cursor
urlCursor = db.cursor()

id = "1"
urlCursor.execute("SELECT url FROM phish_urls WHERE id=1711")
db.close()
url = str(urlCursor.fetchone()[0])
path=urlparse(url)
ext = tldextract.extract(url)

domain = '.'.join(ext[1:])

w = whois.query(domain)
print (w.__dict__)

print("Number of dots :" + str(countdots(url)))
print("Number of delim :" + str(countdelim(url)))
print("Is IP :" + str(isip(ext.domain)))
print("Is hyphen present :"+str(isPresentHyphen(path.netloc)))
print("Count sub directory :" + str(countSubDir(url)))
print()


