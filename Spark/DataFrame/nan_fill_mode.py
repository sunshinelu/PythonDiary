# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/10 下午2:28 
 @File    : nan_fill_mode.py
 @Note    : 
 
 """


import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用
os.environ["PYSPARK_PYTHON"] = "/Users/sunlu/anaconda3/bin/python"  # 在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce
from pyspark.ml.feature import Imputer

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()


df = spark.read.jdbc(url="jdbc:mysql://localhost:3306/data_mining_db?user=root&password=root",
                      table="ck_test0",
                      properties={"driver": 'com.mysql.jdbc.Driver'})

df.show()

df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "Industry") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()

# df = df.withColumn("var2", F.col("var2").cast("float")).withColumn("var3", F.col("var3").cast("float"))

cols = ["var1","var2"]



# mode_dict = dict()
# for c in cols:
#     mode_dict[c] = df.stat.approxQuantile(c, [0.5], 0.001)[0]
#    print(df.stat.approxQuantile(c, [0.5], 0.001))


