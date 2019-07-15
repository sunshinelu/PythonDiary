# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午1:19 
 @File    : pyspark_read_csv_demo3.py
 @Note    : 
 
 """


import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StringType,ArrayType
import jieba

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

file_path = "/Users/sunlu/Documents/Case/天枢大数据平台V3.0/数据挖掘分析平台/数据挖掘平台所需demo数据/bigDataMiner_demodata/03分类模型测试数据/"
# file_name = "diabetes.csv"
# ds = spark.read.csv(file_path + file_name,header = True,encoding="UTF-8")
file_name = "abalone.data.txt"
cols = ["gender","length","diameter","height","total_weight","shelling_weight","visceral_weight","shell_weight","rings"]
ds = spark.read.csv(file_path + file_name,header = False,encoding="UTF-8").toDF(*cols)


splits = ds.randomSplit([0.7,0.3], 24)

url = "jdbc:mysql://10.20.5.49:3306/rgznpt_sjy?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

# print(splits[0].count())
# print(splits[1].count())

# splits[0].write.jdbc(url = url, table= "ml_classify_diabetes_train",mode="overwrite")
# splits[1].write.jdbc(url = url, table= "ml_classify_diabetes_test",mode="overwrite")
#

splits[0].write.jdbc(url = url, table= "ml_classify_abalone_train",mode="overwrite")
splits[1].write.jdbc(url = url, table= "ml_classify_abalone_test",mode="overwrite")