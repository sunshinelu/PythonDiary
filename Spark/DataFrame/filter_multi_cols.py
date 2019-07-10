# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/10 上午11:50 
 @File    : filter_multi_cols.py
 @Note    : 
 
 """
"""
对多列同一条件进行过滤

参考链接：
pyspark dataframe filtering on multiple columns

https://stackoverflow.com/questions/47339105/pyspark-dataframe-filtering-on-multiple-columns?rq=1

"""

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()


ds1 = spark.read.jdbc(url="jdbc:mysql://localhost:3306/data_mining_db?user=root&password=root",
                      table="ml_info_item",
                      properties={"driver": 'com.mysql.jdbc.Driver'})

cols = ["COL_NAME","IF_AUTHORITY"]

# 方法一 √
ds2 = ds1
for x in cols:
    ds2 = ds2.filter(F.col(x).isNotNull())

ds2.select(cols).show(truncate=False)

# ds1.filter(F.col(*cols).isNotNull()).select(cols).show(truncate=False)

# 方法二 √
ds1.where(reduce(lambda x, y: x & y,  (F.col(x).isNotNull() for x in cols)))\
    .select(cols).show(truncate=False)

