#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from lxml import etree
import re
import chardet
import urllib.request
from lxml import etree
import re
import json
import time,datetime

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

#
# # connect mysql
# ## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="localhost", # 127.0.0.1
  database="cnki",
  user="root",
  password="root",
  port=3306,
  charset='utf8'
 )
# sql语句
sqlcmd = "select time from axlepress_pressure"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd,dbconn)[1:5]
df2 = pd.to_datetime(df["time"],unit="s")
print("============")
print(df2)
print("============")

# df3 = pd.to_datetime(df2["time"],unit="s").dt.strftime("%Y-%m-%d %H:%M")
# print("=====df3=======")
# print(df3)
# print("======df3======")

list1 = df["time"].values.tolist()
print("------",type(list1))
# print(df)
print("++++++++++++++++++")
print(time.mktime(time.strptime("2019-04-03 11:03:08","%Y-%m-%d %H:%M:%S")))

list2 = []
for i in list1:
    # time_local = time.localtime(i)
    # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    # dt1 = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # list2.append(dt1)
    print(i/1000000, type(i))

# doc_list1 = []
# for i in df.time.values.list:
#     time_local = time.localtime(i)
#     dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
#     dt1 = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
#     doc_list1.append(dt1)
# print("----",list(doc_list1))


#
# conn = pymysql.connect(
#         host='localhost',
#         port=3306,
#         user='root',
#         passwd='root',
#         db='coco'
#     )
#     #conn = sqlite3.connect('test@localhost')
# cursor = conn.cursor()
#
print(time.mktime(time.strptime("2018-08-07", "%Y-%m-%d")))

#
# a = cursor.execute(
#     'select time from axlepress_pressure')
# a1 = ((row[0].strftime("%Y-%m-%d %H:%M:%S")) for row in cursor.fetchall())
# print("-----------------------------xdata-------------------------------------")
# xdata = list(a1)
# print("-----------------------------xdata-------------------------------------")
# print("时间:", xdata)
# print(type(xdata[1]))
#
#
# # xdata = int(time.mktime(xdata))
# # xdata = time.mktime(time.strptime(xdata, "%Y-%m-%d %H:%M:%S"))
# L = []
# for x in xdata:
#     L.append(int(time.mktime(time.strptime(str(x), "%Y-%m-%d %H:%M:%S"))))
# print("-----------------------------L-------------------------------------")
# print("时间:", L)