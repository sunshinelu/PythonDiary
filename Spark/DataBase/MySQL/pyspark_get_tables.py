# -*- coding: utf-8 -*-

"""
获取mysql数据库gogndan中所有表的名字

"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


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

list1 = list(ds1.rdd.map(lambda x:x.TABLE_NAME).collect())

print(list1)

for i in list1:
    l1 = str(i).split("_")[2]
    print(l1)
    print(str(l1[0:4]))
    print(str(l1[4:6]))

    # print(i + "_ana")