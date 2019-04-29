#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

from datetime import datetime

"""
需求：
无效数据、脏数据：ml_info_type表中type_desc字符数小于10的。

"""

# 获取当前时间
a=datetime.now()

# create the database connection:
conn_mysql = create_engine('mysql+pymysql://root:root@localhost:3306/gongdan?'
                           'charset=utf8')

# sql语句
sqlcmd = "select * from ml_info_type"

# read data to a pandas DataFrame from a SQL query:
df = pd.read_sql(sqlcmd, conn_mysql)

# 对指定列数据长度进行过滤
df_filter = df[df["TYPE_DESC"].apply(len) < 10]

# 将结果保存到mysql数据库
df_filter.to_sql(name = 'table_filter',con = conn_mysql,if_exists = 'replace',index = False,index_label = False)


# 获取当前时间
b=datetime.now()

#时间差的计算，单位为秒
miao = (b-a).seconds
print(miao) # 7秒
print("所需时间：" + str(miao) + "秒")
