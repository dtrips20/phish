import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.metrics import confusion_matrix

balance_data = pd.read_csv('D:/projects/phish/test_data.csv', sep=',', header=0)

print("Dataset Length :", len(balance_data))

balance_data.head()

X = balance_data.values[:, 2:12]
# print(X)

Y = balance_data.values[:, 1]
# print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
clf_entropy = DecisionTreeClassifier(max_depth=10)

clf_entropy.fit(X_train, y_train)
score = clf_entropy.score(X_test, y_test)
print("Score :", score)

y_pred_en = clf_entropy.predict(X)
# print(y_pred_en)
# print("Accuracy is ",accuracy_score(y_test,y_pred_en)*100)

mt = confusion_matrix(Y, y_pred_en)

print("False positive rate : %f %%" % ((mt[0][1] / float(sum(mt[0]))) * 100))
print('False negative rate : %f %%' % ((mt[1][0] / float(sum(mt[1]))) * 100))
