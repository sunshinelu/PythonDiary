# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/10 下午1:52 
 @File    : spark_streaming_demo_2.py
 @Note    : 
 
 """



from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split,length
import pyspark.sql.functions as F
from pyspark.sql.types import *

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()
sc = spark.sparkContext
# 获取任务ID
app_id = sc.applicationId

colName_list = ["name","age","score","col1","time"]
type_list = ["string","integer","float","double","timestamp"]
dataSchema = StructType()#.add("name", "string").add("age", "integer")

for i in range(len(colName_list)):
    dataSchema.add(colName_list[i],type_list[i])

print(dataSchema)

dataSchema2 = StructType()

for i,j in zip(colName_list,type_list):
    dataSchema2.add(i,j)

print(dataSchema2)

print(dataSchema == dataSchema2)