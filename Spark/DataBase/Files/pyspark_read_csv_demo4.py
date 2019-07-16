# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午5:10 
 @File    : pyspark_read_csv_demo4.py
 @Note    : 
 
 """


import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StringType,ArrayType
import jieba

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

file_path = "/Users/sunlu/Documents/创新研究院/实习生/招投标打标签/ztb_titlt_csv/*"

t_path  ="/Users/sunlu/Documents/创新研究院/实习生/招投标打标签/ztb_titlt_csv/归档/t_ztb_csv_20.csv"
t_ds = spark.read.csv(t_path,header = True,encoding="UTF-8").select("id","url","title","label")
t_ds.show()

# ds = spark.read.csv(file_path,header = True,encoding="UTF-8").select("id","url","title","label")
# ds = spark.read.csv(file_path,header = True,encoding="UTF-8").select("id","url","title","label")
# print(ds.count())

# ds.show(truncate=False)


url = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
# url = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=GBK&user=root&password=root"
# url = "jdbc:mysql://localhost:3306/ylzx?useUnicode=true&characterEncoding=utf8mb4&user=root&password=root"

t_ds.write.jdbc(url = url, table= "t_ylzx_title_label",mode="overwrite", properties={"driver": 'com.mysql.jdbc.Driver'})
# ds.write.jdbc(url = url, table= "ylzx_title_label",mode="append", properties={"driver": 'com.mysql.jdbc.Driver'})
# ds.coalesce(1).write.csv(path="/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/ztb_title_label",mode="overwrite",header=True,encoding="UTF-8")