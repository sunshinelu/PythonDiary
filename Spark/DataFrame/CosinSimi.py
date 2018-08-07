#-*- coding: UTF-8 -*-

"""
Cosine similarity between a static vector and each vector in a Spark data frame
https://hashnode.com/post/cosine-similarity-between-a-static-vector-and-each-vector-in-a-spark-data-frame-cjctjlump0074dlwtfaoe0pwj
https://github.com/leenakhote/virtualSearchDjango/blob/0e6674e39c4121f2a9d9ca355f3cb49593bb1273/udf_test.py
"""
import numpy as np
from pyspark.ml.linalg import *
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql import SQLContext, Row
import os

# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '/Users/sunlu/Software/spark-2.0.2-bin-hadoop2.6'
 # Create a variable for our root path
SPARK_HOME = os.environ['SPARK_HOME']

sc = SparkContext.getOrCreate()
sparkSession = SparkSession(sc)
sqlContext = SQLContext(sc)

# function to generate a random Spark dense vector
def random_dense_vector(length=10):
    return Vectors.dense([float(np.random.random()) for i in xrange(length)])

# create a random static dense vector
static_vector = random_dense_vector()

print static_vector
# create a random DF with dense vectors in column
df = sparkSession.createDataFrame([[random_dense_vector()] for x in xrange(10)], ["myCol"])
df.limit(3).toPandas()

print df.show()
# write our UDF for cosine similarity
def cos_sim(a,b):
    print a,b
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# apply the UDF to the column
df = df.withColumn("coSim", udf(cos_sim, FloatType())(col("myCol"), array([lit(v) for v in static_vector])))
print "9999999999999",df.show()
res = df.limit(10).toPandas()
print res