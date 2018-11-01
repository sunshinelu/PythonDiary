# -*- coding: utf-8 -*-



import pandas as pd
from pyramid.arima import auto_arima

# For serialization:
from sklearn.externals import joblib
import pickle

# server & sql
from flask import Flask, request
import pymysql
from sqlalchemy import create_engine

data_path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/data/daily-minimum-temperatures-in-me.csv"
path = "/Users/sunlu/Workspaces/PyCharm/PythonDiary/results/"
pre_time = 12

"""
测试1. 将本地数据直接读取为Series类型
"""
print "测试1. 将本地数据直接读取为Series类型"

df_series = pd.Series.from_csv(data_path)
# print df_series.dtypes
print df_series

ts_fit_1 = auto_arima(df_series[0:500],start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise
print ts_fit_1.summary()


model_1 = "ts_model_1"
# save auto arima model
# Serialize with Pickle
with open(path + model_1, 'wb') as pkl:
    pickle.dump(ts_fit_1, pkl)


predict_data_1 = joblib.load(path + model_1).predict(n_periods=int(pre_time))
print predict_data_1


"""
测试2. 将本地数据读取为dataframe，再转化为Series类型
"""
print "测试2. 将本地数据读取为dataframe，再转化为Series类型"

df_csv = pd.read_csv(data_path,header=None,sep=',')
df_csv.columns = ["time","value"]
ts_local = pd.Series(df_csv['value'].values, index=df_csv['time'])

ts_fit_2 = auto_arima(ts_local[0:500],start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise
ts_fit_2.summary()

model_2 = "ts_model_2"
# save auto arima model
# Serialize with Pickle
with open(path + model_2, 'wb') as pkl:
    pickle.dump(ts_fit_2, pkl)

predict_data_2 = joblib.load(path + model_2).predict(n_periods=int(pre_time))
print predict_data_2

"""
测试3. 将mysql数据读取为dataframe，再转化为Series类型
"""
print "测试3. 将mysql数据读取为dataframe，再转化为Series类型"

## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
    host="localhost", # 127.0.0.1
    database="data_mining_DB",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
 )
# sql语句
sqlcmd = "select * from daily_minimum_temperatures"

# 利用pandas 模块导入mysql数据
df_mysql = pd.read_sql(sqlcmd, dbconn)
ts_mysql = pd.Series(df_mysql['value'].values, index=df_mysql['time'])

ts_fit_3 = auto_arima(ts_mysql[0:500],start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise
ts_fit_3.summary()

model_3 = "ts_model_3"
# save auto arima model
# Serialize with Pickle
with open(path + model_3, 'wb') as pkl:
    pickle.dump(ts_fit_3, pkl)

predict_data_3 = joblib.load(path + model_3).predict(n_periods=int(pre_time))
print predict_data_3


"""
结果保存
"""

print "结果保存"

predict_data_1 = pd.DataFrame(predict_data_1,columns=['Prediction'])
predict_data_2 = pd.DataFrame(predict_data_2,columns=['Prediction'])
predict_data_3 = pd.DataFrame(predict_data_3,columns=['Prediction'])

# 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
yconnect = create_engine('mysql+pymysql://root:root@localhost:3306/data_mining_DB?charset=utf8')
# pd.io.sql.to_sql(wineind, "daily_minimum_temperatures", yconnect, if_exists='overwrite', index=False, index_label=None)
pd.io.sql.to_sql(predict_data_1, "ts_demo1_pred_1", yconnect, if_exists='append', index=False, index_label=None)
pd.io.sql.to_sql(predict_data_2, "ts_demo1_pred_2", yconnect, if_exists='append', index=False, index_label=None)
pd.io.sql.to_sql(predict_data_3, "ts_demo1_pred_3", yconnect, if_exists='append', index=False, index_label=None)
