# -*- coding: utf-8 -*-

"""
计算短文本相似性。

"""

import os

from pyspark.ml.feature import HashingTF, IDF, Tokenizer, MinHashLSH
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.functions import lit, length,row_number
from pyspark.sql.types import StringType
from pyspark.sql.window import Window

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("similarity of short text")\
        .getOrCreate()

# Loading data from a JDBC source
ds1 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "rc_jbxx") \
    .option("user", "root") \
    .option("password", "root") \
    .load()\
    .select("address")\
    .dropna().dropDuplicates()\
    .withColumnRenamed("address", "text").withColumn("tag", lit("address"))\
    .sample(withReplacement=False, fraction=0.01, seed=3)

ds2 = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "district_dict") \
    .option("user", "root") \
    .option("password", "root") \
    .load()\
    .select("full_name").dropna().dropDuplicates()\
    .withColumnRenamed("full_name", "text").withColumn("tag", lit("full_name"))

ds = ds1.union(ds2)
# ds.show()

def seg_words(text):
    return  " ".join(list(text))

seg_words_udf = udf(seg_words, StringType())

ds_words = ds.withColumn("seg_words",seg_words_udf("text")).filter(length("seg_words") >= 3)
# tokenizer = Tokenizer().setInputCol("seg_words").setOutputCol("words")
tokenizer = Tokenizer(inputCol="seg_words", outputCol="words")
wordsData = tokenizer.transform(ds_words)

hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=20000)
featurizedData = hashingTF.transform(wordsData)

idf = IDF(inputCol="rawFeatures", outputCol="features")
idfModel = idf.fit(featurizedData)
rescaledData = idfModel.transform(featurizedData)

mh = MinHashLSH(inputCol="features", outputCol="hashes", numHashTables=5)
mh_model = mh.fit(rescaledData)

mh_data = mh_model.transform(rescaledData)

ds_address = mh_data.filter(col("tag") == "address")
ds_full_name = mh_data.filter(col("tag") == "full_name")

docsimi_mh = mh_model.approxSimilarityJoin(ds_address, ds_full_name, 1.0)

docsimi_mh.printSchema()

colRenamed = ["address", "full_name","distCol"]
mhSimiDF = docsimi_mh.select("datasetA.text", "datasetB.text", "distCol").toDF(*colRenamed)

# mhSimiDF.printSchema()
w = Window.partitionBy("address").orderBy(col("distCol").asc())
ds_simi = mhSimiDF.withColumn("rn", row_number().over(w)).where(col("rn") <= 1).drop("rn")

# ds_simi.show(20, truncate = False)

# Saving data to a JDBC source
ds_simi.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/gongdan?useUnicode=true&characterEncoding=UTF-8") \
    .option("dbtable", "simi_test") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()