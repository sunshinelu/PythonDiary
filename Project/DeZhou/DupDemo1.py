#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

from datetime import datetime
"""
需求：
重复数据：ml_info_type表中provider重复的数据展示出来。输出的是除去第一个之外剩下的全部重复数据。（2019/4/29更新）

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

# 对指定列数据获取重复数据
dup_index = df.duplicated("PROVIDER")
df_dup = df[dup_index]

"""
# 指定多列进行重复数据判断
s = "TYPE_NAME,PROVIDER"
l = s.split(",")
dup_index = df.duplicated(l)
df_dup = df[dup_index]
"""

# 将结果保存到mysql数据库
df_dup.to_sql(name = 'table_dup',con = conn_mysql,if_exists = 'replace',index = False,index_label = False)

# 获取当前时间
b=datetime.now()

#时间差的计算，单位为秒
miao = (b-a).seconds
print(miao) # 13秒
print("所需时间：" + str(miao) + "秒")
