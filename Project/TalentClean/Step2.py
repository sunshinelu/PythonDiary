# -*- coding: utf-8 -*-


from pyspark.sql import SparkSession
import pyspark.sql.functions as func
from pyspark.sql.window import Window
from Project.TalentClean.idcard_util import check_idcard

from pyspark.sql.types import StringType

spark = SparkSession\
        .builder\
        .appName("step 2")\
        .getOrCreate()

# Loading data from a JDBC source
url = "jdbc:mysql://localhost:3306/talentscout?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds_sex = spark.read.jdbc(url=url,table="dict_new",properties={"driver": 'com.mysql.jdbc.Driver'})\
    .filter((func.col("classify") == "性别") | (func.col("classify") == "性别（数字）"))\
    .orderBy(func.col("sort")).select("name","sort")
# ds_sex.show(truncate=False)

ds = spark.read.jdbc(url=url,table="sunlu_step1",properties={"driver": 'com.mysql.jdbc.Driver'})

# 小写转大写
def to_upper(x):
    return str(x).upper()
to_upper_udf = func.udf(to_upper,StringType())

ds = ds.withColumn("rc_id", to_upper_udf(func.col("rc_id")))
# ds.select("rc_id").show(200,truncate=False)

# 去除字符串中的空格
def remove_blank(x):
    return x.replace(' ', '')
remove_blank_udf = func.udf(remove_blank, StringType())

ds = ds.withColumn("ch_name",remove_blank_udf(func.col("ch_name")))

#
check_idcard_udf = func.udf(check_idcard,StringType())
ds = ds.withColumn("identification_id",check_idcard_udf(func.col("identification_id")))
ds.select("identification_id").drop_duplicates().show(200,truncate=False)












spark.stop()