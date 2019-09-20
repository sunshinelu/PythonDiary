# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/19 下午2:48 
 @File    : to_Json_demo1.py
 @Note    : 
 
 """

from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

data = [
    ('one', 1, 10),
    (None, 2, 20),
    ('three', None, 30),
    (None, None, 40)
]

sdf = spark.createDataFrame(data, ["A", "B", "C"])
sdf.printSchema()

from pyspark.sql.functions import col, to_json, struct, when, lit

sdf.withColumn("JSON", to_json(struct(
    [when(
        col(x).isNotNull(), col(x)).otherwise(lit("")).alias(x)
     for x in sdf.columns
     ]))).show(truncate=False)
"""
+-----+----+---+-----------------------------+
|A    |B   |C  |JSON                         |
+-----+----+---+-----------------------------+
|one  |1   |10 |{"A":"one","B":"1","C":"10"} |
|null |2   |20 |{"A":"","B":"2","C":"20"}    |
|three|null|30 |{"A":"three","B":"","C":"30"}|
|null |null|40 |{"A":"","B":"","C":"40"}     |
+-----+----+---+-----------------------------+
"""

sdf.withColumn("JSON", to_json(struct(
    [when(
        col(x).isNotNull(), col(x)).otherwise(lit(None)).alias(x)
     for x in sdf.columns
     ]))).show(truncate=False)
"""
+-----+----+---+------------------------+
|A    |B   |C  |JSON                    |
+-----+----+---+------------------------+
|one  |1   |10 |{"A":"one","B":1,"C":10}|
|null |2   |20 |{"B":2,"C":20}          |
|three|null|30 |{"A":"three","C":30}    |
|null |null|40 |{"C":40}                |
+-----+----+---+------------------------+
"""

from pyspark.sql.functions import coalesce

sdf.withColumn("JSON", to_json(struct(
       [coalesce(col(x), lit("")).alias(x) for x in sdf.columns]
    )
)
).show(truncate=False)
"""
+-----+----+---+-----------------------------+
|A    |B   |C  |JSON                         |
+-----+----+---+-----------------------------+
|one  |1   |10 |{"A":"one","B":"1","C":"10"} |
|null |2   |20 |{"A":"","B":"2","C":"20"}    |
|three|null|30 |{"A":"three","B":"","C":"30"}|
|null |null|40 |{"A":"","B":"","C":"40"}     |
+-----+----+---+-----------------------------+

"""


sdf.withColumn("JSON", to_json(struct(
       [coalesce(col(x), lit(None)).alias(x) for x in sdf.columns]
    )
)
).show(truncate=False)
"""
+-----+----+---+------------------------+
|A    |B   |C  |JSON                    |
+-----+----+---+------------------------+
|one  |1   |10 |{"A":"one","B":1,"C":10}|
|null |2   |20 |{"B":2,"C":20}          |
|three|null|30 |{"A":"three","C":30}    |
|null |null|40 |{"C":40}                |
+-----+----+---+------------------------+
"""