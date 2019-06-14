import os

from flask import Flask
from flask import request
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import pyspark
import pyspark.sql
from pyspark.sql import SparkSession


app = Flask(__name__)

# Configure the environment
if 'SPARK_HOME' not in os.environ:
    os.environ['SPARK_HOME'] = '/Users/sunlu/Software/spark-2.0.2-bin-hadoop2.6'
 # Create a variable for our root path
SPARK_HOME = os.environ['SPARK_HOME']



def produce_pi(scale):
    # spark = SparkSession.builder.appName("PythonPi").getOrCreate()
    spark = SparkSession \
        .builder \
        .appName("PythonPi") \
        .getOrCreate()

    sc = spark.sparkContext
    n = 100000 * scale

    def f(_):
        from random import random
        x = random()
        y = random()
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    count = spark.sparkContext.parallelize(
        range(1, n + 1), scale).map(f).reduce(lambda x, y: x + y)
    spark.stop()
    pi = 4.0 * count / n
    return pi


@app.route("/")
def index():
    return "Python Flask SparkPi server running. Add the 'sparkpi' route to this URL to invoke the app."