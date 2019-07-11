# -*- coding: utf-8 -*-

"""
 @Author  : sunlu
 @Date    : 19/7/11 上午10:32
 @File    : pyspark_read_csv_demo2.py
 @Note    :

 """

"""
读取招投标title数据，使用jieba进行分词，然后进行word count，找出这些信息化招投标文件中排名较高的词。

参考链接：
Pyspark Word2Vec + jieba 训练词向量流程
https://zhuanlan.zhihu.com/p/60532089

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

path_import = "/Users/sunlu/Downloads/title.csv"
ds1 = spark.read.csv(path_import,header = False,encoding="UTF-8").toDF("title")

# ds1.show()


def seg(x):
    jieba_seg_generator = jieba.cut(x, cut_all=False)
    words = []
    for word in jieba_seg_generator:
        if len(word) > 1:
            words.append(word)
    return " ".join(words)

def seg_list(x):
    jieba_seg_generator=jieba.cut(x, cut_all=False)
    words = []
    for word in jieba_seg_generator:
        if  len(word)>1:
            words.append(word)
    return words


seg_udf = F.udf(seg, StringType())

ds2 = ds1.withColumn('seg',seg_udf(ds1['title']))

ds3 = ds2.withColumn("words", F.explode(F.split(F.col("seg"), "\s+")))

# ds3.select("title","words").show(truncate=False)

ds4 = ds3.groupBy("words").agg(F.count("words")).orderBy(F.col("count(words)").desc())

# ds4.show(truncate=False)

file_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/ztb_word_count.csv"
ds4.toPandas().to_csv(file_path, encoding = 'utf_8_sig',
                             index = False,
                             header = True)

