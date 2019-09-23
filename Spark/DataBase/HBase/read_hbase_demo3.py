# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午3:45 
 @File    : read_hbase_demo3.py
 @Note    : 
 
 """
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test hbase").getOrCreate()
host = "192.168.37.21,192.168.37.22,192.168.37.23"
table = 't_student_sunlu'

conf = {"hbase.zookeeper.quorum": host, "hbase.mapreduce.inputtable": table}
conf["TableInputFormat.INPUT_TABLE"] = "hbase.mapreduce.scan"

keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"

hbase_rdd = spark.sparkContext.newAPIHadoopRDD(
    "org.apache.hadoop.hbase.mapreduce.TableInputFormat",
    "org.apache.hadoop.hbase.io.ImmutableBytesWritable",
    "org.apache.hadoop.hbase.client.Result",
    keyConverter=keyConv, valueConverter=valueConv, conf=conf
    )

print(hbase_rdd.count())

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