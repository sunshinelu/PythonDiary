# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/17 下午5:03 
 @File    : check_label_2.py
 @Note    : 
 
 """


import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

url = "jdbc:mysql://10.20.5.49:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"


table_name = "ztb_class_0716_train_copy"
ds = spark.read.jdbc(url=url,table=table_name)
print(ds.count())
print(ds.na.drop().count())
print(ds.filter(F.length("title") >=5).count())
