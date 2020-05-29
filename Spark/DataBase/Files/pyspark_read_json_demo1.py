# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/10/9 下午4:09 
 @File    : pyspark_read_json_demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
from pyspark.sql.functions import *



spark = SparkSession\
        .builder\
        .appName("read json")\
        .getOrCreate()

sc = spark.sparkContext

file_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/Spider/*.json"
ds1 = spark.read.json(file_path)
ds1.printSchema()
ds1.show(truncate=False)
print(ds1.count())