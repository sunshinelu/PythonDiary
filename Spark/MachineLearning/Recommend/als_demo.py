# -*- coding: utf-8 -*-


from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import *

from pyspark.sql import SparkSession

import sys
reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()

import os
# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '/Users/sunlu/Software/spark-2.0.2-bin-hadoop2.6'
 # Create a variable for our root path
SPARK_HOME = os.environ['SPARK_HOME']

master= "local"
spark = SparkSession.builder\
    .appName("als_demo")\
    .master(master)\
    .getOrCreate()

sc = spark.sparkContext

ratings = spark.read.option("header","true").\
    csv(r'/Users/sunlu/Workspaces/PyCharm/PythonDiary/data/als_new.csv').\
    withColumn("user",col("user").cast("int")).\
    withColumn("item",col("item").cast("int")).\
    withColumn("rating",col("rating").cast("double"))
ratings.show()
print(ratings.printSchema)

(training, test) = ratings.randomSplit([0.8, 0.2])

als = ALS(maxIter=5, regParam=0.01, userCol="user", itemCol="item", ratingCol="rating")
model = als.fit(training)


predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))


userRecs = model.recommendForAllUsers(2)

bookRecs = model.recommendForAllItems(2)


users = ratings.select(als.getUserCol()).distinct().limit(3)
userSubsetRecs = model.recommendForUserSubset(users, 10)

books = ratings.select(als.getItemCol()).distinct().limit(3)
movieSubSetRecs = model.recommendForItemSubset(books, 10)