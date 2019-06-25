# -*- coding: utf-8 -*-

"""
分组排序TopN问题

参考链接：
Spark SQL Row_number() PartitionBy Sort Desc
https://stackoverflow.com/questions/35247168/spark-sql-row-number-partitionby-sort-desc

How to use window functions in PySpark?
https://stackoverflow.com/questions/31857863/how-to-use-window-functions-in-pyspark

"""

import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit,col,row_number
from pyspark.sql.window import Window
from pyspark.sql.functions import asc

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("window fnction demo")\
        .getOrCreate()

import numpy as np
np.random.seed(1)

keys = ["foo"] * 10 + ["bar"] * 10
values = np.hstack([np.random.normal(0, 1, 10), np.random.normal(10, 1, 100)])

df = spark.createDataFrame([
   {"k": k, "v": round(float(v), 3)} for k, v in zip(keys, values)])

df.show()
"""
+---+------+
|  k|     v|
+---+------+
|foo| 1.624|
|foo|-0.612|
|foo|-0.528|
|foo|-1.073|
|foo| 0.865|
|foo|-2.302|
|foo| 1.745|
|foo|-0.761|
|foo| 0.319|
|foo|-0.249|
|bar|11.462|
|bar|  7.94|
|bar| 9.678|
|bar| 9.616|
|bar|11.134|
|bar|   8.9|
|bar| 9.828|
|bar| 9.122|
|bar|10.042|
|bar|10.583|
+---+------+
"""

w = Window.partitionBy("k").orderBy(col("v").asc())
df_1 = df.withColumn("rn", row_number().over(w)).where(col("rn") <= 5)#.drop("rn")
df_1.show()
"""
+---+------+---+
|  k|     v| rn|
+---+------+---+
|bar|  7.94|  1|
|bar|   8.9|  2|
|bar| 9.122|  3|
|bar| 9.616|  4|
|bar| 9.678|  5|
|foo|-2.302|  1|
|foo|-1.073|  2|
|foo|-0.761|  3|
|foo|-0.612|  4|
|foo|-0.528|  5|
+---+------+---+
"""

df3 = spark.range(10)

df3.show()