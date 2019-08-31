# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/29 下午5:36 
 @File    : lda_demo_2.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
from pyspark.ml.clustering import LDA
from pyspark.ml.linalg import Vectors, SparseVector

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

df = spark.createDataFrame([[1, Vectors.dense([0.0, 1.0])],
                            [2, SparseVector(2, {0: 1.0})],], ["id", "features"])
lda = LDA(k=2, seed=1, optimizer="em")
model = lda.fit(df)
print(model.isDistributed())
# True

print(model.vocabSize())

model.describeTopics().show()

print(model.topicsMatrix())