"""
Author : Deepak Tripathi

Date : Dec 21 , 2018

"""

from contextlib import closing
from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from time import sleep


class Feature:
    _url_to_compute = None

    _headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/61.0.3163.100 Safari/537.36"}

    def __init__(self, url_to_compute):
        self._url_to_compute = url_to_compute

    def log_error(self, e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(self._url_to_compute, e)

        # create a fake user agent so it looks like a real query.

    def is_good_response(self, resp):
        url = self._url_to_compute
        print(url)
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        print(resp.status_code)
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

    """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
    """

    def simple_get(self):

        """
          Attempts to get the content at `url` by making an HTTP GET request.
          If the content-type of response is some kind of HTML/XML, return the
          text content, otherwise return None.
          """
        try:

            resp = get(self._url_to_compute, headers=self._headers, stream=True, verify=False)
            if self.is_good_response(resp):
                return resp.content
            else:
                return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(self._url_to_compute, str(e)))
            return None
        except ConnectionError:
            print('Web site does not exist')
            return None

    '''
        Features:
        URL of anchor Anchors in a normal web page usually point to pages in the same domain.
        For phishing pages, there are three possible abnormalities listed below. 
        In the following, let A(a) be the total number of anchors in page (P).
        Nil anchor : An anchor is called a nil anchor if it points to nowhere. 
        Examples are <a href=“#”>, 
                     <a href=“#skip”>,
                     <a href=“javascript::void(0)”>, etc. 
    
        The percentage of nil anchors in a page reflects the degree of suspicious.
        The higher the percentage, the more likely that P is a phishing page.
    
        if total number of anchor ==  0 then 0
        if  nil anchor > 0 the nil anchor / total number of anchor
        otherwise -1 
    '''

    def anchor_in_url(self):

        no_href = 0
        href = 0
        total_href = 0
        #sleep(2)
        print("Url to compute :", self._url_to_compute)
        raw_html = self.simple_get()
        if raw_html:
            html = BeautifulSoup(raw_html, 'html.parser')
            for a in html.select('a'):
                if a.has_attr('href'):
                    total_href = total_href + 1
                    if a['href'].startswith("#") or a.__contains__('javascript::void(0)'):
                        print(a['href'])
                        no_href = no_href + 1
                    else:
                        href = href + 1

            if total_href == 0:
                return 0
            elif total_href > 0:
                result = no_href / total_href
                if result > 0:
                    return result
                else:
                    return -1
        else:
            print("Bad request")
            return -1


f = Feature("https://www.all-today.com")
print(f.anchor_in_url())
