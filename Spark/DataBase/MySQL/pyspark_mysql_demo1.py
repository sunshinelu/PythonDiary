# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "ml_info_item") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

ds2 = ds1.select("ITEM_ID").dropDuplicates().dropna()

# Saving data to a JDBC source
ds2.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "t_write") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()