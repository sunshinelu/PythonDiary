#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql



"""
人工打标签数据存放数据库访问地址
host：192.168.37.104
数据库：IngloryBDP
用户名：root
密码：root
端口号：33333
原始数据表名：DA_SEED_年月（例如,DA_SEED_201808）
打标签结果表：DA_ZTB_LABEL中，其中，1表示信息化，2表示非信息化。
打标签程序访问地址为：
http://10.20.5.116:8080/label
"""

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# connect mysql
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="192.168.37.104", # 127.0.0.1
  database="IngloryBDP",
  user="root",
  password="root",
  port=33333,
  charset='utf8'
 )

# sql语句
sqlcmd = "select * from DA_ZTB_LABEL"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd,dbconn)

print(df.head(5))