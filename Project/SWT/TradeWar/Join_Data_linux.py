# -*- coding: utf-8 -*-

"""

nohup spark-submit --master yarn --deploy-mode client --num-executors 10 --executor-cores 2 /root/lulu/Workspace/swt/Join_Data_linux.py &

查看任务执行状态
yarn application -list



"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

url = "jdbc:mysql://10.20.5.49:3306/swt_tradewar?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

# data_table = "data_import"
data_table = "data_export"
ds = spark.read.jdbc(url=url,table=data_table)
# print(ds.select("HSCODE").dropDuplicates().count())

ds_industry_code = spark.read.jdbc(url=url,table="Industry")\
    .select("HSCODE").dropDuplicates().withColumnRenamed("HSCODE","HSCODE2")

# ds1 = ds.where(ds.HSCODE == ds_industry_code.HSCODE) # 报错

# ds1 = ds.join(ds_industry_code, "HSCODE","inner")

# 将dat_order_item和dat_order DF注册成spark临时表
ds.registerTempTable("ds")
ds_industry_code.registerTempTable("ds_industry_code")

ds1 = spark.sql("select * from ds, ds_industry_code where ds.HSCODE=ds_industry_code.HSCODE2")

ds1.coalesce(100).write.jdbc(mode="overwrite", url=url,table="industry_" + data_table, properties={"driver": 'com.mysql.jdbc.Driver'})

