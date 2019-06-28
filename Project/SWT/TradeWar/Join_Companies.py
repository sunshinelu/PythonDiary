# -*- coding: utf-8 -*-

"""

"""

import os

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds = spark.read.jdbc(url=url,table="data_export")
ds.printSchema()
# print(ds.count())

ds_COUNTRY = ds.select("COUNTRY").dropDuplicates()
print(ds_COUNTRY.count())

ds_companies = spark.read.jdbc(url=url,table="top100_company").toDF("name1","code1")
# ds_companies.show()

ds1 = ds.join(ds_companies,ds.COMPANYNAME == ds_companies.name1,"inner")
# ds1.show(truncate=False)
# print(ds1.count())

# print(ds1.dropDuplicates().count())

# ds2 = ds.filter(ds.COMPANYNAME == ds_companies.name1) # 无法执行
# ds2.show()