"""
Created on Sat Dec 15 17:41:08 2018

@author: deepak tripathi

"""

import ipaddress as ip
from urllib.parse import urlparse
import tldextract
# import whois
# from os.path import splitext
from config import read_shady_tlds_config
from config import read_shorten_url_services_config


class LexFeature:
    _url_to_compute = None
    _shady_tlds = None
    _shorten_url_services = None

    def __init__(self, url_to_compute):
        self._url_to_compute = url_to_compute
        self._shady_tlds = read_shady_tlds_config()
        self._shorten_url_services = read_shorten_url_services_config()

    # Feature 1: Method to count number of dots
    def count_dots(self):
        return self._url_to_compute.count('.')

    # Feature 2: Method to count number of delimiters
    def count_delimiters(self):
        count = 0
        delimiters = [';', '_', '?', '=', '&']
        for each in self._url_to_compute:
            if each in delimiters:
                count = count + 1

        return count

    # Feature 3: Is IP addr present as th hostname, let's validate
    def is_domain_ip(self):

        try:
            ext = tldextract.extract(self._url_to_compute)
            ip_address = ip.ip_address(ext.domain)
            if ip_address:
                return 1
        except Exception as e:
            return 0

    # Feature 4: method to check the presence of hyphens
    def is_present_hyphen(self):
        return self._url_to_compute.count('-')

    # Feature 5: count number of sub-directories
    def count_sub_dir(self):
        return self._url_to_compute.count('/')

    # Feature 6: count sub domains
    def count_sub_domain(self):

        extract = tldextract.extract(self._url_to_compute)
        sub_domain = extract.subdomain

        if not sub_domain:
            return 0
        else:
            return len(sub_domain.split('.'))

    # Feature 7: count queries
    def count_queries(self):

        parsed_url = urlparse(self._url_to_compute)

        if not parsed_url.query:
            return 0
        else:
            return len(parsed_url.query.split('&'))

    # Feature 8: Presence of shady domain
    def shady_tld(self):

        extract = tldextract.extract(self._url_to_compute)

        if extract.suffix in self._shady_tlds:
            return 1
        else:
            return 0

    # Feature 9: Long URL to hide the suspicious part
    # Rule
    #        if url length <= 75 then feature is legit:
    #            else if url length > 75 then its phishing
    def is_suspicious_part_hidden(self):
        if len(self._url_to_compute) <= 75:
            return 0
        else:
            return 1

    # Feature 10: Using URL shortening services "Tiny URL"
    # Rule
    #   if tiny url then phishing :
    #      else legitimate
    def is_tiny_url(self):

        parsed_url = urlparse(self._url_to_compute)

        if parsed_url.netloc in self._shorten_url_services:
            return 1
        else:
            return 0

    # Feature 11: URL's having "@" symbol
    # Using @ symbol

    # end of features , start saving it.
