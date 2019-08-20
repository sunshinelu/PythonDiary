# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/20 下午2:55 
 @File    : pyspark_read_folder_demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


spark = SparkSession\
        .builder\
        .appName("read folder")\
        .getOrCreate()

sc = spark.sparkContext

file_path = "/Users/sunlu/Documents/数据集/ChnSentiCorp情感分析酒店评论/*/*"

rdd = sc.wholeTextFiles(file_path)


df = rdd.map(lambda x: (x[0].split("/")[6],x[1].strip().replace(" ","").replace("\r","").replace("\n",""))).toDF(["lable","txt"])


splits = df.randomSplit([0.7, 0.3], 24)
train = splits[0]
test = splits[1]


url = "jdbc:mysql://10.20.5.49:3306/rgznpt_sjy?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

train.write.jdbc(url = url, table= "nlp_HotelReviews_train",mode="overwrite")
test.write.jdbc(url = url, table= "nlp_HotelReviews_test",mode="overwrite")