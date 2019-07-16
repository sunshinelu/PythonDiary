# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/16 下午3:39 
 @File    : pyspark_read_csv_demo5.py
 @Note    : 
 
 """



import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StringType,IntegerType
import jieba

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

def to_Int(x):
    if x == "非信息化":
        return "2"
    if x =="信息化":
        return "1"
to_Int_udf = F.udf(to_Int,StringType())

t_path  ="/Users/sunlu/Documents/创新研究院/实习生/招投标打标签/ztb_titlt_csv/归档/t_tb_csv_15.csv"

t_ds = spark.read.csv(t_path,header = True,encoding="UTF-8")\
    .select("title","label").withColumn("label",to_Int_udf(F.col("label")))


t_ds.show()

save_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/ztb_csv_15.csv"
t_ds.toPandas().to_csv(save_path,
                             encoding = 'utf-8',
                             index = False,
                             header = True)