# -*- coding: utf-8 -*-

"""
读取本地csv文件，并将结果保存到mysql中。

"""
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

path_import = "/Users/sunlu/Documents/创新研究院/产品/Evay人工智能平台/产品-Evay人工智能平台v1.0/最佳实践/商务厅/贸易战影响分析/top100.csv"
ds1 = spark.read.csv(path_import,header=None,encoding="UTF-8").toDF("companies")
ds1.show()


# Saving data to a JDBC source
ds1.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "top100companies") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()