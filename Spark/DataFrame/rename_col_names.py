# -*- coding: utf-8 -*-


import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("similarity of short text")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "rc_jbxx") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

col_1 = ["address"]
col_2 = ["text", "label"]
col_3 = list(["text", "label"])
# col_4 = list("text", "label") # 这个不可用

col_5 = "text,label".split(",")

ds2 = ds1.select(col_1)\
    .dropna().dropDuplicates()\
    .withColumn("tag", lit("address")).toDF(* col_5)

ds2.printSchema()

