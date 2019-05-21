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
# 取前5行数据
print(df)


df1 = df.dropna()


engine = create_engine("mysql+pymysql://root:root@localhost:3306/cnki?charset=utf8")


df1.to_sql(name = 'ID_card',con = engine,if_exists = 'append',index = False,index_label = False)
