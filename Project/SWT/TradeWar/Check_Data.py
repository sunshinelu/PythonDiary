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
ds = spark.read.jdbc(url=url,table="b_data_201707_e_ana")

ds_company = spark.read.jdbc(url=url,table="top100companies")
ds_company_code = spark.read.jdbc(url=url,table="ut_company_code").select("CODE","NAME")

ds1 = ds_company.join(ds_company_code, ds_company.companies == ds_company_code.NAME, "left")

# ds1.coalesce(10).write.mode("overwrite").jdbc(url=url,table="dup_companies")

w = Window.partitionBy("NAME","companies").orderBy(col("CODE").asc())
ds2 = ds1.dropna().withColumn("rn", row_number().over(w)).where(col("rn") == 2).select("NAME")
ds3 = ds2.join(ds1, ds2.NAME == ds1.NAME, "left").drop("NAME")
# ds3.coalesce(10).write.mode("overwrite").jdbc(url=url,table="dup_companies_2")

# 取差集
ds4 = ds1.dropna().select("NAME").join(ds2, "NAME", "left_anti")
print(ds4.count())
ds5 = ds4.join(ds_company_code,"NAME", "left")
ds5.write.mode("overwrite").jdbc(url=url,table="right_companies")
