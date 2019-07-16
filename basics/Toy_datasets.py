# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午4:16 
 @File    : Toy_datasets.py
 @Note    : 
 
 """

import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用


from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import StringType,ArrayType
import jieba

spark = SparkSession\
        .builder\
        .appName("read csv")\
        .getOrCreate()

import pandas as pd
from sklearn.datasets import load_linnerud,load_boston
linnerud = load_boston()

df = linnerud.data

df_label = linnerud.target

# print(linnerud)

# print(df)


# print(df_label)

# print(type(df))

# print(type(df_label))

df1 = pd.DataFrame(linnerud.data,columns=linnerud.feature_names)
# print(df1)
#
# print(df1.columns)
#
# print(len(linnerud.target))
#
# print(df1.columns.size)
#
# print(len(df1))

df1["MEDV"] = linnerud.target

# print(df1.columns)

# pandas dataframe 转spark dataset
df2 = spark.createDataFrame(df1).randomSplit([0.7,0.3],seed=56)

# df2.show()

url = "jdbc:mysql://10.20.5.49:3306/rgznpt_sjy?useUnicode=true&characterEncoding=UTF-8&user=root&password=BigData@2018"

df2[0].write.jdbc(url = url, table= "ml_regression_boston_train",mode="overwrite")
df2[1].write.jdbc(url = url, table= "ml_regression_boston_test",mode="overwrite")