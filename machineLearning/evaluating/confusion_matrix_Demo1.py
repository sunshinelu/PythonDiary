# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix
import pandas as pd


y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]

label = list(set(y_true))

matrix = confusion_matrix(y_true, y_pred, labels=label)
matrix_df = pd.DataFrame(matrix, columns=label, index=label)

print matrix_df
"""
      ant  bird  cat
ant     2     0    0
bird    0     0    1
cat     1     0    2
"""