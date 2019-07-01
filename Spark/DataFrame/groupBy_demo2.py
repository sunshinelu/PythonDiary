# -*- coding: utf-8 -*-

"""
读取本地csv文件，并将结果保存到mysql中。

"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql import Window
from pyspark.sql.types import StringType

import os
# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"
spark = SparkSession\
        .builder\
        .appName("groupby demo")\
        .getOrCreate()

"""
path_import = "/Users/sunlu/Downloads/rc_jbxx.csv"
ds1 = spark.read.csv(path_import,header=True,encoding="UTF-8")
# ds1.show()


# Saving data to a JDBC source
ds1.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "test_rc_jbxx") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()
"""

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds = spark.read.jdbc(url=url,table="test_rc_jbxx")

# ds.select("identification_type").dropDuplicates().show(truncate=False)
# ds.select("nation").dropDuplicates().show(truncate=False)

# print(ds.count()) # 1256
# print(ds.drop("id","source").dropDuplicates().count()) # 1005

w = Window.partitionBy('rc_id')

def split_col(col, n):
    try:
        result = str(col).replace("\'", "").replace("(", "").replace(")", "").split(", ")[n]
        return result
    except IndexError:
        return None

split_col_udf = udf(split_col,StringType())

ds_1 = ds.select("nation").drop_duplicates()\
    .withColumn("nation_name",split_col_udf(col("nation"),lit(0)))\
    .withColumn("rn",split_col_udf(col("nation"),lit(1))).dropna()
ds_1.show(truncate = False)

