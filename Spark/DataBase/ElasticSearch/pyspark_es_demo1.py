# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/20 下午4:46 
 @File    : pyspark_es_demo1.py
 @Note    : 
 
 """

"""
参考链接：
1. pyspark访问Elasticsearch数据
https://blog.icocoro.me/2018/03/07/1803-pyspark-elasticsearch/

2. Spark SQL大数据处理并写入Elasticsearch
https://www.cnblogs.com/FG123/p/9748836.html

https://github.com/a342058040/Spark-for-Python
https://github.com/a342058040/Spark-for-Python/blob/master/spark_sql/spark_weather.py

将elasticsearch-spark-20_2.11-6.2.3.jar 放在$SPARK_HOME/jars目录下。
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import *

import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


spark = SparkSession\
        .builder\
        .appName("spark read and write es")\
        .getOrCreate()
# save data to elasticsearch
schema = StructType([
    StructField("id", StringType(), True),
    StructField("email", StringType(), True)
])

data = [('1', 'ss'), ('2', 'dd'), ('3', 'ff_update'), ('4', '哈哈哈')]
# data = [('10', 'ss'), ('20', 'dd'), ('30', 'ff_update'), ('40', '哈哈哈')]

save_df = spark.createDataFrame(data, ['id', 'uname'])
save_df.show(truncate=False)

save_df.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "127.0.0.1") \
    .option("es.resource", "pyspark_es/data2") \
    .option("es.mapping.id", "id") \
    .mode('append') \
    .save()

# read data from elasticsearch
df = spark.read \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "127.0.0.1") \
    .option("es.resource", "pyspark_es/data2") \
    .load()

df.show(truncate=False)

spark.stop()