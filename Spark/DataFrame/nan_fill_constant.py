# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/20 下午3:21 
 @File    : nan_fill_constant.py
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



fill_col = ["identification_id","email","mobile_phone"]
fill_value = [0,"无","空"]
fill_dic = dict(zip(fill_col,fill_value))
print(type(fill_dic))
print(fill_dic)

# ds1.na.drop().show(truncate=False)

ds2 = ds1.na.fill(fill_dic)
ds2.show(truncate=False)

