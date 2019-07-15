# -*- coding: utf-8 -*-

"""
读取本地csv文件，并将结果保存到mysql中。

"""
from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

path_import = "/Users/sunlu/Documents/创新研究院/产品/Evay人工智能平台/产品-Evay人工智能平台v1.0/最佳实践/商务厅/贸易战影响分析/贸易摩擦清单+行业详细hscode.csv"
ds1 = spark.read.csv(path_import,header=True,encoding="UTF-8").select("HS_CODE","TYPE").toDF("HSCODE","Industry")

# ds1.show()
print(ds1.count())
print(ds1.dropDuplicates().count())
print(ds1.select("HSCODE").dropDuplicates().count())


# Saving data to a JDBC source
ds1.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "Industry") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()