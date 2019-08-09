# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/6 下午2:40 
 @File    : MySQL_conn.py
 @Note    : 
 
 """


from pyspark.sql import SparkSession
import os
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6" #在Mac中使用

class MySQL(object):
    """

    """

    def __init__(self, username, password, host, database):
        # self.username = username
        # self.password = password
        # self.host = host
        # self.database = database

        self.spark = SparkSession \
            .builder \
            .appName("Falcon - Falcon on Spark") \
            .getOrCreate()
        self.url = "jdbc:mysql://" + str(host) + "/" + str(database) + \
        "?useUnicode=true&characterEncoding=UTF-8&user="+ str(username) + "&password=" + str(password)

    def read_sql(self, temp_table):
        try:
            ds = self.spark.read.jdbc(url=self.url,
                                      table=temp_table,
                                      properties={"driver": 'com.mysql.jdbc.Driver'})
            print("read table " + temp_table)
            return ds
        except Exception as e:
            return str(e)

    def write_sql(self, new_table, ds):
        try:
            save_data = ds.write.jdbc(mode="overwrite", url=self.url, table=new_table,
                       properties={"driver": 'com.mysql.jdbc.Driver'})
            print("write to new_table success:" + new_table)
            self.spark.stop()
            return save_data
        except Exception as e:
            return str(e)


