# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/25 下午2:09 
 @File    : read_ES_Demo2.py
 @Note    : 

读取http://10.20.5.112:5601/中的 springer-data/doc 索引。

 报错1：
 org.elasticsearch.hadoop.rest.EsHadoopParsingException: Cannot parse value [2016/05/10] for field [publishTime]
解决方案：
在SparkSession后添加配置
.config("spark.es.mapping.date.rich","false") √ 此方法测试成功

在spark.read 添加option
.option("es.mapping.date.rich", "false") 此方法未验证。

参考链接：
https://elasticsearch.cn/question/584
https://zturn.cc/?p=164
https://stackoverflow.com/questions/48469761/write-to-elasticsearch-from-spark-wrong-timestamp
https://stackoverflow.com/questions/55205679/pyspark-write-dstream-data-to-es-with-saveasnewapihadoopfile-get-warnning

 """


from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import *

import os
# os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


spark = SparkSession\
    .builder \
    .config("spark.es.mapping.date.rich","false")\
    .appName("spark read and write es")\
    .getOrCreate()

# .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-20_2.11:6.2.3")\

#
# read data from elasticsearch
df = spark.read \
    .format("org.elasticsearch.spark.sql") \
    .option("es.read.field.as.array.include","Authora,keywords,classNumber,authors,author_aff") \
    .option("es.nodes", "http://10.20.5.112") \
    .option("es.resource", "springer-data/doc") \
    .load()
# .option("es.read.field.as.array.include","Authora,keywords,classNumber,authors") \

df.printSchema()
"""
root
 |-- @timestamp: string (nullable = true)
 |-- @version: string (nullable = true)
 |-- Authora: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- abstracts: string (nullable = true)
 |-- author_aff: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- authors: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- host: string (nullable = true)
 |-- issn: string (nullable = true)
 |-- journal: string (nullable = true)
 |-- keywords: array (nullable = true)
 |    |-- element: string (containsNull = true)
 |-- path: string (nullable = true)
 |-- publishTime: string (nullable = true)
 |-- qkid: string (nullable = true)
 |-- rowkey: string (nullable = true)
 |-- title: string (nullable = true)
 |-- type: string (nullable = true)
"""

print(df.count())
"""
2416686
"""