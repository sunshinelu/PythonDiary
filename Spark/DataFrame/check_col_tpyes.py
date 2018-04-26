#-*- coding: UTF-8 -*-

from pyspark import SparkContext
from pyspark import SparkConf
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession
from pyspark.sql.types import *


import os
import sys

# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '/Users/sunlu/Software/spark-2.0.2-bin-hadoop2.6'
 # Create a variable for our root path
SPARK_HOME = os.environ['SPARK_HOME']


master= "local"
spark = SparkSession.builder\
    .appName("check_col_type")\
    .master(master)\
    .getOrCreate()

sc = spark.sparkContext

# Generate comma delimited data
stringCSVRDD = sc.parallelize([
    (123, 'Katie', 19, 'brown'),
    (234, 'Michael', 22, 'green'),
    (345, 'Simone', 23, 'blue')
])

# Specify schema
schema = StructType([
    StructField("id", LongType(), True),
    StructField("name", StringType(), True),
    StructField("age", LongType(), True),
    StructField("eyeColor", StringType(), True)
   ])

"""
_acceptable_types = {
    BooleanType: (bool,),
    ByteType: (int, long),
    ShortType: (int, long),
    IntegerType: (int, long),
    LongType: (int, long),
    FloatType: (float,),
    DoubleType: (float,),
    DecimalType: (decimal.Decimal,),
    StringType: (str, unicode),
    BinaryType: (bytearray,),
    DateType: (datetime.date, datetime.datetime),
    TimestampType: (datetime.datetime,),
    ArrayType: (list, tuple, array),
    MapType: (dict,),
    StructType: (tuple, list, dict),
}
"""
# Apply the schema to the RDD and Create DataFrame
swimmers = spark.createDataFrame(stringCSVRDD, schema)

sc.stop()
spark.stop()