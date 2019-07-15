# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午5:10 
 @File    : pyspark_read_csv_demo4.py
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

file_path = "/Users/sunlu/Downloads/ztb_titlt_csv/*"

ds = spark.read.csv(file_path,header = False,encoding="UTF-8")#.select("id","url","title","label")
# ds = spark.read.csv(file_path,header = True,encoding="utf8mb4")
# print(ds.count())

ds.show(truncate=False)


url = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
# url = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=utf8mb4&user=root&password=root"

ds.write.jdbc(url = url, table= "ylzx_title_label",mode="overwrite")