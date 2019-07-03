# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import *

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

path_import = "/Users/sunlu/Documents/创新研究院/产品/Evay人工智能平台/产品-Evay人工智能平台v1.0/最佳实践/商务厅/贸易战影响分析/COMMODITIES_TYPE_AND_CODE.csv"
ds = spark.read.csv(path_import,header=True,encoding="UTF-8").drop("_c3")
# ds.show()

# url = "jdbc:mysql://10.20.5.49:3306/swt_tradewar?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"
url = "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8&user=root&password=root"

ds_hs_code = spark.read.jdbc(url=url,table="ut_hs_code").select("CODE","NAME").withColumnRenamed("NAME","COMMODITIES")

ds1 = ds.join(ds_hs_code, "CODE","inner")
# ds1.show(truncate=False)
ds1.write.jdbc(mode="overwrite",url=url,table="COMMODITIES_TYPE",properties={"driver": 'com.mysql.jdbc.Driver'})