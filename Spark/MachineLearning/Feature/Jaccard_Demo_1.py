# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/2 下午5:56 
 @File    : Jaccard_Demo_1.py
 @Note    : 
 参考链接：
 pyspark minHash LSH 查找相似度
 https://www.cnblogs.com/bonelee/p/10955307.html
 """

import os
import re
import hashlib

from pyspark import SparkContext, SparkConf
from pyspark import Row
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.functions import udf,collect_list, collect_set
from pyspark.ml.feature import MinHashLSH, BucketedRandomProjectionLSH
from pyspark.ml.linalg import Vectors, VectorUDT

# 控制spark服务启动
spark = SparkSession.builder.appName('app_name').getOrCreate()
spark.stop()
spark = SparkSession.builder.appName('app_name').getOrCreate()

class PySpark(object):
    @staticmethod
    def execute(df_input):
        """
        程序入口，需用户重载
        :return:必须返回一个DataFrame类型对象
        """
        # step 1：读入DataFrame
        df_mid = df_input.select('id','name','data','mat')
        # step 2：特征向量预处理
        def mat2vec(mat):
            """
            定义UDF函数，将特征矩阵向量化
            :return:返回相似度计算所需的VectorUDT类型
            """
            arr = [0.0]*len(mat)
            for i in range(len(mat)):
                if mat[i]!='0':
                    arr[i]=1.0
            return Vectors.dense(arr)

        udf_mat2vec = udf(mat2vec,VectorUDT())
        df_mid = df_mid.withColumn('vec', udf_mat2vec('mat')).select(
                                 'id','name','data','mat','vec')
        # step 3：计算相似度
        ## MinHashLSH，可用EuclideanDistance
        minlsh = MinHashLSH(inputCol="vec", outputCol="hashes", seed=123, numHashTables=3)
        model_minlsh = minlsh.fit(df_mid)
        ## BucketedRandomProjectionLSH
        brplsh = BucketedRandomProjectionLSH(inputCol="vec", outputCol="hashes",  seed=123, bucketLength=10.0, numHashTables=10)
        model_brplsh = brplsh.fit(df_mid)

        # step 4：计算（忽略自相似，最远距离限制0.8）
        ## model_brplsh类似，可用EuclideanDistance
        df_ret = model_minlsh.approxSimilarityJoin(df_mid, df_mid, 0.8, distCol='JaccardDistance').select(
                col("datasetA.id").alias("id"),
                col("datasetA.name").alias("name"),
                col("datasetA.data").alias("data"),
                col("datasetA.mat").alias("mat"),
                col("JaccardDistance").alias("distance"),
                col("datasetB.id").alias("ref_id"),
                col("datasetB.name").alias("ref_name"),
                col("datasetB.data").alias("ref_data"),
                col("datasetB.mat").alias("ref_mat")
            )#.filter("id=ref_id")
        return df_ret

df_in = spark.createDataFrame([
    (1001,"A","xxx","1010001000010000001001101010000"),
    (1002,"B","yyy","1110001000010000000011101010000"),
    (1003,"C","zzz","1101100101010111011101110111101")],
    ['id', 'name', 'data', 'mat'])
df_out = PySpark.execute(df_in)
df_out.show()
