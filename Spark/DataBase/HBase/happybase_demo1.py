# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/25 上午11:21 
 @File    : happybase_demo1.py
 @Note    : 
  参考链接：
 thriftpy2.transport.TTransportException: TTransportException("Could not connect to(9090)问题解决
https://blog.csdn.net/haiyan09/article/details/99993800


首先要检查ThriftServer是否启动，在bigdata2中启动 ThriftServer。

jps
cd $HBASE_HOME
cd bin/
hbase-daemon.sh start thrift
jps

 """


import happybase
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("read HBase data")\
        .getOrCreate()

sc = spark.sparkContext
#
# # host = "192.168.37.21,192.168.37.22,192.168.37.23"
host = "192.168.37.22"
table_name = 't_student_sunlu'

connection = happybase.Connection(host=host)
print(connection.tables())