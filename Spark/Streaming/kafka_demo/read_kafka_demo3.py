# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/18 上午11:29 
 @File    : read_kafka_demo3.py
 @Note    : 
 对数据进行处理后，将结果保存成json然后以key的形式发出，传输给Kafka。
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


inputDf = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .load()
# print("inputDf schema is:")
# inputDf.printSchema()

personJsonDf = inputDf.selectExpr("CAST(value AS STRING)")
# print("personJsonDf schema is:")
# personJsonDf.printSchema()

struct = StructType()\
    .add("firstName", StringType())\
    .add("lastName", StringType())\
    .add("birthDate", StringType())

personNestedDf = personJsonDf.select(F.from_json("value", struct).alias("person"))
# print("personNestedDf schema is:")
# personNestedDf.printSchema()

personFlattenedDf = personNestedDf.selectExpr("person.firstName", "person.lastName", "person.birthDate")
# print("personFlattenedDf schema is:")
# personFlattenedDf.printSchema()

personDf = personFlattenedDf.withColumn("birthDate", F.to_timestamp("birthDate", "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))

processedDf = personDf.withColumn('date',F.current_timestamp())\
    .withColumn("age", F.months_between("date","birthDate")/ F.lit(12))\
    .withColumn("age",F.col("age").cast("int")).drop(* ["date"])

# 将列拼接成json作为key传输出去
resDf = processedDf.withColumn("jsonCol", F.to_json(F.struct([processedDf[x] for x in processedDf.columns])))\
    .select(
      F.concat("firstName", F.lit(" "), "lastName").alias("key"),
      F.col("jsonCol").alias("value"))

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