# -*- coding: utf-8 -*-

import re
import numpy
import pandas
import constant
from sqlalchemy import create_engine

from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.window import Window

from pyspark.sql.types import StringType

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/talentscout?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds_area = spark.read.jdbc(url=url,table="gb_t_2260",properties={"driver": 'com.mysql.jdbc.Driver'}).select("code","full_name").dropna()
# 身份证编码对应日期
# area_sql = "SELECT code,full_name FROM talentscout.gb/t_2260"
# ds_area = spark.sql(area_sql)
# ds_area.show()

ds = spark.read.jdbc(url=url,table="rc_jbxx").dropna(subset=['ch_name'])
# ds.show()


def replace(column, value):
    return func.when(column == value, func.lit(None)).otherwise(column)

for c_name in ds.columns:
    # 每列数据去除前后空格
    ds = ds.withColumn(c_name, func.trim(func.col(c_name)))
    # 每列数据将无替换为null
    ds = ds.withColumn(c_name, replace(func.col(c_name),"无"))

# ds.show()
# ds.select("job","position").show()


# job为None,position不为None position填充job
def job_position(job, position):
    return func.when((job !=None),job).otherwise(position)

# position为None,job不为None,job填充position
def position_job(position, job):
    return func.when((position !=None),position).otherwise(job)

ds = ds.withColumn("job",job_position(func.col("job"), func.col("position")))\
    .withColumn("position", position_job(func.col("position"), func.col("job")))


# ds.select("job","position").show()
ds.write.jdbc(mode="overwrite",url = url,table="sunlu_step1",properties={"driver": 'com.mysql.jdbc.Driver'})
ds.select("sex").drop_duplicates().show(truncate = False)









spark.stop()