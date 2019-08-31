# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/30 下午3:13 
 @File    : randomforest_demo_2.py
 @Note    : 
 
 """

import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel

root_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
model_path = root_dir + "/results/rf_model"
data_path = root_dir + "/data/affairs.csv"


#import SparkSession
spark=SparkSession.builder.appName('random_forest').getOrCreate()

#read the dataset
df = spark.read.csv(data_path,inferSchema=True,header=True)\
    .withColumn("affairs", F.col("affairs").cast("string"))

#select data for building model
train_df,test_df=df.randomSplit([0.75,0.25])

rf_model_reload = PipelineModel.load(model_path)

pred_df = rf_model_reload.transform(test_df.drop("affairs"))
pred_df.show()
pred_df.printSchema()