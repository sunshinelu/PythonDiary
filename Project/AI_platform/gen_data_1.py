# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/11 下午2:33 
 @File    : gen_data_1.py
 @Note    : 
 
 """


import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

url = "jdbc:mysql://10.20.5.49:3306/rgznpt_sjy?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"


data_table = "sjycl_rc_jbxx"
ds = spark.read.jdbc(url=url,table=data_table)

cols = ["identification_type","identification_id","email","mobile_phone"]

ds1 = ds.select(cols).filter(F.col("identification_type") == "居民身份证")\
    .dropDuplicates().na.drop().sample(fraction=0.03, seed=3).withColumn('rand1', F.rand(seed=10))

# print(ds1.count())
# ds1.show(truncate=False)

ds1.printSchema()

# save_table = "sjycl_test_data_1"

# ds1.write.jdbc(url=url,table=save_table,mode="overwrite")