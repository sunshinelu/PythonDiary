# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午2:55 
 @File    : random_split_2.py
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

url = "jdbc:mysql://10.20.5.49:3306/rgznpt_sjy?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

table_name = "nlp_sogou_classification_mini"
ds = spark.read.jdbc(url=url,table=table_name).filter(F.length("txt") >= 10)

ds.select("label").distinct().show()

splits = ds.randomSplit([0.7,0.3], 24)

splits[0].write.jdbc(url = url, table= "nlp_sogou_train",mode="append")
splits[1].write.jdbc(url = url, table= "nlp_sogou_test",mode="append")



