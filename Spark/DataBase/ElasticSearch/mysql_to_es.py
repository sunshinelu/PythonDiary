# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/23 下午2:12 
 @File    : mysql_to_es.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()


ds1 = spark.read.jdbc(url="jdbc:mysql://localhost:3306/data_mining_db?user=root&password=root",
                      table="ml_info_item",
                      properties={"driver": 'com.mysql.jdbc.Driver'})

ds1.write \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "127.0.0.1") \
    .option("es.resource", "data_mining_db/ml_info_item") \
    .mode('append') \
    .save()