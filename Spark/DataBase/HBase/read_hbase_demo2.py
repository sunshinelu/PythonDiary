# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午2:19 
 @File    : read_hbase_demo2.py
 @Note    : 
 https://mvnrepository.com/artifact/org.apache.spark/spark-examples_2.11/1.6.0-typesafe-001
 """


import json

from pyspark.sql import SparkSession
from pyspark.sql.types import Row,StringType,StructField,StringType,IntegerType

"""
spark = SparkSession\
        .builder\
        .appName("read HBase data")\
        .getOrCreate()

sc = spark.sparkContext

host = "192.168.37.21,192.168.37.22,192.168.37.23"
table = 't_student_sunlu'
clientPort = "2181"
conf = {"hbase.zookeeper.quorum": host,
        "hbase.mapreduce.inputtable": table #,
        # "hbase.zookeeper.property.clientPort":clientPort
        }

keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"

# valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToBigDecimalToStringConverter"
hbase_rdd = sc.newAPIHadoopRDD("org.apache.hadoop.hbase.mapreduce.TableInputFormat",
                               "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
                               "org.apache.hadoop.hbase.client.Result",
                               keyConverter=keyConv,valueConverter=valueConv,conf=conf)
count = hbase_rdd.count()
hbase_rdd.cache()
output = hbase_rdd.collect()
for (k, v) in output:
        print(k, v)

"""



#spark连接hbase，读取RDD数据

spark = SparkSession.builder.master("local[*]").appName("hbase_test").getOrCreate()

host = "192.168.37.21,192.168.37.22,192.168.37.23"
table = 't_student_sunlu'
clientPort = "2181"

hbaseconf = {"hbase.zookeeper.quorum":host,
             "hbase.mapreduce.inputtable":table,
             # "hbase.mapreduce.scan.row.start":"***", "hbase.mapreduce.scan.row.stop":"***"
             }

keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"

valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

hbase_rdd = spark.sparkContext.newAPIHadoopRDD(
    "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    "org.apache.hadoop.hbase.client.Result",
    keyConverter=keyConv, valueConverter=valueConv, conf=hbaseconf)

#从每列的dict中提取列名和取值，组成dict

def call_transfor(y1):
    y2 = [json.loads(i) for i in y1]
    fdc={}
    for i in y2:
        colname = i['qualifier']
        value = i['value']
        fdc[colname] = value
    return fdc

#将hbase RDD转换为DataFrame

def rdd_to_df(hbase_rdd):
    #同一个RowKey对应的列之间是用\n分割，进行split，split后每列是个dict
    fdc_split = hbase_rdd.map(lambda x:(x[0],x[1].split('\n')))
    #提取列名和取值
    fdc_cols = fdc_split.map(lambda x:(x[0],call_transfor(x[1])))
    colnames = ['row_key'] + fdc_cols.map(lambda x:[i for i in x[1]]).take(1)[0]
    fdc_dataframe = fdc_cols.map(lambda x:[x[0]]+[x[1][i] for i in x[1]]).toDF(colnames)
    return fdc_dataframe

#数据转换

fdc_data = rdd_to_df(hbase_rdd)
fdc_data.show()

"""
报错：
py4j.protocol.Py4JJavaError: An error occurred while calling z:org.apache.spark.api.python.PythonRDD.newAPIHadoopRDD.
: java.lang.ClassNotFoundException: org.apache.hadoop.hbase.io.ImmutableBytesWritable
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	at java.lang.Class.forName0(Native Method)
	at java.lang.Class.forName(Class.java:348)
	at org.apache.spark.util.Utils$.classForName(Utils.scala:238)
	at org.apache.spark.api.python.PythonRDD$.newAPIHadoopRDDFromClassNames(PythonRDD.scala:312)
	at org.apache.spark.api.python.PythonRDD$.newAPIHadoopRDD(PythonRDD.scala:297)
	at org.apache.spark.api.python.PythonRDD.newAPIHadoopRDD(PythonRDD.scala)
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
"""