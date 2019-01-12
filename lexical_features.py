"""
Created on Sat Dec 15 17:41:08 2018

@author: deepak tripathi

"""
# import mysql.connector
import ipaddress as ip
from urllib.parse import urlparse
import tldextract
import whois
from os.path import splitext
from config import read_shady_tlds_config
from config import read_shorten_url_services_config


class LexicalFeature:

    _url_to_compute = None
    _shady_tlds = read_shady_tlds_config()
    _shorten_url_services = read_shorten_url_services_config()

    def __init__(self, url_to_compute ):
        self._url_to_compute = url_to_compute

    # Feature 1 : Method to count number of dots
    def count_dots(self):
        return self._url_to_compute.count('.')

    # Feature 2 : Method to count number of delimeters
    def count_delim(self):
        count = 0
        delim = [';', '_', '?', '=', '&']
        for each in self._url_to_compute:
            if each in delim:
                count = count + 1

        return count

    # Feature 3 :Is IP addr present as th hostname, let's validate
    def is_ip(self):
        try:
            if ip.ip_address(self._url_to_compute):
                return 1
        except:
            return 0

    # Feature 4: method to check the presence of hyphens
    def is_present_hyphen(self):
        return self._url_to_compute.count('-')

    # Feature 5 : count number of sub-directories
    def count_sub_dir(self):
        return self._url_to_compute.count('/')

    # Feature 6: Return the filename extension from url.
    def get_ext(self):
        root, ext = splitext(self._url_to_compute)
        return ext

    # Feature 7 : count sub domains
    def count_sub_domain(self):


        if not sub_domain:
            return 0
        else:
            return len(sub_domain.split('.'))


    # Feature 8 : count queries
    def count_queries(query):
        if not query:
            return 0
        else:
            return len(query.split('&'))


    # Feature 9 : Presense of shady domain
    def shady_tld(suffix):
        if suffix in shady_tlds:
            return 1
        else:
            return 0


    # Feature 10 : Long URL to hide the suspicious part
    # Rule
    #        if url length <= 75 then feature is legit:
    #            else if url length > 75 then its phishing
    def is_suspicious_part_hidden(url):
        if len(url) <= 75:
            return 0
        else:
            return 1


    # Feature 11 : Using URL shortening services "Tiny URL"
    # Rule
    #   if tiny url then phishing :
    #      else legitimate
    def is_tiny_url(url):
        if url in shorten_url_services:
            return 1
        else:
            return 0


    # Feature 12 : URL's having "@" symbol
    # Using @ symbol

    # end of features , start saving it.

    if __name__ == '__main__':

        url = "http://www.google.com"
        path = urlparse(url)
        print("Path :" + str(path))
        ext = tldextract.extract(url)

        domain = '.'.join(ext[1:])

        try:
            w = whois.query(domain)
        except:
            print("Unknow TDL")
        # print (w.__dict__)

        print("Number of dots :" + str(count_dots()))
        print("Number of delim :" + str(count_delim(url)))
        print("Is IP :" + str(is_ip(ext.domain)))
        print("Is hyphen present :" + str(is_present_hyphen(path.netloc)))
        print("Count sub directory :" + str(count_sub_dir(url)))
        print("Count queries :" + str(count_queries(path.query)))
        print(ext.suffix + " - Supicious Shady top level domain :" + str(shady_tld(ext.suffix)))
        print("is suspicious part hidden :" + str(is_suspicious_part_hidden(url)))
        print("Shorted url present :" + str(is_tiny_url(path.netloc)))
