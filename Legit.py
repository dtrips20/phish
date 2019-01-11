"""
Created on Sat Dec 15 21:00:42 2018

@author: Deepak Tripathi

This module will load verified non-phish site for training.
We may need to find another way to get verified non-phish site.
For prototype this could be good.

"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
from mysql_connect import MysqlPython


phishTankLegitUrls="https://www.phishtank.com/phish_search.php?page=4&valid=n&Search=Search"

# create a fake user agent so it looks like a real query.
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/61.0.3163.100 Safari/537.36"}


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:

        with closing(get(url,headers=headers, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
        

if __name__ == "__main__":
    raw_html = simple_get(phishTankLegitUrls)
    #print("Length of raw html " + str(len(raw_html)))
    html = BeautifulSoup(raw_html, 'html.parser')
    connect_mysql = MysqlPython()
    insertedRecords = 0 
    sql = "INSERT into urls (url,sha256 , label , added_date) values ( %s , %s, %s, %s)"

    for a in html.select('a'):
        if "phish_detail.php"  in a['href']:
            #print(a['href'])
            raw_html = simple_get("https://www.phishtank.com/"+a['href'])
            html = BeautifulSoup(raw_html, 'html.parser')
            for a in html.select('a'):
                if 'visit the site' in a.text:
                    url = a['href']
                    m = hashlib.sha256(url.encode())
                    connect_mysql.insert('urls',url=url,sha256=m.hexdigest(),label=0,added_date=datetime.utcnow())
print("Record inserted")