import csv
from mysql_connect import MysqlPython
import os

file = 'test_data.csv'

connect_mysql = MysqlPython()

conditional_query = 'label = %s'

items = connect_mysql.select('features', conditional_query, 'label', 'count_dots', 'count_delimiters', 'is_domain_ip',
                             'is_hyphen_present',
                             'count_sub_dir',
                             'count_sub_domain', 'count_queries', 'shady_tld', 'is_suspicious_part_hidden',
                             'is_tiny_url', label='1')

# Getting Field Header names
column_names = ['label', 'count_dots', 'count_delimiters', 'is_domain_ip', 'is_hyphen_present', 'count_sub_dir',
                'count_sub_domain', 'count_queries', 'shady_tld', 'is_suspicious_part_hidden', 'is_tiny_url']

file_name = os.path.join(os.getcwd(), file)
fp = open(file_name, 'w')

myFile = csv.writer(fp, lineterminator='\n')  # use line terminator for windows
myFile.writerow(column_names)
myFile.writerows(items)
fp.flush()
fp.close()
