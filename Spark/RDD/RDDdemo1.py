#-*- coding: UTF-8 -*-

from pyspark import SparkContext
from pyspark import SparkConf
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession

master= "local"
spark = SparkSession.builder\
    .appName("RDDdemo1")\
    .master(master)\
    .getOrCreate()

sc = spark.sparkContext

x = sc.parallelize([("a", 1), ("b", 4),("c", 3),("d", 2)])
sorted(x.collect())
df1 = spark.createDataFrame(x).toDF("col1","col2")
df1.show()