#-*- coding: UTF-8 -*-

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from pyspark.sql.functions import split, explode,col

import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
python WordCountDemo_DF提交任务的时候报错，"ImportError: No module named pyspark.sql"为什么出现这个原因不明白。
"""

# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '"/home/gpuserver/softwares/spark-2.1.0-bin-hadoop2.6"'
 # Create a variable for our root path
SPARK_HOME = os.environ['SPARK_HOME']

master= "local"
spark = SparkSession.builder\
    .appName("WORD_COUNT")\
    .master(master)\
    .getOrCreate()
sc = spark.sparkContext


text_file = sc.textFile("file:///home/lufeng/software/models/traintextsum/data/weibo/DA_WEIBO_2018_000.txt")
df1 = text_file.map(lambda x: (x, )).toDF(["col1"])
df2 = df1.select(explode(split(col("col1"), "\s+")).alias("word"))
df3 = df2.groupBy('word').count()
df3.toPandas().to_csv('/home/lufeng/software/models/traintextsum/data/weibo/DA_WEIBO_word_count.txt',sep=' ',
                             index=False,header=False)