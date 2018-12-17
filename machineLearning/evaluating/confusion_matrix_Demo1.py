# -*- coding: utf-8 -*-

from sklearn.metrics import confusion_matrix
import pandas as pd


y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]

label = list(set(y_true))

n = len(label)
lst = []

for i in range(n):
    # lst = lst + ["lable_" + str(i)] # 方法一
    lst.append("lable_" + str(i))  # 方法二

print lst
# ['lable_0', 'lable_1', 'lable_2']

lst = list(lst)

matrix = confusion_matrix(y_true, y_pred, labels=label)
matrix_df = pd.DataFrame(matrix, columns=label, index=label)

print matrix_df
"""
      ant  bird  cat
ant     2     0    0
bird    0     0    1
cat     1     0    2
"""

matrix_df2 = pd.DataFrame(matrix, columns=lst, index=lst)
print matrix_df2
"""
         lable_0  lable_1  lable_2
lable_0        2        0        0
lable_1        0        0        1
lable_2        1        0        2

"""