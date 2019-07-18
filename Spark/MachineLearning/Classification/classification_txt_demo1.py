# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/17 下午4:06 
 @File    : classification_txt_demo1.py
 @Note    : 
 
 """


import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import StringType,ArrayType
from pyspark.sql.functions import udf
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import jieba

spark = SparkSession\
        .builder\
        .appName("join data")\
        .getOrCreate()

url = "jdbc:mysql://10.20.5.49:3306/data_mining_db?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

table_name = "ztb_class_0716_train"
ds = spark.read.jdbc(url=url,table=table_name)
ds_1 = ds.filter(F.col("label") == "1")
ds_2 = ds.filter(F.col("label") == "2").sample(fraction=0.185,seed=123)

ds_3 = ds_1.union(ds_2).sample(fraction=0.3,seed=123)


"""
定义udf,把jieba分词包装起来,返回一个pyspark可识别的arraytype,array中的基元素是stringtype
"""
def seg(x):
    jieba_seg_generator = jieba.cut(x, cut_all=False)
    words = []
    for word in jieba_seg_generator:
        if len(word) > 1:
            words.append(word)
    return " ".join(words)


seg_udf = udf(seg, StringType())

ds_4 = ds_3.withColumn("text",seg_udf("title")).randomSplit([0.7,0.3],seed=123)
ds_train = ds_4[0]
ds_test = ds_4[1]

# ds_train.show()

tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures")
idfModel = IDF(inputCol=hashingTF.getOutputCol(), outputCol="features")

pipeline_tfidf = Pipeline(stages=[tokenizer,hashingTF,idfModel])


train_tfidf = pipeline_tfidf.fit(ds_train).transform(ds_train)
test_tfidf = pipeline_tfidf.fit(ds_train).transform(ds_test)

train_tfidf.printSchema()
print("+++++")
test_tfidf.printSchema()


labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(train_tfidf)
# featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4).fit(ds_tfidf)
# rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=10)
rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="features", numTrees=10)
labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

# pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
pipeline = Pipeline(stages=[labelIndexer, rf, labelConverter])

model = pipeline.fit(train_tfidf)

ds_pre = model.transform(test_tfidf)
print("+++++++++++++")
ds_pre.printSchema()

spark.stop()