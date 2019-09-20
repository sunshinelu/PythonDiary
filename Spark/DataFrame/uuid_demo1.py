# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 下午2:04 
 @File    : uuid_demo1.py
 @Note    : 

 """


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import uuid
from pyspark.sql.types import StringType

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


def uuid_func():
    return str(uuid.uuid4())
uuid_udf = F.udf(uuid_func,StringType())

ds2 = ds1.withColumn("key", uuid_udf())
ds2.show(truncate=False)
ds2.printSchema()
