# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/29 下午4:21 
 @File    : lda_demo_1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
from pyspark.ml.clustering import LDA

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

spark_home  ="/Users/sunlu/Software/spark-2.4.3-bin-hadoop2.6/"
# Loads data.
dataset = spark.read.format("libsvm").load(spark_home + "data/mllib/sample_lda_libsvm_data.txt")

# Trains a LDA model.
lda = LDA(k=10, maxIter=10)
model = lda.fit(dataset)

ll = model.logLikelihood(dataset)
lp = model.logPerplexity(dataset)
print("The lower bound on the log likelihood of the entire corpus: " + str(ll))
print("The upper bound on perplexity: " + str(lp))

# Describe topics.
topics = model.describeTopics(3)
print("The topics described by their top-weighted terms:")
topics.show(truncate=False)

# Shows the result
transformed = model.transform(dataset)
transformed.show(truncate=False)

topics_M = model.topicsMatrix()
print(topics_M)

