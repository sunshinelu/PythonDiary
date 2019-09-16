# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/16 下午4:33 
 @File    : read_kafka_demo2.py
 @Note    : 

 参考链接：
 1. PySpark Structured Streaming kafka示例
 https://blog.csdn.net/qq_33689414/article/details/86469267
 """

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType

if __name__ == '__main__':
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0") \
        .appName("pyspark_structured_streaming_kafka") \
        .getOrCreate()

    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .load()

    words = df.selectExpr("CAST(value AS STRING)")

    schema = StructType() \
        .add("name", StringType()) \
        .add("age", StringType()) \
        .add("sex", StringType())

    # 通过from_json，定义schema来解析json
    res = words.select(from_json("value", schema).alias("data")).select("data.*")

    query = res.writeStream \
        .format("console") \
        .outputMode("append") \
        .start()

    query.awaitTermination()
