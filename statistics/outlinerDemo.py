# -*- coding: utf-8 -*-

"""
功能描述：
使用Z标准化得到的阀值作为判断标准：当标准化后的得分超过阀值则为异常。
"""

import pandas as pd # 导入pandas库
import numpy as np

# 生成异常数据
df = pd.DataFrame({'col1': [1, 120, 3, 5, 2, 12, 13],
                   'col2':[12, 17, 31, 53, 22, 32, 43],
                   'col3':[10, 27, 33, 53, 12, 12, 143]})
print (df) # 打印输出
"""
   col1  col2  col3
0     1    12    10
1   120    17    27
2     3    31    33
3     5    53    53
4     2    22    12
5    12    32    12
6    13    43   143
"""

# 通过Z-Score方法判断异常值
df_zscore = df.copy() # 复制一个用来存储Z-score得分的数据框

cols = df.columns # 获得数据框的列名
for col in cols: # 循环读取每列
    df_col = df[col] # 得到每列的值
    z_score = (df_col - df_col.mean()) / df_col.std() # 计算每列的Z-score得分
    df_zscore[col] = z_score.abs() > 2.2 # 判断Z-score得分是否大于2.2，如果是则是True，否则为False
print (df_zscore) # 打印输出
"""
    col1   col2   col3
0  False  False  False
1   True  False  False
2  False  False  False
3  False  False  False
4  False  False  False
5  False  False  False
6  False  False  False
"""

df[df_zscore] = None
print "df is: "
print df

"""
   col1  col2  col3
0   1.0    12    10
1   NaN    17    27
2   3.0    31    33
3   5.0    53    53
4   2.0    22    12
5  12.0    32    12
6  13.0    43   143
"""