# -*- coding: utf-8 -*-

"""
参考链接：
python – 在Pyspark中具有最大值的GroupBy列和过滤器行
https://codeday.me/bug/20190307/724332.html

"""
import os

from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.window import Window

from pyspark.sql import Window

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("window fnction demo")\
        .getOrCreate()

data = [
    ('a', 5),
    ('a', 8),
    ('a', 7),
    ('b', 1),
    ('b', 3)
]

df = spark.createDataFrame(data, ["A", "B"])
df.show()

# Window function
w = Window.partitionBy('A')
df.withColumn('maxB', f.max('B').over(w)).show()
    # .where(f.col('B') == f.col('maxB'))\
    # .show()

# sql method
df.registerTempTable('table')
q = "SELECT A, B FROM (SELECT *, MAX(B) OVER (PARTITION BY A) AS maxB FROM table) M WHERE B = maxB"
spark.sql(q).show()