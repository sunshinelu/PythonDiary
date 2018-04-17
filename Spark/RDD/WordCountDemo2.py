#-*- coding: UTF-8 -*-

from pyspark import SparkContext
from pyspark import SparkConf
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession

import sys
reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()

master= "local"
spark = SparkSession.builder\
    .appName("WordCountDemo2")\
    .master(master)\
    .getOrCreate()

sc = spark.sparkContext

# x = sc.parallelize([("a", 1), ("b", 4),("c", 3),("d", 2)])
# print x.count()
text_file = sc.textFile("file:///Users/sunlu/Workspaces/PyCharm/Github/pythonDemo/SparkDemo/wordCountDemo2.txt")
print text_file.count()
def splitChar(x):
    result = ""
    for i in x:
        result = result + " " + i
    return result
wordCounts = text_file.map(lambda x: splitChar(x)).flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
def is_str(s):
    return isinstance(s, basestring)

# wordCounts2 = wordCounts.filter(lambda x: x[1] >= 3).map(lambda x: [x[0].encode('unicode_escape').decode('gbk'), x[1]])
#
# wordCounts2 = wordCounts.filter(lambda x: x[1] >= 3).map(lambda x: [x[0].encode('gbk'), x[1]])
# print wordCounts2.collect()
# print wordCounts2.first()
# wordCounts2 = wordCounts.filter(lambda x: x[1] >= 3).map(lambda x: [x[0].encode('gbk').decode('utf-8'), x[1]])
wordCounts2 = wordCounts.filter(lambda x: x[1] >= 3).map(lambda x: [x[0].encode('utf-8'), x[1]])

# typelist = wordCounts.filter(lambda x: x[1] >= 3).map(lambda x: [type(x[0]), x[1]])
# print typelist.collect()

# print text_file.collect()

print wordCounts2.collect()


def f(x):
    print(x[0] + " " + str(x[1]))

wordCounts2.foreach(f)

# wordCounts2.saveAsTextFile("file:///Users/sunlu/Workspaces/PyCharm/PythonDiary/results/wordCountDemo2_result_5")