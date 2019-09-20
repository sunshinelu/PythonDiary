# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 上午10:13 
 @File    : read_ES_Demo1.py
 @Note    :


读取人才事业部ES中数据，但是人才事业部使用的ES版本为5.4.2，因此需要新增config
.config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-20_2.11:5.4.2")

参考链接：
1. spark读取elasticsearch中数组类型的字段
 https://blog.csdn.net/piduzi/article/details/81407434?utm_source=blogxgwz8
 """

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import *

import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


spark = SparkSession\
    .builder \
    .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-20_2.11:5.4.2")\
    .appName("spark read and write es")\
    .getOrCreate()

#
# read data from elasticsearch
df = spark.read \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "10.20.5.140") \
    .option("es.read.field.as.array.include","Authora,keywords,classNumber,authors") \
    .option("es.resource", "lunwen-cn/cnki") \
    .load().first()

print(df)

# print(df.count()) # 12432590

# df.show(5, truncate=False)
# df.printSchema()
"""

root
 |-- Authora: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- abstracts: string (nullable = true)
 |-- authors: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- classNumber: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- journal: string (nullable = true)
 |-- keywords: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- publishTime: string (nullable = true)
 |-- publishYear: long (nullable = true)
 |-- publisher: string (nullable = true)
 |-- qkid: long (nullable = true)
 |-- rowkey: string (nullable = true)
 |-- term: struct (nullable = true)
 |    |-- authors: string (nullable = true)
 |-- title: string (nullable = true)
 |-- url: string (nullable = true)


"""