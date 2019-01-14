from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
from mysql_connect import MysqlPython
import labeler



url = ''

