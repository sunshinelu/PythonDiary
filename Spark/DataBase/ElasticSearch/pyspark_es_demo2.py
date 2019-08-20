# -*- coding: utf-8 -*-

"""
@Author  : sunlu
@Time    : 2019/8/20 21:33
@File    : pyspark_es_demo2.py
@Note:

参考链接：
https://stackoverflow.com/questions/42114519/inserting-arrays-in-elasticsearch-via-pyspark

查看索引数：
curl http://127.0.0.1:9200/_cat/indices?v

删除index索引：
curl -X DELETE http://127.0.0.1:9200/index

删除pyspark_es2索引：
curl -X DELETE http://127.0.0.1:9200/pyspark_es2

"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession\
        .builder\
        .appName("spark read and write es")\
        .getOrCreate()

schema = StructType([  # schema
    StructField("id", StringType(), True),
    StructField("email", ArrayType(StringType()), True)])

df = spark.createDataFrame([{"id": "id1"},
                            {"id": "id2", "email": None},
                            {"id": "id3","email": ["email1@gmail.com"]},
                            {"id": "id4", "email": ["email1@gmail.com", "email2@gmail.com"]}],
                           schema=schema)
df.show(truncate=False)

df.write\
    .format("org.elasticsearch.spark.sql")\
    .option("es.nodes","127.0.0.1")\
    .option("es.resource","index/type")\
    .option("es.mapping.id", "id")\
    .save()

spark.stop()