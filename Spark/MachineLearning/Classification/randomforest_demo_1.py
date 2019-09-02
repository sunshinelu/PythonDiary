# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/30 下午3:11 
 @File    : randomforest_demo_1.py
 @Note    : 

 参考链接：
pyspark分类算法之随机森林分类器模型实践【randomForestClassifier】
 https://blog.csdn.net/Together_CZ/article/details/91968439
 """
import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml import Pipeline

root_dir = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
data_path = root_dir + "/data/affairs.csv"
print(data_path)


#import SparkSession
spark=SparkSession.builder.appName('random_forest').getOrCreate()

#read the dataset
df = spark.read.csv(data_path,inferSchema=True,header=True)\
    .withColumn("affairs", F.col("affairs").cast("string"))

#select data for building model
train_df,test_df=df.randomSplit([0.75,0.25])

labelIndexer = StringIndexer(inputCol="affairs", outputCol="affairs"+"_ID").fit(train_df)
assembler = VectorAssembler(inputCols=['rate_marriage', 'age', 'yrs_married', 'children', 'religious'],
                               outputCol="features")

rf_classifier=RandomForestClassifier(labelCol=labelIndexer.getOutputCol(),
                                     featuresCol=assembler.getOutputCol(),
                                     numTrees=50)#.fit(train_df)

rf_pipeline = Pipeline(stages=[labelIndexer, assembler,rf_classifier])


rf_model = rf_pipeline.fit(train_df)

pred_df = rf_model.transform(test_df)
pred_df.show()
pred_df.printSchema()

# save model
model_path = "/Users/sunlu/Workspaces/PyCharm/EvayAIPlatform-V2.0/model/als_model"
model_path = root_dir + "/results/rf_model"
rf_model.write().overwrite().save(model_path)


# rf_classifier=RandomForestClassifier(labelCol='affairs',numTrees=50).fit(train_df)
# rf_predictions=rf_classifier.transform(test_df)
# rf_predictions.show()
# rf_predictions.printSchema()
