"""
Created on Sun Dec 16 19:35:03 2018

@author: deepak tripathi

This will create feature set with label
"""
from lexical_features import LexFeature
from mysql_connect import MysqlPython

# columns
columns = ['sha256',
           'label',
           'count_dots',
           'count_delimiters',
           'is_domain_ip',
           'is_hyphen_present',
           'count_sub_dir',
           'count_sub_domain',
           'count_queries',
           'shady_tld',
           'is_suspicious_part_hidden',
           'is_tiny_url']


def save_features(url, sha256, label):
    feature = LexFeature(url)
    # return_id = None
    result = list()

    result.append(sha256)
    result.append(label)
    result.append(feature.count_dots())
    result.append(feature.count_delimiters())
    result.append(feature.is_domain_ip())
    result.append(feature.is_hyphen_present())
    result.append(feature.count_sub_dir())
    result.append(feature.count_sub_domain())
    result.append(feature.count_queries())
    result.append(feature.shady_tld())
    result.append(feature.is_suspicious_part_hidden())
    result.append(feature.is_tiny_url())

    connect_mysql = MysqlPython()
    conditional_query = 'sha256 = %s'
    items = connect_mysql.select("features", conditional_query, "id", sha256=sha256)
    if items:
        return_id = connect_mysql.update('features', conditional_query, sha256,
                                         label=result[1],
                                         count_dots=result[2],
                                         count_delimiters=result[3],
                                         is_domain_ip=result[4],
                                         is_hyphen_present=result[5],
                                         count_sub_dir=result[6],
                                         count_sub_domain=result[7],
                                         count_queries=result[8],
                                         shady_tld=result[9],
                                         is_suspicious_part_hidden=result[10],
                                         is_tiny_url=result[11]
                                         )
    else:
        return_id = connect_mysql.insert('features',
                                         sha256=result[0],
                                         label=result[1],
                                         count_dots=result[2],
                                         count_delimiters=result[3],
                                         is_domain_ip=result[4],
                                         is_hyphen_present=result[5],
                                         count_sub_dir=result[6],
                                         count_sub_domain=result[7],
                                         count_queries=result[8],
                                         shady_tld=result[9],
                                         is_suspicious_part_hidden=result[10],
                                         is_tiny_url=result[11]
                                         )
    return return_id
