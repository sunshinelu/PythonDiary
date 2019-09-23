# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/23 下午4:07 
 @File    : read_hbase_demo5.py
 @Note    : 

 https://stackoverflow.com/questions/54826218/what-is-the-best-possible-way-of-interacting-with-hbase-using-pyspark?noredirect=1#comment96435984_54826218
 """

from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.master("local[*]").appName("HelloSpark").getOrCreate()

    dataSourceFormat = "org.apache.spark.sql.execution.datasources.hbase"
    writeCatalog = ''.join("""{
                "table":{"namespace":"default", "name":"t_tblEmployee", "tableCoder":"PrimitiveType"},
                "rowkey":"key",
                "columns":{
                  "key":{"cf":"rowkey", "col":"key", "type":"int"},
                  "empId":{"cf":"personal","col":"empId","type":"string"},
                  "empName":{"cf":"personal", "col":"empName", "type":"string"},
                  "empWeight":{"cf":"personal", "col":"empWeight", "type":"double"}
                }
              }""".split())

    writeDF = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/Users/sunlu/Workspaces/PyCharm/PythonDiary/data/emp.csv")
    print("csv file read", writeDF.show())
    writeDF.write.options(catalog=writeCatalog, newtable=5).format(dataSourceFormat).save()
    print("csv file written to HBase")

    readCatalog = ''.join("""{
                "table":{"namespace":"default", "name":"t_tblEmployee"},
                "rowkey":"key",
                "columns":{
                  "key":{"cf":"rowkey", "col":"key", "type":"int"},
                  "empId":{"cf":"personal","col":"empId","type":"string"},
                  "empName":{"cf":"personal", "col":"empName", "type":"string"}
                }
              }""".split())

    print("going to read data from Hbase table")
    readDF = spark.read.options(catalog=readCatalog).format(dataSourceFormat).load()
    print("data read from HBase table")
    readDF.select("empId", "empName").show()
    readDF.show()

# entry point for PySpark application
if __name__ == '__main__':
    main()
