#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

from datetime import datetime
a=datetime.now()

## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="gongdan",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)
table = "ml_info_item"
# sql语句
sqlcmd = "select * from ml_info_item"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)
# 取前5行数据
# df_not_null = df[df["OPEN_CONDITION"].isnull()]
df_not_null = df[df["COL_NAME"].isnull()]


# print(df_not_null)
# pd.io.sql.to_sql(df_not_null,'t1', dbconn, schema='gongdan',
#                  if_exists='replace')
# pd.io.sql.to_sql(df_not_null, "t1", dbconn, if_exists='replace', index=False, index_label=None)

# df_not_null.to_sql("dbo.test", con=conn, if_exists="append", index=False)
# df_not_null.to_sql('test_table', dbconn)

engine = create_engine("mysql+pymysql://root:root@localhost:3306/gongdan?charset=utf8")


df_not_null.to_sql(name = 'table_name',con = engine,if_exists = 'append',index = False,index_label = False)


b=datetime.now()

miao = (b-a).seconds #时间差的计算，单位为秒
print(miao)
# print("所需时间：" + miao + "秒")