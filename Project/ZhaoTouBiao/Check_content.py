# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/15 上午10:45 
 @File    : Check_content.py
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

url = "jdbc:mysql://10.20.5.49:3306/efp5-ztb?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

# data_table = "data_import"
data_table = "collect_ccgp"
ds = spark.read.jdbc(url=url,table=data_table).filter(F.col("contenthh").contains("<div class="))
# print(ds.count())

ds.select("provinces").dropDuplicates().show(truncate=False)

# cols = ["id","url","collect_time","contenthh"]
# ds1 = ds.select(cols)

# ds1.show()

# ds1.select("collect_time")

# url2 = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
#
# ds1.write.jdbc(url = url2, table= "ztb_check_content",mode="overwrite")
