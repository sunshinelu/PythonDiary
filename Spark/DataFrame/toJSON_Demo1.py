# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 上午9:58 
 @File    : toJSON_Demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *


spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "sjycl_test_data_1") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

ds1.show(truncate=False)
ds1.printSchema()


ds1.select(F.expr('length(identification_id)')).show()
"""
+-------------------------+
|length(identification_id)|
+-------------------------+
|                       18|
|                       18|
|                       18|
|                        0|
|                       18|
|                       18|
+-------------------------+
"""

na_col = ["identification_id","email","mobile_phone"]

ds2 = ds1.na.drop(subset=na_col)
ds2.show(truncate=False)
ds2.printSchema()

# ds1.filter(F.isnull(na_col)).show(truncate=False)
sc = spark.sparkContext
col_name = ["identification_type","identification_id","email","mobile_phone","rand1"]
col_type = ["string","string","string","string","double"]
dataSchema = StructType()
for i,j in zip(col_name,col_type):
    dataSchema.add(i,j)

ds2 = spark.createDataFrame(sc.emptyRDD(), dataSchema)
# ds2 = spark.emptyDataFrame()

for i in na_col:
    ds2 = ds2.union(ds1.filter(F.isnull(i)))

ds2.show(truncate=False)

# file_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/json_file"
# ds1.toJSON().saveAsTextFile(file_path)

"""
brokers = "127.0.0.1:9092"
ds1.writeStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", brokers)\
    .option("topic", "ages")\
    .option("checkpointLocation", "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/kafka-tutorials/spark/checkpoints")\
    .start()

"""