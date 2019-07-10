# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/10 下午4:09 
 @File    : get_dup_data.py
 @Note    : 
 
 """

"""
获取数据中国年的全部重复数据

参考链接：
PySpark - Get indices of duplicate rows
https://stackoverflow.com/questions/50865803/pyspark-get-indices-of-duplicate-rows
"""

import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce
from pyspark.ml.feature import Imputer
from pyspark.sql.window import Window

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

sc = spark.sparkContext

cols_1 = ["col1", "col2","col3","col4"]

rdd = sc.parallelize([
    (1, "a", "b", 3),
    (2, None, "f", None),
    (3, "g", "h", 4),
    (4, None, "f", None),
    (5, "a", "b", 3)])

df = spark.createDataFrame(rdd).toDF(* cols_1)


df.show()

cols_2 = ["col2","col3"]
df1 = df.join(
    df.groupBy(cols_2).agg((F.count("*")>1).cast("int").alias("e")),
    on=cols_2,
    how="inner"
).filter(F.col("e") >= 1).drop("e")

df1.show()

df2 = df.join(
    df.groupBy(cols_2).count(),
    on=cols_2,
    how="inner"
)#.filter(F.col("e") >= 1).drop("e")

df2.show()