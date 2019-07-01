# -*- coding: utf-8 -*-

"""
长宽表相互转换、或者透视表
参考链接：
Spark实现行列转换pivot和unpivot
https://juejin.im/post/5b1e343f518825137c1c6a27

"""
import os

from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window

from pyspark.sql import Window

# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

spark = SparkSession\
        .builder\
        .appName("pivot fnction demo")\
        .getOrCreate()

# 原始数据
df = spark.createDataFrame([('2018-01','项目1',100), ('2018-01','项目2',200), ('2018-01','项目3',300),
                            ('2018-02','项目1',1000), ('2018-02','项目2',2000), ('2018-03','项目x',999)
                           ], ['年月','项目','收入'])
df.show()

# 透视Pivot
df_pivot = df.groupBy('年月')\
                .pivot('项目', ['项目1','项目2','项目3','项目x'])\
                .agg(F.sum('收入'))\
                .fillna(0)
df_pivot.show()

# 逆透视Unpivot
df_unpivot = df_pivot.selectExpr("`年月`",
                    "stack(4, '项目1', `项目1`,'项目2', `项目2`, '项目3', `项目3`, '项目x', `项目x`) as (`项目`,`收入`)")\
            .filter("`收入` > 0 ")\
            .orderBy(["`年月`", "`项目`"])
df_unpivot.show()

spark.stop()