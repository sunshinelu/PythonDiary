#-*- coding: UTF-8 -*-

"""
https://blog.csdn.net/u010983763/article/details/78793528

"""
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score

# y_true = [0, 1, 2, 0, 1, 2]
# y_pred = [0, 2, 1, 0, 0, 1]

y_true = ["0", "1", "2", "0", "1", "2"]
y_pred = ["0", "2", "1", "0", "0", "1"]

print(recall_score(y_true,y_pred,average='macro'))

print(recall_score(y_true,y_pred,average='micro'))

print(recall_score(y_true,y_pred,average='weighted'))

print(recall_score(y_true,y_pred,average=None))


print(accuracy_score(y_true, y_pred))
print(accuracy_score(y_true, y_pred, normalize=False))