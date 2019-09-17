# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/17 上午10:43 
 @File    : read_sql_demo1.py
 @Note    : 

 使用sql
 """



import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine




## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="10.20.5.114",  # 127.0.0.1
    database="IngloryBDP",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)

# sql语句
sqlcmd = """
SELECT a.SEED_ID,a.SEED_TITLE,a.SEED_CONTENT,a.SEED_DATE,d.WEBSITE_NAME,a.SEED_URL
from DA_SEED_201909 a 
left join DA_TASK b on a.TASK_ID=b.TASK_ID
left join DA_WEBSITE_COLUMN c on b.SEED_URL=c.COLUMN_ID
left join DA_WEBSITE d on c.WEBSITE_ID=d.WEBSITE_ID
WHERE  a.MANUALLABEL='人才'
and d.WEBSITE_NAME = '中国科学院学部'
ORDER BY SEED_TITLE
"""

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)
# 取前5行数据
print(df)


df1 = df.dropna()


engine = create_engine("mysql+pymysql://root:root@localhost:3306/rencai?charset=utf8")

print(df1.count())

df1.to_sql(name = 'gongchengyuanshi',con = engine,if_exists = 'replace',index = False,index_label = False)
