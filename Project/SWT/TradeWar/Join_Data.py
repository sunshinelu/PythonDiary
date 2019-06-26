# -*- coding: utf-8 -*-

"""

"""

import os

from pyspark.sql import SparkSession
from pyspark.sql.window import Window

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

# Loading data from a JDBC source

url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"
ds = spark.read.jdbc(url=url,table="b_data_201707_e")
ds_company_code = spark.read.jdbc(url=url,table="ut_company_code").select("CODE","NAME").withColumnRenamed("NAME","COMPANYNAME")
ds_consign_code = spark.read.jdbc(url=url,table="ut_consign_code").select("CODE","NAME").withColumnRenamed("NAME","CONSIGN")
ds_country_code = spark.read.jdbc(url=url,table="ut_country_code").select("CODE","NAME").withColumnRenamed("NAME","COUNTRY")
ds_cust_code = spark.read.jdbc(url=url,table="ut_cust_code").select("CODE","NAME").withColumnRenamed("NAME","CUST")
ds_hs_code = spark.read.jdbc(url=url,table="ut_hs_code").select("CODE","NAME").withColumnRenamed("NAME","COMMODITIES")
ds_trade_code = spark.read.jdbc(url=url,table="ut_trade_code").select("CODE","NAME").withColumnRenamed("NAME","TRADE")
ds_transport_code = spark.read.jdbc(url=url,table="ut_transport_code").select("CODE","NAME").withColumnRenamed("NAME","TRANSPORT")


ds1 = ds.join(ds_company_code, ds.COMPANYCODE == ds_company_code.CODE,"inner").drop("CODE").drop("COMPANYCODE")

ds2 = ds1.join(ds_hs_code, ds1.HSCODE == ds_hs_code.CODE,"inner").drop("CODE").drop("HSCODE")

ds3 = ds2.join(ds_consign_code, ds2.CONSIGNCODE == ds_consign_code.CODE, "inner").drop("CODE").drop("CONSIGNCODE")

ds4 = ds3.join(ds_trade_code, ds3.TRADECODE == ds_trade_code.CODE, "inner").drop("CODE").drop("TRADECODE")

ds5 = ds4.join(ds_country_code, ds4.COUNTRYCODE == ds_country_code.CODE,"inner").drop("CODE").drop("COUNTRYCODE")

ds6 = ds5.join(ds_cust_code, ds5.CUSTCODE == ds_cust_code.CODE, "inner").drop("CODE").drop("CUSTCODE")

ds7 = ds6.join(ds_transport_code, ds6.TRANSPORTCODE == ds_transport_code.CODE, "inner").drop("CODE").drop("TRANSPORTCODE")

col_name = ["COMPANYNAME","COMMODITIES","UNITCODE","CONSIGN","TRADE","COUNTRY","CUST","TRANSPORT","QUNT","SUMQ","USD","SUMM","RMB","RMBSUMM"]
# 企业名、主要商品、计量单位、货源地（出口）/境内目的地（进口）、贸易方式、国别、进出口关区、运输方式、当月数量、累计数量、当月美元、累计美元、当月rmb、累计rmb
ds8 = ds7.select(col_name)

# ds7.printSchema()
# print("========================")
# ds8.printSchema()

# ds8.show(truncate=False)

ds8.coalesce(5).write.mode("overwrite").jdbc(url=url,table="b_data_201707_e_ana")

