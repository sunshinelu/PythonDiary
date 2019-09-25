# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/25 上午11:10 
 @File    : streaming_na_filter.py
 @Note    : 
 
 """


# from pyspark.streaming.DStream import union
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import *
import pyspark.sql.functions as F
from datetime import datetime
import uuid
from functools import reduce
import sys
from pyspark.sql import window as w


spark = SparkSession\
    .builder\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0") \
    .appName("spark read and write kafka")\
    .getOrCreate()

brokers = "127.0.0.1:9092"
topic = "test"


inputDf = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .load()

col_name = ["identification_type","identification_id","email","mobile_phone","rand1"]
col_type = ["string","string","string","string","double"]

JsonDf = inputDf.selectExpr("CAST(value AS STRING)")

dataSchema = StructType()
for i,j in zip(col_name,col_type):
    dataSchema.add(i,j)

NestedDf = JsonDf.select(F.from_json("value", dataSchema).alias("Kafka_value"))

expr_col_1 = ["Kafka_value." +i for i in col_name]
FlattenedDf = NestedDf.selectExpr(expr_col_1)

"""
1. 缺失值处理
na_col:输入要处理的列名
na_mode:输入处理方式
    删除：drop
    保存：save
    填充：fill
    不做任何处理：donothing
na_fill：设置 na_col 中指定的列要填充的数据
"""
na_col = ["identification_id","email","mobile_phone"]
na_mode = "save" # drop or save or fill or donothing
na_fill = [0,"无","空"]

if (na_mode == "drop") & (len(na_col) >= 1):
    na_processedDf = FlattenedDf.na.drop(subset=na_col).withColumn("tag", F.lit("na drop"))
elif (na_mode == "save") & (len(na_col) >= 1):
    na_processedDf = FlattenedDf.where(reduce(lambda x, y: x | y, (F.col(x).isNull() for x in na_col)))\
        .withColumn("tag", F.lit("na save"))
elif (na_mode == "fill") & (len(na_col) >= 1):
    # na_processedDf = FlattenedDf.na.fill(na_fill, subset=na_col) # na_fill为固定值时用此方法
    fill_dic = dict(zip(na_col, na_fill))
    na_processedDf = FlattenedDf.na.fill(fill_dic)
else:
    na_processedDf = FlattenedDf.withColumn("tag", F.lit("na donothing"))


processedDf = na_processedDf


def uuid_func():
    return str(uuid.uuid4())
uuid_udf = F.udf(uuid_func,StringType())

# 将列拼接成json作为key传输出去
resDf = processedDf\
    .withColumn("jsonCol", F.to_json(F.struct([processedDf[x] for x in processedDf.columns])))\
    .withColumn("key", uuid_udf()) \
    .select("key", F.col("jsonCol").alias("value"))

kafkaOutput = resDf.writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", brokers)\
    .option("topic", "ages")\
    .outputMode("append") \
    .option("checkpointLocation", "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/kafka-tutorials/spark/checkpoints")\
    .start()

# outputMode: complete append update
query = resDf \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .option('truncate', 'false') \
    .start()

spark.streams.awaitAnyTermination()