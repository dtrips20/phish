"""
Created on Sat Dec 15 21:00:42 2018

@author: Deepak Tripathi

Load PhishTank feed in DB.

"""

import os
import time
import feedparser
import ijson
import requests
import urllib.request
import shutil
import bz2
from mysql_connect import MysqlPython
import datetime
import hashlib

api_key = "9bfbd8e16dd87bda0a598ee964db349bdace48fc70b126e3362a3c581bbb1aeb"
url = 'https://data.phishtank.com/data/{0}/online-valid.json.bz2'.format(api_key)


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
        # print(stat_info.st_size)
        # unzip the json feed
        zipfile = bz2.BZ2File(file_name)  # open the file
        data = zipfile.read()  # get the decompressed data
        new_file_path = file_name[:-4]  # assuming the filepath ends with .bz2
        open(new_file_path, 'wb').write(data)  # write a uncompressed file

    return new_file_path


def parse_json_save_urls(file_name):

    total_record = 0
    record_inserted = 0
    record_found = 0
    t0 = time.time()
    with open(file_name, 'r') as f:
        parse = ijson.parse(f)
        for prefix, event, value in parse:
            if prefix == 'item.url':
                # print('prefix={}, event={}, value={}'.format(prefix, event, value))
                m = hashlib.sha256(value.encode())
                found, inserted = save_to_db(value, m.hexdigest())
                total_record += 1
                if found:
                    record_found += 1
                if inserted:
                    record_inserted += 1
    t1 = time.time()
    print("Total Records :", total_record)
    print("Time elapsed in sec ", t1 - t0)
    print("Record Inserted ", record_inserted)
    print("Record already found ", record_found)


def save_to_db(url_value, sha256):

    found = False
    inserted = False
    conditional_query = 'sha256 = %s'
    connect_mysql = MysqlPython()
    items = connect_mysql.select("urls", conditional_query, "id", sha256=sha256)
    if items:
        print("Don't insert the values ", sha256)
        found = True
    else:
        # print("insert the values")
        connect_mysql.insert("urls", url=url_value, sha256=sha256, label=1, added_date=datetime.datetime.utcnow())
        inserted = True

    return found, inserted


if __name__ == '__main__':

    cloud_url_loc, etag_has_changed = etag_changed()

    if etag_has_changed:
        print("ETag has changed")
        new_file = download_bz_file_and_decompress(cloud_url_loc)
        parse_json_save_urls(new_file)
    else:
        print("Dont parse the json as ETag has not changed")
