# -*- coding: utf-8 -*-

"""
读取 csv 数据到mysql中

"""

import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine



df=pd.read_csv('/Users/sunlu/Workspaces/PyCharm/PythonDiary/data/daily-minimum-temperatures-in-me.csv',
               header=None,sep=',')


df.columns = ["time","value"]

print df[0:300]

print df.dtypes

# 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
yconnect = create_engine('mysql+pymysql://root:root@localhost:3306/data_mining_DB?charset=utf8')
pd.io.sql.to_sql(df, "daily_minimum_temperatures", yconnect, if_exists='replace', index=False, index_label=None)
