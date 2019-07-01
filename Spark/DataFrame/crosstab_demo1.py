# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

import os
# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("merge data")\
        .getOrCreate()

# 交叉列表
# Create a DataFrame with two columns (name, item)
names = ["Alice", "Bob", "Mike"]
items = ["milk", "bread", "butter", "apples", "oranges"]
df = spark.createDataFrame([(names[i % 3], items[i % 5]) for i in range(100)], ["name", "item"])
df.show()

df.stat.crosstab("name", "item").show()
# +---------+------+-----+------+----+-------+
# |name_item|apples|bread|butter|milk|oranges|
# +---------+------+-----+------+----+-------+
# |      Bob|     6|    7|     7|   6|      7|
# |     Mike|     7|    6|     7|   7|      6|
# |    Alice|     7|    7|     6|   7|      7|
# +---------+------+-----+------+----+-------+
