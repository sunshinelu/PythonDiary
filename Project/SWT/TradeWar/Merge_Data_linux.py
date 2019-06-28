# -*- coding: utf-8 -*-


"""

在192.168.37.28 bigdata8上执行
报错：
py4j.protocol.Py4JJavaError: An error occurred while calling o361.jdbc. : scala.MatchError: null

1. pyspark 写入MySQL报错 An error occurred while calling o45.jdbc.: scala.MatchError: null 解决方案
https://blog.csdn.net/helloxiaozhe/article/details/81033767


"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession\
        .builder\
        .appName("merge data")\
        .getOrCreate()

ds_tables = spark.read.format('jdbc').\
    options(url='jdbc:mysql://10.20.5.49:3306/',
            dbtable='information_schema.tables',
            user='root',
            password='BigData@2018',
            driver='com.mysql.jdbc.Driver').\
    load().\
    filter("table_schema = 'swt_tradewar'").\
    select("TABLE_NAME").filter(col("TABLE_NAME").startswith("b_data_"))

list_tables = list(ds_tables.rdd.map(lambda x:x.TABLE_NAME).collect())

list_tables = filter(lambda x:str(x).startswith("b_data_2017"),list_tables)

url = "jdbc:mysql://10.20.5.49:3306/swt_tradewar?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

ds_company_code = spark.read.jdbc(url=url,table="ut_company_code").select("CODE","NAME").withColumnRenamed("NAME","COMPANYNAME")
ds_consign_code = spark.read.jdbc(url=url,table="ut_consign_code").select("CODE","NAME").withColumnRenamed("NAME","CONSIGN")
ds_country_code = spark.read.jdbc(url=url,table="ut_country_code").select("CODE","NAME").withColumnRenamed("NAME","COUNTRY")
ds_cust_code = spark.read.jdbc(url=url,table="ut_cust_code").select("CODE","NAME").withColumnRenamed("NAME","CUST")
ds_hs_code = spark.read.jdbc(url=url,table="ut_hs_code").select("CODE","NAME").withColumnRenamed("NAME","COMMODITIES")
ds_trade_code = spark.read.jdbc(url=url,table="ut_trade_code").select("CODE","NAME").withColumnRenamed("NAME","TRADE")
ds_transport_code = spark.read.jdbc(url=url,table="ut_transport_code").select("CODE","NAME").withColumnRenamed("NAME","TRANSPORT")

# 企业名、主要商品、计量单位、货源地（出口）/境内目的地（进口）、贸易方式、国别、进出口关区、运输方式、当月数量、累计数量、当月美元、累计美元、当月rmb、累计rmb
col_name = ["COMPANYNAME", "COMMODITIES", "UNITCODE", "CONSIGN", "TRADE", "COUNTRY", "CUST", "TRANSPORT", "QUNT",
            "SUMQ", "USD", "SUMM", "RMB", "RMBSUMM"]

for db_table in list_tables:
    print(db_table+" start!")
    type = str(db_table).split("_")[3]
    time = str(db_table).split("_")[2]
    year = str(time[0:4])
    month = str(time[4:6])
    ds = spark.read.jdbc(url=url, table=db_table)
    ds1 = ds.join(ds_company_code, ds.COMPANYCODE == ds_company_code.CODE, "inner").drop("CODE").drop("COMPANYCODE")
    ds2 = ds1.join(ds_hs_code, ds1.HSCODE == ds_hs_code.CODE, "inner").drop("CODE").drop("HSCODE")
    ds3 = ds2.join(ds_consign_code, ds2.CONSIGNCODE == ds_consign_code.CODE, "inner").drop("CODE").drop("CONSIGNCODE")
    ds4 = ds3.join(ds_trade_code, ds3.TRADECODE == ds_trade_code.CODE, "inner").drop("CODE").drop("TRADECODE")
    ds5 = ds4.join(ds_country_code, ds4.COUNTRYCODE == ds_country_code.CODE, "inner").drop("CODE").drop("COUNTRYCODE")
    ds6 = ds5.join(ds_cust_code, ds5.CUSTCODE == ds_cust_code.CODE, "inner").drop("CODE").drop("CUSTCODE")
    ds7 = ds6.join(ds_transport_code, ds6.TRANSPORTCODE == ds_transport_code.CODE, "inner").drop("CODE").drop("TRANSPORTCODE")
    ds8 = ds7.select(col_name).withColumn("TIME", lit(time)).withColumn("YEAR", lit(year)).withColumn("MONTH", lit(month))
    # if type == "e":
    #     # ds8.coalesce(5).write.mode("append").jdbc(url=url, table="data_export") # 在bigdata8运行出错代码
    #     ds8.coalesce(15).write.jdbc(mode="append", url=url,table="data_export_" + year, properties={"driver": 'com.mysql.jdbc.Driver'})
    #     print(db_table + " finish!")
    if type == "i":
        # ds8.coalesce(5).write.mode("append").jdbc(url=url, table="data_import")  # 在bigdata8运行出错代码
        ds8.coalesce(15).write.jdbc(mode="append", url=url,table="data_import_" + year, properties={"driver": 'com.mysql.jdbc.Driver'})
        print(db_table + " finish!")



spark.stop()