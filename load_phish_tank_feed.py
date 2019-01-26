"""
Created on Sat Dec 15 21:00:42 2018

@author: Deepak Tripathi

Load PhishTank feed in DB.

"""

# TODO:'Write the ETag changes after the update in DB is complete so that we can run the prog again incase of failure.'
import bz2
import csv
import datetime
import hashlib
import os
import shutil
import time
import urllib.request
import feedparser
import requests
import tldextract
import logging
from config import read_phishtank_feed_config
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

from export_csv import file_name
from mysql_connect import MysqlPython

fh = TimedRotatingFileHandler(filename="logs/PhishTankFeed", interval=1, when='M',  backupCount=20)
fh.suffix= '%Y_%m_%d.log'


logger = logging.getLogger("PhisTank feed log")
logger.addHandler(fh)
logger.setLevel(logging.INFO)


api_key , url =  read_phishtank_feed_config()
url = url.format(api_key)

_headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36"}


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


def parse_csv_save_urls(file_name):
    total_record = 0
    record_inserted = 0
    record_found = 0
    t0 = time.time()

    with open(file_name, 'r') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader)
        count = 0
        for row in data_reader:

            total_record += 1

            phish_url = row[1]
            verified = row[4]
            online = row[6]
            target = row[7]

            if verified == "yes" and online == "yes":
                count = count + 1
                m = hashlib.sha256(phish_url.encode())
                conditional_query = 'url_sha256 = %s'
                connect_mysql = MysqlPython()
                items = connect_mysql.select("urls", conditional_query, "id", url_sha256=m.hexdigest())

                if items:
                    print("Don't insert the values ", m.hexdigest())
                    record_found += 1

                else:
                    extract = tldextract.extract(phish_url)
                    inserted = save_to_db(phish_url, m.hexdigest(),
                                          extract.subdomain, extract.domain, extract.suffix,
                                          extract.registered_domain, target)
                    if inserted:
                        record_inserted += 1

    t1 = time.time()
    print("Total Records :", total_record)
    print("Time elapsed in sec ", t1 - t0)
    print("Record Inserted ", record_inserted)
    print("Record already found ", record_found)


def save_to_db(url_value, sha256, subdomain, domain, suffix, registered_domain, target):
    connect_mysql = MysqlPython()
    connect_mysql.insert("urls", url=url_value, url_sha256=sha256, source='PhishTank', label=1,
                         added_date=datetime.datetime.utcnow()
                         , sub_domain=subdomain, domain=domain, suffix=suffix, registered_domain=registered_domain,
                         target=target)
    inserted = True

    return inserted


def main():
    cloud_url_loc, etag_has_changed = etag_changed()

    if etag_has_changed:
        print("ETag has changed")
        new_file = download_bz_file_and_decompress(cloud_url_loc)
        parse_csv_save_urls(new_file)
    else:
        print("Dont parse the json as ETag has not changed")


if __name__ == '__main__':
    logger.info("Phish tank feed started")
    print(api_key)
    print(url)
    #main()
    # parse_csv_save_urls('verified_online.csv')
