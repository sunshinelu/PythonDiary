# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix
import pandas as pd

import numpy as np
from sklearn import metrics


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

print tpr

print thresholds

print auc_value

print df
