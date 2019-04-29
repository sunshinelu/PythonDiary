#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np

import pandas.io.sql as psql
from sqlalchemy import create_engine

# import sys
# sys.setdefaultencoding('utf-8')

# connect mysql
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="localhost", # 127.0.0.1
  database="gongdan",
  user="root",
  password="root",
  port=3306,
  charset='utf8'
 )

# sql语句
sqlcmd = "select * from ml_info_type_copy"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd,dbconn)



engine_pg = create_engine(r'postgresql://postgres:root@localhost:5432/gongdan')

c = engine_pg.connect()
conn = c.connection

# df = psql.read_sql("SELECT * FROM xxx", con=conn)
# df.to_sql('a_schema.test', engine_pg)
df.to_sql("ml_info_type_copy", engine_pg, if_exists='replace', index=False)

conn.close()