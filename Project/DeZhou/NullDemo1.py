#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime

"""
需求
空数据：
ml_info_type表中table_name为空的，将table_name字段为空值的全部数据保存出来。（2019/4/29更新）
ml_info_item表里open_condition字段为空或null的，将open_condition字段为空值的全部数据保存出来。（2019/4/29更新）

"""

# 获取当前时间
a=datetime.now()

# create the database connection:
conn_mysql = create_engine('mysql+pymysql://root:root@localhost:3306/gongdan?'
                           'charset=utf8')

# sql语句
sqlcmd = "select * from ml_info_item"

# read data to a pandas DataFrame from a SQL query:
df = pd.read_sql(sqlcmd, conn_mysql)

# 获取制定列数据为空的数据
df_not_null = df[df["COL_NAME"].isnull()]

"""
# 获取指定多列进行任意为空数据
s = "COL_NAME,ITEM_NAME"
l = s.split(",")
df_not_null = df[df[l].isnull().values == True]
"""

# 将结果保存到mysql数据库
df_not_null.to_sql(name = 'table_null',con = conn_mysql,if_exists = 'replace',index = False,index_label = False)

# 获取当前时间
b=datetime.now()

#时间差的计算，单位为秒
miao = (b-a).seconds
print(miao) # 49 秒
print("所需时间：" + str(miao) + "秒")
