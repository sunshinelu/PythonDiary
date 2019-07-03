# -*- coding: utf-8 -*-

"""

Statistical and Mathematical Functions with DataFrames in Apache Spark
https://databricks.com/blog/2015/06/02/statistical-and-mathematical-functions-with-dataframes-in-spark.html

"""

import os

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

spark = SparkSession\
        .builder\
        .appName("check company")\
        .getOrCreate()

# Loading data from a JDBC source   company_data_import  country_data_export
url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
# table_name = "company_data_import"
table_name = "company_data_export"
ds = spark.read.jdbc(url=url,table=table_name)\
    .withColumn("MONTH", col("MONTH").cast("int"))


# 公司每月向各国出口金额，金额是亿元
company_name = "青岛中联油国际贸易有限公司" # import
country_name = "美国"
ds1 = ds.groupBy("COMPANYNAME","TIME","YEAR","MONTH").agg({"USD": "sum", "RMB": "sum"})\
    .filter(col("COMPANYNAME") == company_name).orderBy(col("TIME").asc())\
    .withColumnRenamed("sum(RMB)","RMB").withColumnRenamed("sum(USD)","USD")
    # .withColumn("sum(RMB)",bround(col("sum(RMB)").cast("float") / 100000000.0, 3))\
    # .withColumn("sum(USD)",bround(col("sum(USD)").cast("float") / 100000000.0, 3))
# ds1.show(200)
# ds1.coalesce(1).write.jdbc(mode="overwrite",url=url,table=table_name + "_qdzly",properties={"driver": 'com.mysql.jdbc.Driver'})
#

# 中国每年向各国出口金额，金额是亿元
type1 = "COMPANYNAME" #  COMPANYNAME  COMMODITIES_TYPE
ds2 = ds.filter(col("MONTH") <= 5).groupBy(type1,"YEAR").agg({"USD": "sum", "RMB": "sum"})\
    .orderBy(col("YEAR").asc())\
    .withColumn("sum(RMB)",bround(col("sum(RMB)").cast("float") / 100000000.0, 3))\
    .withColumn("sum(USD)",bround(col("sum(USD)").cast("float") / 100000000.0, 3))\
    .groupBy(type1).agg({"sum(RMB)":"stddev","sum(USD)":"stddev"})\
    .orderBy(col("stddev(sum(USD))").desc()).dropna()
# ds2.show(200)

# Window function
w1 = Window.partitionBy('COMPANYNAME','YEAR')
w2 = Window.partitionBy('YEAR')
ds3 = ds.filter(col("COUNTRY") != "中国").withColumn("sum_company",sum("USD").over(w1))\
    .withColumn("sum_year",sum("USD").over(w2))\
    .select("COMPANYNAME","YEAR","sum_company","sum_year") \
    .dropDuplicates() \
    .withColumn("percent",bround(col("sum_company") / col("sum_year"),3))\
    .orderBy(col("YEAR").asc(),col("percent").desc()).select("COMPANYNAME","YEAR","percent")

# ds3.printSchema()
# ds3.show()

# ds3.groupBy("YEAR").agg(sum("percent")).show(truncate=False)

ds4 = ds3.groupBy("COMPANYNAME")\
    .pivot('YEAR', ['2015','2016','2017','2018','2019'])\
    .agg(sum('percent')).fillna(0).orderBy(col("2015").desc())

# ds4.printSchema()
# ds4.show()

# ds4.coalesce(1).write.jdbc(mode="overwrite",url=url,table=table_name + "_stddev_company",properties={"driver": 'com.mysql.jdbc.Driver'})
#


ds5 = ds.filter(col("MONTH") <= 5)\
    .groupBy("COUNTRY","COMMODITIES_TYPE","TIME")\
    .agg(sum("RMB"),sum("USD"))\
    .groupBy("COUNTRY","COMMODITIES_TYPE").agg({"sum(RMB)":"stddev","sum(USD)":"stddev"})\
    .orderBy(col("stddev(sum(USD))").desc()).dropna()

# ds5.printSchema()
# ds5.show(truncate=False)

ds.filter(col("MONTH") <= 5)\
    .filter(col("COUNTRY") == "美国")\
    .groupBy("COUNTRY","COMMODITIES_TYPE","TIME")\
    .agg(sum("RMB"),sum("USD"))\
    .groupBy("COUNTRY","COMMODITIES_TYPE").agg({"sum(RMB)":"stddev","sum(USD)":"stddev"})\
    .orderBy(col("stddev(sum(USD))").desc()).dropna()#.show(200,truncate=False)


ds.filter(col("MONTH") <= 5)\
    .filter(col("COMMODITIES_TYPE") == "电器及电子产品")\
    .groupBy("COMPANYNAME", "COUNTRY", "TIME") \
    .agg(sum("RMB"), sum("USD")) \
    .groupBy("COMPANYNAME", "COUNTRY").agg({"sum(RMB)": "stddev", "sum(USD)": "stddev"}) \
    .orderBy(col("stddev(sum(USD))").desc()).dropna().show(200,truncate=False)



spark.stop()