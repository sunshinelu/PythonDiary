# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 下午1:18 
 @File    : read_kafka_demo4.py
 @Note    : 
 读取Kafka数据，对数据进行缺失值处理
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

"""
dataSchema = StructType()
for i in range(len(col_name)):
    dataSchema.add(col_name[i],col_type[i])
"""
dataSchema = StructType()
for i,j in zip(col_name,col_type):
    dataSchema.add(i,j)

NestedDf = JsonDf.select(F.from_json("value", dataSchema).alias("Kafka_value"))

expr_col_1 = ["Kafka_value." +i for i in col_name]
FlattenedDf = NestedDf.selectExpr(expr_col_1)

"""
1. 缺失值处理
删除：drop
保存：save
填充：fill
不做任何处理：donothing
"""
na_col = ["identification_id","email","mobile_phone"]
na_mode = "drop" # drop or save or fill or donothing
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
else: na_processedDf = FlattenedDf.withColumn("tag", F.lit("na donothing"))


"""
2. 重复数据处理处理
删除：drop
不做任何处理：donothing
"""

dup_col = ["identification_id","email"]
dup_mode = "drop" # drop or save or donothing

if (dup_mode == "drop") & (len(dup_col) >= 1):
    dup_processedDf = FlattenedDf.dropDuplicates(subset=dup_col)\
        .withColumn("tag", F.lit("dup drop"))
# elif (dup_mode == "save") & (len(dup_col) >= 1):

    # 方法四：不通过
    # temp_df = FlattenedDf.groupBy(dup_col).count().filter(F.col("count") > 1).drop("count")
    # dup_processedDf = temp_df.join(FlattenedDf)

    # 方法三：不通过
    # windowSpec = w.Window.partitionBy(dup_col).rowsBetween(-sys.maxsize, sys.maxsize)
    # dup_processedDf = FlattenedDf.withColumn('DM_dup_tag', (F.count('*').over(windowSpec) > 1).cast('int'))\
    #     .filter(F.col("DM_dup_tag") >= 1).drop("DM_dup_tag").withColumn("tag", F.lit("dup save"))

    # 方法二：不通过
    # dup_processedDf = FlattenedDf.join(FlattenedDf.dropDuplicates(subset=dup_col),FlattenedDf.columns,"left_anti")\
    #     .withColumn("tag", F.lit("dup save"))

    # 方法一：不通过
    # dup_processedDf = FlattenedDf.join(
    #     FlattenedDf.groupBy(dup_col).agg((F.count("*") > 1).cast("int").alias("DM_dup_tag")),
    #     on=dup_col,
    #     how="inner"
    # ).filter(F.col("DM_dup_tag") >= 1).drop("DM_dup_tag").withColumn("tag", F.lit("dup save"))
else: dup_processedDf = FlattenedDf.withColumn("tag", F.lit("dup donothing"))



processedDf = na_processedDf.union(dup_processedDf)
# processedDf = na_processedDf
# processedDf = dup_processedDf

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