# -*- coding: utf-8 -*-

"""
groupby agg之后拼接字符串

* groupby操作demo
  * 1. Spark Dataframe groupBy with sequence as keys arguments（输入一个sequence进行分组groupby操作）
  * 参考链接：
  * https://stackoverflow.com/questions/37524510/spark-dataframe-groupby-with-sequence-as-keys-arguments
  * https://stackoverflow.com/questions/33882894/spark-sql-apply-aggregate-functions-to-a-list-of-column
  *
  * 2. groupby agg之后拼接字符串
  * 参考链接：
  * https://community.hortonworks.com/questions/44886/dataframe-groupby-and-concat-non-empty-strings.html
  * https://stackoverflow.com/questions/31450846/concatenate-columns-in-apache-spark-dataframe
  *

"""
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import lit,col,row_number,concat_ws,collect_list,explode,split
from pyspark.sql.window import Window
from pyspark.sql.functions import asc

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

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

df = df.withColumn("v", col("v").cast("string"))

df.printSchema()
df.show()

df2 = df.groupBy("k").agg(concat_ws("$",collect_list(col("v"))).alias("v2"))
df2.show(truncate= False)

df3 = df.join(df2, "k", "left").withColumn("single", explode(split(col("v2"), "\$"))).filter(col("k") != col("single"))
df3.printSchema()
df3.show()