# -*- coding: utf-8 -*-

"""

Statistical and Mathematical Functions with DataFrames in Apache Spark
https://databricks.com/blog/2015/06/02/statistical-and-mathematical-functions-with-dataframes-in-spark.html

"""

import os

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

spark = SparkSession\
        .builder\
        .appName("check country")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds = spark.read.jdbc(url=url,table="country_data_export")\
    .withColumn("MONTH", col("MONTH").cast("int"))
ds.printSchema()
# print(ds.count())

ds_COUNTRY = ds.select("COUNTRY").dropDuplicates()
print(ds_COUNTRY.count()) # 234

# 中国每月向各国出口金额，金额是亿元
ds1 = ds.groupBy("COUNTRY","TIME","YEAR","MONTH").agg({"USD": "sum", "RMB": "sum"})\
    .filter(col("COUNTRY") == "美国").orderBy(col("TIME").asc())\
    .withColumn("sum(RMB)",bround(col("sum(RMB)").cast("float") / 100000000.0, 3))\
    .withColumn("sum(USD)",bround(col("sum(USD)").cast("float") / 100000000.0, 3))
ds1.show(200)
ds1.printSchema()

# 中国每年向各国出口金额，金额是亿元
ds2 = ds.filter(col("MONTH") <= 5).groupBy("COUNTRY","YEAR").agg({"USD": "sum", "RMB": "sum"})\
    .orderBy(col("YEAR").asc())\
    .withColumn("sum(RMB)",bround(col("sum(RMB)").cast("float") / 100000000.0, 3))\
    .withColumn("sum(USD)",bround(col("sum(USD)").cast("float") / 100000000.0, 3))\
    .groupBy("COUNTRY").agg({"sum(RMB)":"stddev","sum(USD)":"stddev"})\
    .orderBy(col("stddev(sum(USD))").asc())
ds2.show(200)
ds2.printSchema()