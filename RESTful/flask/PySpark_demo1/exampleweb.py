# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

"""
参考链接：
Running Flask on Spark2
https://www.thegoldfish.org/2018/04/running-flask-on-spark2/

Flask on Spark example.

Run with:

    ./bin/spark-submit --master spark://$(hostname -s):7077 exampleweb.py

在win下以local模式运行：
spark-submit --master local exampleweb.py


And then access it at http://localhost:5000/ and http://localhost:5000/pi?partitions=1


问题解决：
Mac中默认的python版本是2.7，但是程序使用的python版本是3.6，如果是程序启动是使用的python版本是3.6？

修改spark-env.sh文件，新增
export PYSPARK_PYTHON=/Users/sunlu/anaconda2/envs/python36/lib/python3.6
export PYSPARK_DRIVER_PYTHON=/Users/sunlu/anaconda2/envs/python36/bin/python3.6

代码中增加：
import os
# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

问题参考链接：
1. Spark修改为python3.6.5
https://blog.csdn.net/a794922102/article/details/87107456

2. Python使用spark时出現版本不同的错误
https://blog.csdn.net/wmh13262227870/article/details/77992608

"""

import sys
sys.path.append( './python' )
from random import random
from operator import add

from flask import Flask, request
from pyspark.sql import SparkSession

import os
# os.environ["PYSPARK_PYTHON"]="/usr/bin/python3"
os.environ["PYSPARK_PYTHON"]="/Users/sunlu/anaconda2/envs/python36/bin/python3.6"

app = Flask(__name__)

spark = SparkSession\
        .builder\
        .appName("Flark - Flask on Spark")\
        .getOrCreate()

@app.route("/")
def hello():
    return "Hello World! There is a spark example at <a href=\"/pi?partitions=1\">/pi</a>"

@app.route("/pi")
def pi():

    try:
        partitions = int(request.args.get('partitions', '1'))
    except Exception as e:
        return e

    partitions = 4
    n = 1000000 * partitions


    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    return "Pi is roughly %f" % (4.0 * count / n)


if __name__ == "__main__":
    app.run()