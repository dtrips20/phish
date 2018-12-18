#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 17:41:08 2018

@author: deepaktripathi
"""
#import mysql.connector
import ipaddress  as ip
from urllib.parse import urlparse
import tldextract
import whois
from os.path import splitext
#import configparser
from config import read_shady_tlds_config
from config import read_shorten_url_services_config


    
#cp=configparser.ConfigParser()
#cp.read("config.ini")
#shady_tlds = eval(cp.get("shady.top.level.domains","stld"),{},{})
shady_tlds = read_shady_tlds_config()
shorten_url_services = read_shorten_url_services_config()
print("Following is the list of shady domains")
print(shady_tlds)
print("\n")
print("Following is the list of url shorting services")
print(shorten_url_services)
print("\n")

#Feature 1 : Method to count number of dots
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

# Feature 3 :Is IP addr present as th hostname, let's validate
def isip(uri):
    try:
        if ip.ip_address(uri):
            return 1
    except:
        return 0
    
#Feature 4: method to check the presence of hyphens
def isPresentHyphen(url):
    return url.count('-')

#Feature 5 : count number of sub-directories
def countSubDir(url):
    return url.count('/')

#Feature 6: Return the filename extension from url.
def get_ext(url):
    root, ext = splitext(url)
    return ext

#Feature 7 : count sub domains
def countSubDomain(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))

#Feature 8 : count queries
def countQueries(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))
    
#Feature 9 : Presense of shady domain
def shadyTLD(suffix):
    if suffix in shady_tlds:
        return 1
    else:
        return 0

#Feature 10 : Long URL to hide the suspicious part
#Rule 
#        if url length <= 75 then feature is legit:
#            else if url length > 75 then its phishing
def isSuspiciousPartHidden(url):
    if len(url) <= 75:
        return 0
    else:
        return 1

#Feature 11 : Using URL shortening services "Tiny URL"
#Rule
#   if tiny url then phishing :
#      else legitimate
def isTinyURL(url):
    if url in shorten_url_services:
        return 1
    else:
        return 0
    

#Feature 12 : URL's having "@" symbol
#Using @ symbol 

#end of features , start saving it.
    
if __name__ == '__main__':
    
    url="http://www.google.com"
    path=urlparse(url)
    print("Path :"+str(path))
    ext = tldextract.extract(url)
    
    domain = '.'.join(ext[1:])
    
    try:
        w = whois.query(domain)
    except:
        print("Unknow TDL")
    #print (w.__dict__)
    
    print("Number of dots :" + str(countdots(url)))
    print("Number of delim :" + str(countdelim(url)))
    print("Is IP :" + str(isip(ext.domain)))
    print("Is hyphen present :"+str(isPresentHyphen(path.netloc)))
    print("Count sub directory :" + str(countSubDir(url)))
    print("Count queries :"+str(countQueries(path.query)))
    print(ext.suffix + " - Supicious Shady top level domain :"+ str(shadyTLD(ext.suffix)))
    print("is suspicious part hidden :"+str(isSuspiciousPartHidden(url)))
    print("Shorted url present :"+str(isTinyURL(path.netloc)))


