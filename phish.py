import ijson
import mysql.connector
import urllib.request, json
import hashlib
from datetime import datetime
import time
import requests
import feedparser
import os

'''
https://pythonhosted.org/feedparser/http-etag.html

ETag and Last-Modified Headers
ETags and Last-Modified headers are two ways that feed publishers can save bandwidth, 
but they only work if clients take advantage of them. 
Universal Feed Parser gives you the ability to take advantage of these features, but you must use them properly.

The basic concept is that a feed publisher may provide a special HTTP header, called an ETag,when it publishes a feed. 
You should send this ETag back to the server on subsequent requests. 
If the feed has not changed since the last time you requested it, 
the server will return a special HTTP status code (304) and no feed data

'''
api_key = '9bfbd8e16dd87bda0a598ee964db349bdace48fc70b126e3362a3c581bbb1aeb'


def parse_json():
    cnt = 0
    t0 = time.time()
    with open('C:/Users/dtrips/Downloads/verified_online.json/verified_online.json', 'r')  as f:
        parse = ijson.parse(f)
        for prefix, event, value in parse:
            if prefix == 'item.url':
                # print('prefix={}, event={}, value={}'.format(prefix, event, value))
                # url = value
                # m=hashlib.sha256(url.encode())
                # print ( url , m.hexdigest())
                cnt = cnt + 1
    t1 = time.time()
    print(cnt)
    print(t0 - t1)


def etag_changed_in_header():
    url = 'http://data.phishtank.com/data/{0}/online-valid.json.bz2'.format(api_key)

    file_name = os.path.join(os.getcwd(), 'etag.txt')
    print(file_name)

    if not os.path.exists(file_name):
        print('File does not exits so create a new file')
        open(file_name, 'a').close()

    if os.path.getsize(file_name) > 0:
        print('file size is greater than 0')
        f = open(file_name, 'r')
        if f.mode == 'r':
            contents = f.read()
            print(contents)
            f.close()
            resq = requests.head(url)
            print(resq.headers['Location'])
            cloud_url = resq.headers['Location']
            resq = requests.head(cloud_url)
            print(resq.headers['ETag'])
            f = open(file_name, 'w+')
            f.write(resq.headers['ETag'])
            f.close()
            if contents == resq.headers['ETag']:
                return False
            else:
                return True
    else:
        print('file size is not greater than 0')
        d2 = feedparser.parse(url)
        print(d2.etag)
        f = open(file_name, 'w+')
        f.write(d2.etag)
        f.close()


# resp = requests.head(url)
# print (resp.history , resp.text, resp.headers)


'''
db = mysql.connector.connect(
        host="192.168.1.4",
        user="root",

        passwd="Dell@123",
        database="phish"
        
        )

urlCursor = db.cursor()
insertedRecords = 0 
sql = "INSERT into urls (url,sha256 , label , added_date) values ( %s , %s, %s, %s)"

'''

value = json.loads(open("C:/Users/dtrips/Downloads/verified_online.json/verified_online.json").read())

'''
for url in urls:
    # print(url)
    m = hashlib.sha256(url.encode())
    # print(m.hexdigest())
    val = (url,m.hexdigest(),1,datetime.utcnow())
    urlCursor.execute(sql,val)
    insertedRecords= insertedRecords + urlCursor.rowcount
    
db.commit()
db.close()

print("Record inserted")
'''
if __name__ == '__main__':

    if etag_changed_in_header():
        print("ETag has changed")
        print("Parse the JSON")
    else:
        print("Dont parse the json")
