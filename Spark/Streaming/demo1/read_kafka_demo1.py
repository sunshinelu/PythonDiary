# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/16 下午3:40 
 @File    : read_kafka_demo1.py
 @Note    : 

 # 启动Kafka
./zookeeper-server-start.sh ../config/zookeeper.properties
./kafka-server-start.sh ../config/server.properties

# 创建topic
./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

# 查看topic
./kafka-topics.sh --list --zookeeper localhost:2181

# 发送消息
./kafka-console-producer.sh --broker-list localhost:9092 --topic test

输入消息：
{"firstName":"Quentin","lastName":"Corkery","birthDate":"1984-10-26T03:52:14.449+0000"}
{"firstName":"Lysanne","lastName":"Beer","birthDate":"1997-10-22T04:09:35.696+0000"}
{"firstName":"Neil","lastName":"Macejkovic","birthDate":"1971-08-06T18:03:11.533+0000"}

# 消费消息
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning

# 消费spark生成的消息
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic ages --from-beginning


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
print("inputDf schema is:")
inputDf.printSchema()

personJsonDf = inputDf.selectExpr("CAST(value AS STRING)")
print("personJsonDf schema is:")
personJsonDf.printSchema()

struct = StructType()\
    .add("firstName", StringType())\
    .add("lastName", StringType())\
    .add("birthDate", StringType())

personNestedDf = personJsonDf.select(F.from_json("value", struct).alias("person"))
print("personNestedDf schema is:")
personNestedDf.printSchema()

personFlattenedDf = personNestedDf.selectExpr("person.firstName", "person.lastName", "person.birthDate")
print("personFlattenedDf schema is:")
personFlattenedDf.printSchema()

personDf = personFlattenedDf.withColumn("birthDate", F.to_timestamp("birthDate", "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))

"""
# 此方法计算年龄不对
def ageFunc(birthDate):
    endtime = datetime.now()
    age = (endtime - birthDate).days / 365.25
    return age

ageUdf = F.udf(ageFunc, IntegerType())

processedDf = personDf.withColumn("age", ageUdf("birthDate"))
"""
processedDf = personDf.withColumn('date',F.current_timestamp())\
    .withColumn("age", F.months_between("date","birthDate")/ F.lit(12))\
    .withColumn("age",F.col("age").cast("int")).drop(* ["date"])

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