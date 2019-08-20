# -*- coding: utf-8 -*-

"""
获取mysql数据库gogndan中所有表的名字

参考链接：
1. How to list all tables in database using Spark SQL?
https://stackoverflow.com/questions/42880119/how-to-list-all-tables-in-database-using-spark-sql?rq=1

2. Extract column values of Dataframe as List in Apache Spark
https://stackoverflow.com/questions/32000646/extract-column-values-of-dataframe-as-list-in-apache-spark
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


spark = SparkSession\
        .builder\
        .appName("get tables in mysql database gongdan")\
        .getOrCreate()

ds = spark.read.format('jdbc'). \
     options(
         url='jdbc:mysql://localhost:3306/', # database url (local, remote)
         dbtable='information_schema.tables',
         user='root',
         password='root',
         driver='com.mysql.jdbc.Driver').\
         load().\
         filter("table_schema = 'gongdan'")

ds1 = ds.select("TABLE_NAME").filter(col("TABLE_NAME").startswith("b_data_"))
ds1.show()
# ds1.printSchema

ds.dropna()

list1 = list(ds1.rdd.map(lambda x:x.TABLE_NAME).collect())

print(list1)

for i in list1:
    l1 = str(i).split("_")[2]
    print(l1)
    print(str(l1[0:4]))
    print(str(l1[4:6]))

    # print(i + "_ana")

spark.stop()