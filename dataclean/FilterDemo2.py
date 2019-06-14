#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine




## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="cnki",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)
table = "rc_jbxx_20190301"
# sql语句
sqlcmd = "select * from rc_jbxx_20190301"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)

df1 = df[df["email"].isin([''])]

df2 = df1[df1["email"].notnull()][["email"]]
print(df2.count())

df2 = df1[df1["email"].isnull().values == False][["email"]]
print(df2.count())

df2 = df1[df1["email"].isnull().values == True][["email"]]
print(df2.count())

df2 = df1[["email"]].dropna()

# print(df2)
print(df2.count())

# str=r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
#
# df3 = df[df.filter(regex=(str))]
# print(df3)