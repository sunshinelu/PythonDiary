# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/10 下午4:09 
 @File    : get_dup_data.py
 @Note    : 
 
 """

"""
获取数据中的全部重复数据

参考链接：
PySpark - Get indices of duplicate rows
https://stackoverflow.com/questions/50865803/pyspark-get-indices-of-duplicate-rows
"""

import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce
from pyspark.ml.feature import Imputer
from pyspark.sql.window import Window
from pyspark.sql import window as w
import sys

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

sc = spark.sparkContext

cols_1 = ["col1", "col2","col3","col4"]

rdd = sc.parallelize([
    (1, "a", "b", 3),
    (2, None, "f", None),
    (3, "g", "h", 4),
    (4, None, "f", None),
    (5, "a", "b", 3)])

df = spark.createDataFrame(rdd).toDF(* cols_1)


df.show()
"""
+----+----+----+----+
|col1|col2|col3|col4|
+----+----+----+----+
|   1|   a|   b|   3|
|   2|null|   f|null|
|   3|   g|   h|   4|
|   4|null|   f|null|
|   5|   a|   b|   3|
+----+----+----+----+
"""

cols_2 = ["col2","col3"]
df1 = df.join(
    df.groupBy(cols_2).agg((F.count("*")>1).cast("int").alias("e")),
    on=cols_2,
    how="inner"
).filter(F.col("e") >= 1).drop("e")

df1.show()
"""
+----+----+----+----+
|col2|col3|col1|col4|
+----+----+----+----+
|   a|   b|   1|   3|
|   a|   b|   5|   3|
+----+----+----+----+
"""

df2 = df.join(
    df.groupBy(cols_2).count(),
    on=cols_2,
    how="inner"
)#.filter(F.col("e") >= 1).drop("e")

df2.show()
"""
+----+----+----+----+-----+
|col2|col3|col1|col4|count|
+----+----+----+----+-----+
|   g|   h|   3|   4|    1|
|   a|   b|   1|   3|    2|
|   a|   b|   5|   3|    2|
+----+----+----+----+-----+

"""

cols_3 = ["col2","col3"]
# windowSpec = w.Window.partitionBy(cols_3).rowsBetween(-sys.maxint, sys.maxint)
windowSpec = w.Window.partitionBy(cols_3).rowsBetween(-sys.maxsize, sys.maxsize)

# df.withColumn('e', f.when(f.count(f.col('d')).over(windowSpec) > 1, f.lit(1)).otherwise(f.lit(0))).show(truncate=False)

df3 = df.withColumn('e', (F.count('*').over(windowSpec) > 1).cast('int'))
df3.show(truncate=False)
"""
+----+----+----+----+---+
|col1|col2|col3|col4|e  |
+----+----+----+----+---+
|2   |null|f   |null|1  |
|4   |null|f   |null|1  |
|3   |g   |h   |4   |0  |
|1   |a   |b   |3   |1  |
|5   |a   |b   |3   |1  |
+----+----+----+----+---+
"""

df.show()
temp_df = df.groupBy(cols_3).count().filter(F.col("count") > 1).drop("count")
temp_df.show()

temp_df.join(df,cols_3,"left").show()