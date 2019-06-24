# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:sqlserver://172.16.100.155;DatabaseName=SDSWT_Customs_New") \
    .option("dbtable", "B_DATA_201802_I") \
    .option("user", "sa") \
    .option("password", "Yiyun@3372") \
    .load()

ds1.show(10, truncate=False)