# -*- coding: utf-8 -*-

"""
链接sql server数据库

方法一：（亲测可用）
将sqljdbc4-4.0.jar放到C:\Program Files\Java\jdk1.8.0_131\jre\lib\ext路径中

方法二：（未测试）
spark = SparkSession \
.builder \
.appName("Python Spark SQL basic example") \
.config("spark.driver.extraClassPath","/Users/Desktop/drivers/sqljdbc42.jar") \
.getOrCreate()

参考链接：
pyspark to read data from sql server
https://stackoverflow.com/questions/43946157/pyspark-to-read-data-from-sql-server
"""
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