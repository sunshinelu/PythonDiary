# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/28 上午9:25 
 @File    : StringIndexer_Demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession
from pyspark.ml.feature import IndexToString, StringIndexer

spark = SparkSession\
        .builder\
        .appName("StringIndexer_Demo1")\
        .getOrCreate()
df = spark.createDataFrame(
    [(0, "d"), (1, "b"), (2, "c"), (3, "d"), (4, "d"), (5, "c")],
    ["id", "category"])
df.show(truncate=False)

indexer = StringIndexer(inputCol="category", outputCol="categoryIndex")
model = indexer.fit(df)
indexed = model.transform(df)

print("Transformed string column '%s' to indexed column '%s'"
      % (indexer.getInputCol(), indexer.getOutputCol()))
indexed.show()
print("Transformed string column labels is '%s' '"
      % (model.labels))

print(type(model.labels))
list_1 = ['a', 'c', 'b']
list_2 = ['a', 'c', 'b','d']


print("StringIndexer will store labels in output column metadata\n")

converter = IndexToString(inputCol="categoryIndex", outputCol="originalCategory")
converted = converter.transform(indexed)

print("Transformed indexed column '%s' back to original string column '%s' using "
      "labels in metadata" % (converter.getInputCol(), converter.getOutputCol()))
converted.show()