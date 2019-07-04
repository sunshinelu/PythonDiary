import pandas as pd
import pymysql
import numpy as np
"""

dataframe 按照行或者列排序
https://blog.csdn.net/Asher117/article/details/84502952

"""
# 生成frame
frame = pd.DataFrame(pd.Series([3, 5, 2, 6, 9, 23, 12, 34, 12, 15, 11, 0]).values.reshape(3, 4), columns=['c', 'f', 'd', 'a'],
                     index=['C', 'A', 'B'])

print(frame)

#按frame的行索引进行排序
print(frame.sort_index())

print("========")
#按frame的行索引'A'进行排序
# print(frame.sort_index(axis = 1, by='A',ascending=False))
print(frame.sort_values(axis = 1, by='A',ascending=False))

print("========")
# 截取前两行前三列
print(frame.iloc[0:2,0:3])