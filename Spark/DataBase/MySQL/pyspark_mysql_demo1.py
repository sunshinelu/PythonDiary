# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "rc_jbxx") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

ds2 = ds1.select("address").dropDuplicates().dropna()

# Saving data to a JDBC source
ds2.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "t_write") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()