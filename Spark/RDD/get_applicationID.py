# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/26 上午9:21 
 @File    : get_applicationID.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()
sc = spark.sparkContext

print(sc.applicationId)
# local-1566783479708

print(sc.uiWebUrl)
# http://192.168.52.1:4040


sc.stop()
spark.stop()