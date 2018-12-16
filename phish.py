# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import mysql.connector
from urllib import request
import hashlib
from datetime import datetime

db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Dell@123",
        database="phish"
        
        )

urlCursor = db.cursor()
insertedRecords = 0 
sql = "INSERT into phish_urls (url,sha256 , label , added_date) values ( %s , %s, %s, %s)"

r = request.urlopen("https://openphish.com/feed.txt")
bytecode = r.read()
htmlstr = bytecode.decode()

urls = htmlstr.split('\n')

for url in urls:
    #print(url)
    m = hashlib.sha256(url.encode())
    #print(m.hexdigest())
    val = (url,m.hexdigest(),1,datetime.utcnow())
    urlCursor.execute(sql,val)
    insertedRecords= insertedRecords + urlCursor.rowcount
    
db.commit()
db.close()

print(insertedRecords,"Record inserted")


