# -*- coding: utf-8 -*-
"""
获取数据库中所有的表的名字，并将表名是以“ut_”开头的表过滤出来。

参考链接：
使用Python 读取数据库所有表名
https://my.oschina.net/hlstack/blog/1605166

python2.7 获取所有mysql数据库名称和表名称
https://www.cnblogs.com/songjiantong/p/10670642.html

Python中使用filter过滤列表的一个小技巧
https://blog.csdn.net/Jerry_1126/article/details/82827889

python简洁使用正则对列表元素进行筛选, 并生成新列表
https://blog.csdn.net/liaowhgg/article/details/86667938
"""
import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine
import re

## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="gongdan",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)

sqlcmd = "SHOW TABLES"
cursor = dbconn.cursor()
cursor.execute(sqlcmd)

# 获取所有表的名字
tables = cursor.fetchall()
t1 = list(tables)[1]

# 将表的名字提取出来
t2 = list()
for i in range(len(tables)):
    t2.append(tables[i][0])

print(list(tables))
print(t2)

# 对表名进行过滤
## 方法一：
t3 = filter(lambda s: s.startswith("ut_"), t2)
print(list(t3))
## 方法二：
t4 = list(filter(lambda x: re.match('ut_*', x) != None, t2))
print(t4)