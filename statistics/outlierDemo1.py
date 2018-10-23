# -*- coding: utf-8 -*-

"""
参考链接：
3.1 数据清洗：缺失值、异常值和重复值的处理-2代码实操
https://www.dataivy.cn/blog/3-1-%E6%95%B0%E6%8D%AE%E6%B8%85%E6%B4%97%EF%BC%9A%E7%BC%BA%E5%A4%B1%E5%80%BC%E3%80%81%E5%BC%82%E5%B8%B8%E5%80%BC%E5%92%8C%E9%87%8D%E5%A4%8D%E5%80%BC%E7%9A%84%E5%A4%84%E7%90%86-2%E4%BB%A3%E7%A0%81/
"""
import pandas as pd # 导入pandas库
import numpy as np

# 生成异常数据
df = pd.DataFrame({'col1': [1, 120, 3, 5, 2, 12, 13],'col2':[12, 17, 31, 53, 22, 32, 43],'col3':[10, 27, 33, 53, 12, 12, 143]})
print (df) # 打印输出

# 通过Z-Score方法判断异常值
df_zscore = df.copy() # 复制一个用来存储Z-score得分的数据框
print df_zscore

cols = df.columns # 获得数据框的列名
for col in cols: # 循环读取每列
    df_col = df[col] # 得到每列的值
    z_score = (df_col - df_col.mean()) / df_col.std() # 计算每列的Z-score得分
    df_zscore[col] = z_score.abs() > 2.2 # 判断Z-score得分是否大于2.2，如果是则是True，否则为False
print (df_zscore) # 打印输出

df[df_zscore] = None
print "df is: "
print df

# df.iloc[df_zscore] = np.nan # 此方法不行



# df[df_zscore == True] = None

# print "-----------"
# print df_zscore == True

# print df