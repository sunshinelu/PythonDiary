# -*- coding: utf-8 -*-

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

ds1 = spark.read.jdbc(url="jdbc:mysql://localhost:3306/data_mining_db?user=root&password=root",
                      table="ml_info_item",
                      properties={"driver": 'com.mysql.jdbc.Driver'})

ds1.show(5)
ds1.printSchema()

