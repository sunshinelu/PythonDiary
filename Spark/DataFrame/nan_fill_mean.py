# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/10 下午1:24 
 @File    : nan_fill_mean.py
 @Note    : 
 
 """

"""
指定dataframe的列名，将含有空值的列替换成该列的均值

参考链接：
Replace missing values with mean - Spark Dataframe
https://stackoverflow.com/questions/40057563/replace-missing-values-with-mean-spark-dataframe/40059453

"""
import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

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

# df = df.withColumn("var2", F.col("var2").cast("float")).withColumn("var3", F.col("var3").cast("float"))

cols = ["var2","var3"]

# print(df.columns)
# print(spark.version())
"""
# 方法一 
imputer = Imputer(
    inputCols=cols,
    outputCols=["{}_imputed".format(c) for c in cols]
)

ds1 = imputer.fit(df).transform(df)

ds1.select(cols).show()
"""

#  方法二 √
## filter numeric cols
num_cols = [col_type[0] for col_type in filter(lambda dtype: dtype[1] in {"bigint", "double", "int"}, df.dtypes)]
print(num_cols)
### Compute a dict with <col_name, median_value>
median_dict = dict()
for c in num_cols:
   median_dict[c] = df.stat.approxQuantile(c, [0.5], 0.001)[0]
   print(df.stat.approxQuantile(c, [0.5], 0.001))

print(median_dict)
ds1 = df.na.fill(median_dict)
ds1.show()


# def fill_with_mean(df, exclude=set()):
#     stats = df.agg(*(
#         F.avg(c).alias(c) for c in cols if c not in exclude
#     ))
#     return df.na.fill(stats.first().asDict())
#
# ds1 = fill_with_mean(df, cols)
# ds1.select(cols).show()


spark.stop()