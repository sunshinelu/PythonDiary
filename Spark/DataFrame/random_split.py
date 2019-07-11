# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/11 上午8:47 
 @File    : random_split.py
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

url = "jdbc:mysql://10.20.5.49:3306/elan_tender?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

# data_table = "data_import"
data_table = "collect_ccgp"
ds = spark.read.jdbc(url=url,table=data_table)

w = Window.orderBy('id')
ds1 = ds.withColumn("id_increased", F.row_number().over(w))

cols = ["id","url","title"]
random_list = [1.0]*30
splits = ds.select(cols).dropDuplicates(["title"]).randomSplit(random_list, 24)

file_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/ztb_title_csv/ztb_csv_"
# file_path = "/root/sunlu/ztb_csv/ztb_csv_"
"""
pandas输出csv文件用Excel打开中文乱码问题：
只需要在to_csv方法中的encoding参数中设置为'utf-8_sig'即可，表示有BOM的utf8编码，这样生成的csv文件用excel打开便不会出现中文乱码问题。
"""
for i in range(0,30):
    splits[i].toPandas().to_csv(file_path + str(i) + ".csv",
                             encoding = 'utf_8_sig',
                             index = False,
                             header = True)

spark.stop()