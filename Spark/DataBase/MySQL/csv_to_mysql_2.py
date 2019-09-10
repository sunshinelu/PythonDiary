# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/9 下午12:34 
 @File    : csv_to_mysql_2.py
 @Note    : 
 
 """


import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml import Pipeline

root_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
data_path = root_dir + "/data/iris_dataset.csv"
print(data_path)


#import SparkSession
spark=SparkSession.builder.appName('k-means').getOrCreate()

#read the dataset
df = spark.read.csv(data_path,inferSchema=True,header=True)

#select data for building model
train_df,test_df=df.randomSplit([0.75,0.25])

# Saving data to a JDBC source
train_df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "ml_iris_tran") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()

test_df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "ml_iris_test") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()