# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/16 下午3:40 
 @File    : read_kafka_demo1.py
 @Note    : 
 
 """


from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import *
import pyspark.sql.functions as F
from datetime import datetime


spark = SparkSession\
    .builder\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0") \
    .appName("spark read and write kafka")\
    .getOrCreate()

brokers = "127.0.0.1:9092"
topic = "test"

# inputDf = spark.readStream\
#     .format("kafka")\
#     .option("kafka.bootstrap.servers", brokers)\
#     .option("topic", topic)\
#     .load()

inputDf = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .load()

personJsonDf = inputDf.selectExpr("CAST(value AS STRING)")

struct = StructType()\
    .add("firstName", StringType())\
    .add("lastName", StringType())\
    .add("birthDate", StringType())

personNestedDf = personJsonDf.select(F.from_json("value", struct).alias("person"))

personFlattenedDf = personNestedDf.selectExpr("person.firstName", "person.lastName", "person.birthDate")

personDf = personFlattenedDf.withColumn("birthDate", F.to_timestamp("birthDate", "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))

def ageFunc(birthDate):
    endtime = datetime.now()
    age = (endtime - birthDate).days / 365.25
    return age

ageUdf = F.udf(ageFunc, IntegerType())

processedDf = personDf.withColumn("age", ageUdf("birthDate"))

resDf = processedDf.select(
      F.concat("firstName", F.lit(" "), "lastName").alias("key"),
      processedDf.age.cast(StringType()).alias("value"))

kafkaOutput = resDf.writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", brokers)\
    .option("topic", "ages")\
    .option("checkpointLocation", "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/kafka-tutorials/spark/checkpoints")\
    .start()

query = resDf \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

spark.streams.awaitAnyTermination()