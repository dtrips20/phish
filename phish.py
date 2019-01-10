import json
import os
import time
import feedparser
import ijson
import requests
import urllib.request

api_key = "9bfbd8e16dd87bda0a598ee964db349bdace48fc70b126e3362a3c581bbb1aeb"
url = 'http://data.phishtank.com/data/{0}/online-valid.json.bz2'.format(api_key)


def parse_json():

    cnt = 0
    t0 = time.time()
    with open('C:/Users/dtrips/Downloads/verified_online.json/verified_online.json', 'r') as f:
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


def etag_changed():

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
            request = requests.head(url)
            print(request.headers['Location'])
            cloud_url = request.headers['Location']
            cloud_request = requests.head(cloud_url)
            print(cloud_request.headers)
            print(cloud_request.headers['ETag'])
            f = open(file_name, 'w+')
            f.write(cloud_request.headers['ETag'])
            f.close()
            if contents == cloud_request.headers['ETag']:
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


def download_bz_file():

    file_name = url.split('/')[-1]
    u = urllib.request.urlretrieve(url, 'online-valid.json.bz2')
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print(status,)

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
    download_bz_file()
    if etag_changed():
        print("ETag has changed")
        print("Parse the JSON")
    else:
        print("Dont parse the json")
