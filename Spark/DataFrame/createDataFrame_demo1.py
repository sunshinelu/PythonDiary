# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/17 下午3:16 
 @File    : createDataFrame_demo1.py
 @Note    : 
 
 """


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce
from pyspark.ml.feature import Imputer
from pyspark.sql.window import Window

spark = SparkSession\
        .builder\
        .appName("creat data frame")\
        .getOrCreate()

sc = spark.sparkContext

cols_1 = ["firstName", "lastName","birthDate"]



rdd = sc.parallelize([
    ("Quentin","Corkery", "1984-10-26T03:52:14.449+0000"),
    ("Lysanne","Beer","1997-10-22T04:09:35.696+0000"),
    ("Neil","Macejkovic","1971-08-06T18:03:11.533+0000")])

df = spark.createDataFrame(rdd).toDF(* cols_1)

df.show(truncate=False)

df_1 = df.withColumn("birthDate", F.to_timestamp("birthDate", "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))

df_1.show(truncate=False)

df_1.printSchema()

df_2 = df_1.withColumn('date',F.current_timestamp())

df_2.show(truncate=False)
df_2.printSchema()

df_3 = df_2.withColumn("year", F.months_between("date","birthDate")/ F.lit(12))\
    .withColumn("year",F.col("year").cast("int")).drop(* ["date"])

df_3.show(truncate=False)
df_3.printSchema()

# 将dataframe 转成josn
df_4 = df_3.withColumn("jsonCol", F.to_json(F.struct([F.when(F.col(x)!="  ",df_3[x]).otherwise(None).alias(x) for x in df_3.columns])))
df_4.show(truncate=False)
df_4.printSchema()
"""
+---------+----------+-------------------+----+--------------------------------------------+
|firstName|lastName  |birthDate          |year|jsonCol                                     |
+---------+----------+-------------------+----+--------------------------------------------+
|Quentin  |Corkery   |1984-10-26 11:52:14|34  |{"firstName":"Quentin","lastName":"Corkery"}|
|Lysanne  |Beer      |1997-10-22 12:09:35|21  |{"firstName":"Lysanne","lastName":"Beer"}   |
|Neil     |Macejkovic|1971-08-07 02:03:11|48  |{"firstName":"Neil","lastName":"Macejkovic"}|
+---------+----------+-------------------+----+--------------------------------------------+
"""


# 将dataframe 转成josn
df_3.withColumn("jsonCol", F.to_json(F.struct([df_3[x] for x in df_3.columns]))).show(truncate=False)
"""
+---------+----------+-------------------+----+--------------------------------------------------------------------------------------------------+
|firstName|lastName  |birthDate          |year|jsonCol                                                                                           |
+---------+----------+-------------------+----+--------------------------------------------------------------------------------------------------+
|Quentin  |Corkery   |1984-10-26 11:52:14|34  |{"firstName":"Quentin","lastName":"Corkery","birthDate":"1984-10-26T11:52:14.000+08:00","year":34}|
|Lysanne  |Beer      |1997-10-22 12:09:35|21  |{"firstName":"Lysanne","lastName":"Beer","birthDate":"1997-10-22T12:09:35.000+08:00","year":21}   |
|Neil     |Macejkovic|1971-08-07 02:03:11|48  |{"firstName":"Neil","lastName":"Macejkovic","birthDate":"1971-08-07T02:03:11.000+08:00","year":48}|
+---------+----------+-------------------+----+--------------------------------------------------------------------------------------------------+

"""

# 将dataframe 转成josn
df_3.withColumn("jsonCol", F.to_json(F.struct([ F.when(F.col(x)!="  ",df_3[x]).otherwise(None) for x in df_3.columns]))).show(truncate=False)
"""
+---------+----------+-------------------+----+-----------------------------------+
|firstName|lastName  |birthDate          |year|jsonCol                            |
+---------+----------+-------------------+----+-----------------------------------+
|Quentin  |Corkery   |1984-10-26 11:52:14|34  |{"col1":"Quentin","col2":"Corkery"}|
|Lysanne  |Beer      |1997-10-22 12:09:35|21  |{"col1":"Lysanne","col2":"Beer"}   |
|Neil     |Macejkovic|1971-08-07 02:03:11|48  |{"col1":"Neil","col2":"Macejkovic"}|
+---------+----------+-------------------+----+-----------------------------------+
"""