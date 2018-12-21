#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 19:35:03 2018

@author: deepaktripathi

This will create feature set with label
"""
from __future__ import division
import pandas as pd
import mysql.connector
from ComputeUrlFeatures import countdots,isPresentHyphen,shadyTLD
#import ComputeUrlFeatures
from urllib.parse import urlparse
import tldextract
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle as pkl
from pandas.io import sql
from mysql_connect import MysqlPython
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pickle as pkl
import sklearn.ensemble as ek
from sklearn import  tree, linear_model
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import graphviz



db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Dell@123",
        database="phish"
        
        )
urlCursor = db.cursor()

featureSet = pd.DataFrame(columns=("url", \
                                   "number of dots in sub-domain", \
                                   "is hyphen present", \
                                   "length of the url", \
                                   "Shady_TLDS", \
                                   "label"))

def GetFeatures(url,label):
    result = []
    
    ext = tldextract.extract(url)
    #url = str(url)
    #print(url)
    #append the url to the result feature
    result.append(url)
    
    #parse the URL and extract the domain information
    path = urlparse(url)
    #ext = tldextract.extract(url)
    
    #counting number of dots in subdomain
    result.append(countdots(url))
    
    #checking hyphen in domain   
    result.append(isPresentHyphen(path.netloc))
    
    #length of URL    
    result.append(len(url))
    
    #checking @ in the url    
    result.append(shadyTLD(ext.suffix))
    
    result.append(str(label))
    
    return result

if __name__=='__main__':
    
     #connect_mysql = MysqlPython()
     
     #items = connect_mysql.select('urls', None,'url','label')
     #print(items)
     #df = pd.DataFrame.from_records(items)
     #print(range(len(df)))
     #df = pd.DataFrame(items)
     
     df = pd.read_sql("select url,label from urls",con = db)
     db.close()
     urlCursor.close()
     print(range(len(df)))
     
     #features = getFeatures(df["URL"].loc[i], df["Lable"].loc[i])  
     
     #i=0
     for i in range(len(df)):
         
         features = GetFeatures(df["url"].loc[i], df["label"].loc[i])
         featureSet.loc[i] = features
        
     print(featureSet.head())
     """   
     sns.set(style="darkgrid")
     sns.distplot(featureSet[featureSet['label']=='0']['length of the url'],color='green',label='Benign URLs')
     sns.distplot(featureSet[featureSet['label']=='1']['length of the url'],color='red',label='Phishing URLs')
     sns.plt.title('Url Length Distribution')
     plt.legend(loc='upper right')
     plt.xlabel('Length of URL')

     sns.plt.show()
     """
     fz = featureSet.groupby(featureSet['label']).size()
     print(fz)
     
     X = featureSet.drop(['url','label'],axis=1).values
     y = featureSet['label'].values
   
     X_train, X_test , y_train, y_test  = train_test_split(X,y,test_size=0.2)
     
     model = { "DecisionTree":tree.DecisionTreeClassifier(max_depth=2),
         "RandomForest":ek.RandomForestClassifier(n_estimators=50),
         "Adaboost":ek.AdaBoostClassifier(n_estimators=50),
         "GradientBoosting":ek.GradientBoostingClassifier(n_estimators=50),
         "GNB":GaussianNB(),
         "LogisticRegression":LogisticRegression()   
            }
    
     results = {}
     for algo in model:
         clf = model[algo]
         #print(clf)
         clf.fit(X_train,y_train)
         
         score = clf.score(X_test,y_test)
         
         print ("%s : %s " %(algo, score))
         
         results[algo] = score
         
     winner = max(results, key=results.get)
     print(winner)
     
     
     clf = model[winner]
     res = clf.predict(X)
     mt = confusion_matrix(y, res)
     print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0])))*100))
     print('False negative rate : %f %%' % ( (mt[1][0] / float(sum(mt[1]))*100)))

     #dot_data = tree.export_graphviz(clf, out_file=None)
         
    
        
    #sql.write_frame(df,con=db, name='table_name_for_df', if_exists='replace', flavor='mysql')


