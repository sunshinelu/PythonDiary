# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/9 下午6:53 
 @File    : spark_streaming_demo_1.py
 @Note    : 

 在终端中输入：
 nc -lk 9999
apache spark
apache hadoop


 """


from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split,length
import pyspark.sql.functions as F

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()
sc = spark.sparkContext
# 获取任务ID
app_id = sc.applicationId

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()\
    .filter(F.col("count") >= 5)\
    .filter(F.col("word").contains("spark"))

 # Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()