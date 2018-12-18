#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 18:13:08 2018

@author: deepaktripathi
"""

from configparser import ConfigParser
 
filename = 'config.ini'

def read_db_config(section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

def read_shady_tlds_config(section='shady.top.level.domains'):
    """
    Read shady top level domains.
    Currently this is hard coded for POC
    We need to curl this regularly and train the model    
    """
    
    parser = ConfigParser()
    parser.read(filename)
    
    tlds={}
    
    if parser.has_section(section):
         for item in parser.items(section):
             tlds = item[1]
             
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
        
    return tlds

def read_shorten_url_services_config(section="list.of.shorten.url.services"):
    """
    Read the list of shorten url services.
      
    """
    
    parser = ConfigParser()
    parser.read(filename)
    
    shorten_url_services={}
    
    if parser.has_section(section):
         for item in parser.items(section):
             shorten_url_services = item[1]
             
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
        
    return shorten_url_services
    
        
#if __name__ == '__main__':
    #print(read_shorten_url_services_config())