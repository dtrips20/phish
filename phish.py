import os
import time
import feedparser
import ijson
import requests
import urllib.request
import shutil
import bz2

api_key = "9bfbd8e16dd87bda0a598ee964db349bdace48fc70b126e3362a3c581bbb1aeb"
url = 'http://data.phishtank.com/data/{0}/online-valid.json.bz2'.format(api_key)


def parse_json(file_name):

    cnt = 0
    t0 = time.time()
    with open(file_name, 'r') as f:
        parse = ijson.parse(f)
        for prefix, event, value in parse:
            if prefix == 'item.url':
                # print('prefix={}, event={}, value={}'.format(prefix, event, value))
                url = value
                # m=hashlib.sha256(url.encode())
                print(url)#, m.hexdigest())
                cnt = cnt + 1
    t1 = time.time()
    print(cnt)
    print(t1 - t0)


def etag_changed():

    file_name = os.path.join(os.getcwd(), 'etag.txt')

    if not os.path.exists(file_name):
        print('File does not exits so create a new file')
        open(file_name, 'a').close()

    if os.path.getsize(file_name) > 0:
        f = open(file_name, 'r')
        if f.mode == 'r':
            contents = f.read()
            f.close()

            # HEAD request to PhishTank
            request = requests.head(url)
            cloud_url_location = request.headers['Location']

            # HEAD request to cloud url to check changed ETag
            cloud_request = requests.head(cloud_url_location)
            print("Saved ETag :", contents)
            print("Current ETag :", cloud_request.headers['ETag'])

            if contents == cloud_request.headers['ETag']:
                return '', False
            else:
                # save the ETag
                f = open(file_name, 'w+')
                f.write(cloud_request.headers['ETag'])
                f.close()
                return cloud_url_location, True
    else:
        print('file size is not greater than 0')
        d2 = feedparser.parse(url)
        print(d2.etag)
        f = open(file_name, 'w+')
        f.write(d2.etag)
        f.close()


def download_bz_file_and_decompress(cloud_url):

    new_file_path = ''
    file_name = (cloud_url.split('/')[-1]).split('?')[0]
    # u = urllib.request.urlretrieve(url, file_name)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    stat_info = os.stat(file_name)

    if stat_info.st_size > 0:
        print(stat_info.st_size)
        # unzip the json feed
        zipfile = bz2.BZ2File(file_name)  # open the file
        data = zipfile.read()  # get the decompressed data
        new_file_path = file_name[:-4]  # assuming the filepath ends with .bz2
        open(new_file_path, 'wb').write(data)  # write a uncompressed file

    return new_file_path



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

#value = json.loads(open("C:/Users/dtrips/Downloads/verified_online.json/verified_online.json").read())

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

    cloud_url_loc, etag_has_changed = etag_changed()

    if etag_has_changed:
        print("ETag has changed")
        new_file = download_bz_file_and_decompress(cloud_url_loc)
        parse_json(new_file)
    else:
        print("Dont parse the json as ETag has not changed")