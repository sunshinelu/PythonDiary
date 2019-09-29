# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 下午3:42 
 @File    : creat_empty_df_demo1.py
 @Note    :
 参考链接：
 https://blog.csdn.net/dkl12/article/details/81747908
 https://blog.csdn.net/dkl12/article/details/81747908
 """


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *
from functools import reduce

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

sc = spark.sparkContext



col_name = ["identification_type","identification_id","email","mobile_phone","rand1"]
col_type = ["string","string","string","string","double"]

dataSchema = StructType()
for i,j in zip(col_name,col_type):
    dataSchema.add(i,j)

ds2 = spark.createDataFrame(sc.emptyRDD(), dataSchema)
# ds2 = spark.emptyDataFrame()

na_col = ["identification_id","email","mobile_phone"]
for i in na_col:
    ds2 = ds2.union(ds1.filter(F.isnull(i)))

ds2.show(truncate=False)

print(ds1.schema == dataSchema)

nan_data = ds2.where(reduce(lambda x, y: x | y, (F.col(x).isNull() for x in na_col)))
nan_data.show(truncate=False)

print(reduce(lambda x, y: x | y, (F.col(x).isNull() for x in na_col)))
# Column<b'(((identification_id IS NULL) OR (email IS NULL)) OR (mobile_phone IS NULL))'>


ds1.filter(reduce(lambda x,y: x | y, (F.col(x).isNull() for x in na_col))).show(truncate=False)
