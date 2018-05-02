#-*- coding: UTF-8 -*-

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode
from pyspark.sql.functions import col,desc
"""
python word_count_demo_df_1.py 运行成功
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""
解决以下报错：
UnicodeEncodeError: 'ascii' codec can't encode character u'\u4eca' in position 0: ordinal not in range(128)
"""

spark = SparkSession \
    .builder \
    .appName("word_count_df") \
    .getOrCreate()

sc = spark.sparkContext

inp1 = "/home/lufeng/software/models/traintextsum/data/weibo/DA_WEIBO_2018_000.txt"
otp = "/home/lufeng/software/models/traintextsum/data/weibo/DA_WEIBO_word_count.txt"


text_rdd = sc.textFile(inp1).map(lambda x: (x, ))
df1 = text_rdd.toDF(["txt"])
df2 = df1.select("txt", explode(split(col("txt"), "\s+")).alias("word"))

word_count = df2.groupBy('word').count().orderBy(desc("count"))#.filter(col("count") >= 3)


word_count.coalesce(1).toPandas().to_csv(otp,sep=' ',
                             index=False,header=False)