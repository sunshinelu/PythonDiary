# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午4:07 
 @File    : read_hbase_demo6.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[*]').appName('test_1').getOrCreate()


catalog = ''.join("""{
      "table":{"namespace":"test", "name":"test_shc"},
      "rowkey":"key",
      "columns":{
      "col0":{"cf":"rowkey", "col":"key", "type":"string"},
      "col1":{"cf":"result", "col":"class", "type":"string"}
      }
      }""".split())

data_source_format = 'org.apache.spark.sql.execution.datasources.hbase'
df = spark.sparkContext.parallelize([('a', '1.0'), ('b', '2.0')]).toDF(schema=['col0', 'col1'])
df.show()
df.write.options(catalog=catalog, newTable="5").format(data_source_format).save()
df_read = spark.read.options(catalog=catalog).format(data_source_format).load()
df_read.show()