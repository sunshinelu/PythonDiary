# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/25 上午10:56 
 @File    : mysql_to_json.py
 @Note    : 
 
 """


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *


spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "sjycl_test_data_1") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

ds1.show(truncate=False)
ds1.printSchema()

# toJSON 方法中
# file_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/json_file"
# ds1.toJSON().saveAsTextFile(file_path)



# 缺失值用为None
ds2 = ds1.withColumn("JSON", F.to_json(F.struct(
       [F.coalesce(F.col(x), F.lit(None)).alias(x) for x in ds1.columns])))
ds2.select("JSON").write.mode(saveMode="overwrite").format("text").save("/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/json.txt")