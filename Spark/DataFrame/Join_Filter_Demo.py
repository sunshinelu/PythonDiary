# -*- coding: utf-8 -*-


import os

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

spark = SparkSession\
        .builder\
        .appName("join and filter demo")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/talentscout?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds = spark.read.jdbc(url=url,table="country_data_export")
ds = spark.read.jdbc(url=url,table="country_data_export")