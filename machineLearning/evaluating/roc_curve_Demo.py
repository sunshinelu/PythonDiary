# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix
import pandas as pd

import numpy as np
from sklearn import metrics
from sklearn.preprocessing import label_binarize


y = np.array([1, 1, 2, 2])
scores = np.array([0.1, 0.4, 0.35, 0.8])
fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=2)

# df = pd.DataFrame(data = fpr, columns=["fpr"])
# df["tpr"] = tpr

data = {
"fpr":fpr,
"tpr":tpr
}

df = pd.DataFrame(data = data)


auc_value = metrics.auc(fpr,tpr)

print fpr
# [0.  0.5 0.5 1. ]

print tpr
# [0.5 0.5 1.  1. ]

print thresholds
# [0.8  0.4  0.35 0.1 ]

print auc_value
# 0.75

print df
"""
   fpr  tpr
0  0.0  0.5
1  0.5  0.5
2  0.5  1.0
3  1.0  1.0
"""


y = np.array([1, 1, 2, 2])
scores = np.array([0.1, 0.4, 0.35, 0.8])

n_class = 2
y_one_hot = label_binarize(y, np.arange(n_class))  #装换成类似二进制的编码
print "y_one_hot is:"
print y_one_hot


print "=============="
print y_one_hot.ravel()
print len(y_one_hot.ravel())
print scores.ravel()
print len(scores.ravel())

fpr, tpr, thresholds = metrics.roc_curve(y_one_hot.ravel(), scores.ravel())


data = {
"fpr":fpr,
"tpr":tpr
}

df = pd.DataFrame(data = data)

print df