# -*- coding: utf-8 -*-

import pandas as pd
import pymysql
import numpy as np


"""
    @ 缺失值处理：
    @ 方法：删除、不处理、插补[均值]、插补[中位数]、插补[众数]、插补[固定值]、插补[回归方法]
    """

def dele_data(self):

    # 过滤缺失数据
    drop_data = self.dropna()
    return drop_data

def donothing(self):

    # 插补[不处理]
    return self

def mean_data(self):

    # 插补均值
    # col_median = self.iloc[0:len(self)]
    # fill_mean = self.fillna(col_median.mean())
    fill_mean = self.fillna(self.mean())

    return fill_mean

def median_data(self):

    # 插补[中位数]
    # col_median = self.iloc[0:len(self)]
    # fill_median = self.fillna(col_median.median())
    fill_median = self.fillna(self.median())
    return fill_median

def mode_data(self):

    # 插补[众数]
    # col_mode = self.iloc[0:len(self)]
    # fill_mode = self.fillna(col_mode.median())
    fill_mode = self.fillna(self.median())
    return fill_mode

def fill_constant(self,constant):

    # 插固定值
    fill_value = self.fillna(constant)
    return fill_value


## 加上字符集参数，防止中文乱码
db = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="data_mining_DB",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)

temp_table = "data_statistics"
# sql语句
sqlcmd = "select * from %s" % (temp_table)

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, db)

na_drop_df = dele_data(df)

print na_drop_df
print "========================"

na_mead_df = mean_data(df)

print na_mead_df

print "========================"
na_median_df = median_data(df)

print na_median_df

print "========================"

na_mode_df = mode_data(df)

print na_mode_df

print "========================"

print df.mean()
print "****************"
print df.median()
print "****************"
print df.mode()
print "****************"
