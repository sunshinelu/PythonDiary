# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/3 上午10:08 
 @File    : LinearRegression_demo1.py
 @Note    : 
 
 """


from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

spark_home  ="/Users/sunlu/Software/spark-2.4.3-bin-hadoop2.6/"
# Loads data.
training = spark.read.format("libsvm").load(spark_home + "data/mllib/sample_linear_regression_data.txt")

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

# Fit the model
lrModel = lr.fit(training)

# Print the coefficients and intercept for linear regression
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))

# Summarize the model over the training set and print out some metrics
trainingSummary = lrModel.summary
print("numIterations: %d" % trainingSummary.totalIterations)
print("objectiveHistory: %s" % str(trainingSummary.objectiveHistory))
trainingSummary.residuals.show()
print("RMSE: %f" % trainingSummary.rootMeanSquaredError)
print("r2: %f" % trainingSummary.r2)

pred = lrModel.transform(training)
pred.show(truncate=False)
pred.printSchema()