#-*- coding: UTF-8 -*-


import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC

X = np.array([[-1,-1],[-2,-1],[1,1],[2,1],[-1,1],[-1,2],[1,-1],[1,-2]])
y = np.array([0,0,1,1,1,1,0,1])


# clf = SVC(probability=True)
clf = SVC(kernel = "linear",probability=True)
clf.fit(X, y)

print(clf.decision_function(X))


print(clf.predict(X))

print(clf.predict_proba(X)) #这个是得分,每个分类器的得分，取最大得分对应的类。