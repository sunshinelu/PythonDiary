# -*- coding: utf-8 -*-


"""
作者：孙露
时间：2018年10月16日
功能描述：
读取本地mysql中的data_mining_DB数据库中的data_statistics表，另存为data_statistics_temp表

"""
import pymysql
import pandas as pd
from sqlalchemy import create_engine

# 打开数据库连接
## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="data_mining_DB",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)

# sql语句
sqlcmd = "select * from data_statistics"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd, dbconn)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = dbconn.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS data_statistics_temp")
cursor.execute("DROP TABLE IF EXISTS data_statistics_result")
# 关闭数据库连接
dbconn.close()

yconnect = create_engine('mysql+mysqldb://root:root@localhost:3306/data_mining_DB?charset=utf8')
pd.io.sql.to_sql(df, "data_statistics_temp", yconnect, if_exists='append', index=False, index_label=None)
