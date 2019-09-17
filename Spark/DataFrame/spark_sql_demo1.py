# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/17 上午10:41 
 @File    : spark_sql_demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://10.20.5.114:3306/IngloryBDP?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "DA_SEED_201909") \
    .option("user", "root") \
    .option("password", "root") \
    .load()