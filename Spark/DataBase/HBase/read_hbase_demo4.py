# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午4:05 
 @File    : read_hbase_demo4.py
 @Note    : 
 
 """

from pyspark import SparkConf, SQLContext
from pyspark.sql import SparkSession
from datetime import datetime
import json

conf = (SparkConf()
       .setAppName("RW_from_HBase"))

spark = SparkSession.builder \
     .appName(" ") \
     .config(conf=conf) \
     .getOrCreate()

sc = spark.sparkContext
sqlc = SQLContext(sc)

data_source_format = 'org.apache.spark.sql.execution.datasources.hbase'

catalog = json.dumps(
    {
        "table":{"namespace":"default", "name":"t_student_sunlu"},
        "rowkey":"id",
        "columns":{
                       "id":{"cf":"rowkey", "col":"key", "type":"string"},
                       "name":{"cf":"info", "col":"name", "type":"string"},
                       "age":{"cf":"info", "col":"age", "type":"string"},
                       "gender":{"cf":"info", "col":"gender","type":"string"}
        }
    })

# Writing into HBase
# mydf.write\
#     .options(catalog=catalog, newtable = 5)\
#     .format(data_source_format)\
#     .save()

# Reading from Hbase
df = sqlc.read\
    .options(catalog=catalog)\
    .format(data_source_format)\
    .load()

df.show()
"""
报错：
py4j.protocol.Py4JJavaError: An error occurred while calling o32.load.
: java.lang.NoClassDefFoundError: org/apache/hadoop/hbase/NamespaceNotFoundException
	at org.apache.spark.sql.execution.datasources.hbase.DefaultSource.createRelation(HBaseRelation.scala:51)
	at org.apache.spark.sql.execution.datasources.DataSource.resolveRelation(DataSource.scala:318)
	at org.apache.spark.sql.DataFrameReader.loadV1Source(DataFrameReader.scala:223)
	at org.apache.spark.sql.DataFrameReader.load(DataFrameReader.scala:211)
	at org.apache.spark.sql.DataFrameReader.load(DataFrameReader.scala:167)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:497)
	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
	at py4j.Gateway.invoke(Gateway.java:282)
	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
	at py4j.commands.CallCommand.execute(CallCommand.java:79)
	at py4j.GatewayConnection.run(GatewayConnection.java:238)
	at java.lang.Thread.run(Thread.java:745)
Caused by: java.lang.ClassNotFoundException: org.apache.hadoop.hbase.NamespaceNotFoundException
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:331)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	... 16 more
"""