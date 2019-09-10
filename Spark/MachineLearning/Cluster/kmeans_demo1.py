# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/9 下午12:19 
 @File    : kmeans_demo1.py
 @Note    : 
 
 """
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml import Pipeline
from pyspark.ml.clustering import KMeans


root_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
data_path = root_dir + "/data/iris_dataset.csv"
print(data_path)


#import SparkSession
spark=SparkSession.builder.appName('random_forest').getOrCreate()

#read the dataset
df = spark.read.csv(data_path,inferSchema=True,header=True)

input_cols=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

# Transform all features into a vector using VectorAssembler
vec_assembler = VectorAssembler(inputCols = input_cols, outputCol='features')
final_data = vec_assembler.transform(df)

#Selecting k =3 for kmeans clustering
kmeans = KMeans(featuresCol='features',k=3,)

model = kmeans.fit(final_data)

pred = model.transform(final_data)

pred.show(truncate=False)
pred.printSchema()
