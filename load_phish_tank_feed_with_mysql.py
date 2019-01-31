"""
Created on Sat Dec 15 21:00:42 2018

@author: Deepak Tripathi

Load PhishTank feed in DB.

"""

#  Copyright (c) 2019. [Deepak Tripathi]
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.

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
from logging.handlers import TimedRotatingFileHandler
import mysql.connector
from config import read_db_config



db_config = read_db_config()

print(db_config)
logger = logging.getLogger("PhisTank feed log")
logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(filename='logs/PhishTankFeed.log', when='h', interval=1, backupCount=0,
                                   encoding=None, delay=False, utc=False)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

api_key, url = read_phishtank_feed_config()
url = url.format(api_key)

_headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/61.0.3163.100 Safari/537.36"}


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
                cnx = mysql.connector.connect(**db_config)
                cursor = cnx.cursor()
                query = ("select id from urls where url_sha256='{0}'".format(m.hexdigest()))
                cursor.execute(query)
                item = cursor.fetchall()
                cursor.close()
                cnx.close()


                if item:
                    print("Don't insert the values {0}".format(m.hexdigest()))
                    record_found += 1

                else:
                    extract = tldextract.extract(phish_url)
                    inserted = save_to_db(phish_url, m.hexdigest(),
                                          extract.subdomain, extract.domain, extract.suffix,
                                          extract.registered_domain, target)
                    if inserted:
                        record_inserted += 1
                        print("Added {0} URL {1}".format(record_inserted, m.hexdigest()))

    t1 = time.time()
    logger.info("Total Records :{0}".format(total_record))
    logger.info("Time elapsed in sec {0}".format(t1 - t0))
    logger.info("Record Inserted {0}".format(record_inserted))
    logger.info("Record already found {0}".format(record_found))


def save_to_db(url_value, sha256, sub_domain, domain, suffix, registered_domain, target):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    add_url = ("insert into urls "
               "(url, url_sha256, source, label,added_date, sub_domain, domain, suffix, registered_domain, target)"
               "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

    data_url = (url_value, sha256,'PhishTank', '1', datetime.datetime.now(), sub_domain, domain, suffix, registered_domain, target)

    cursor.execute(add_url,data_url)
    cnx.commit()
    cursor.close()
    cnx.close()
    inserted = True

    return inserted


def main():
    # HEAD request to PhishTank
    request = requests.head(url)
    cloud_url_location = request.headers['Location']

    # HEAD request to cloud url to check changed ETag
    cloud_request = requests.head(cloud_url_location)
    etag = cloud_request.headers['ETag']
    logger.info("Current ETag :{0}".format(etag))

    file_name = os.path.join(os.getcwd(), 'etag.txt')

    if not os.path.exists(file_name):
        print('File does not exits so create a new file')
        open(file_name, 'a').close()

    if os.path.getsize(file_name) > 0:
        f = open(file_name, 'r')
        if f.mode == 'r':
            contents = f.read()
            f.close()

            if contents == etag:
                logger.info("Dont parse the json as ETag has not changed")
            else:
                logger.info("ETag has changed")
                new_file = download_bz_file_and_decompress(cloud_url_location)
                parse_csv_save_urls(new_file)
                file_name = os.path.join(os.getcwd(), 'etag.txt')
                f = open(file_name, 'w+')
                f.write(etag)
                f.close()
    else:
        print('file size is not greater than 0')
        d2 = feedparser.parse(url)
        print(d2.etag)
        f = open(file_name, 'w+')
        f.write(d2.etag)
        f.close()


if __name__ == '__main__':
    logger.info("Phish tank feed started")
    logger.info("PhishTank API key is :{0}".format(api_key))
    logger.info("PhishTank URL {0}".format(url))
    #main()
    parse_csv_save_urls('verified_online.csv')
    logger.info("Phish tank feed ended")
