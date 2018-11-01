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

"""
测试1. 将本地数据直接读取为Series类型
"""
print "测试1. 将本地数据直接读取为Series类型"

df_series = pd.Series.from_csv(data_path,header=0)
# print df_series.dtypes
print df_series

print "－－－－－－－－"


# ts_fit_1 = auto_arima(df_series[0:500], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
#                       start_P=0, seasonal=True, n_jobs=-1, d=1, D=1, trace=True,
#                       error_action='ignore',  # don't want to know if an order does not work
#                       suppress_warnings=True,  # don't want convergence warnings
#                       stepwise=False, random=True, random_state=42,  # we can fit a random search (not exhaustive)
#                       n_fits=25)

ts_fit_1 = auto_arima(df_series[0:500], start_p=1, start_q=1, max_p=3, max_q=3, m=12,
                          start_P=0, seasonal=True, d=1, D=1, trace=True,
                          error_action='ignore',  # don't want to know if an order does not work
                          suppress_warnings=True,  # don't want convergence warnings
                          stepwise=True)  # set to stepwise

# ts_fit_1 = auto_arima(df_series[0:500], trace=True, error_action='ignore', suppress_warnings=True)
# ts_fit_1.fit(df_series)
ts_fit_1.summary()

print "－－－－－－－－"

model_1 = "ts_model_1"
# save auto arima model
# Serialize with Pickle
with open(path + model_1, 'wb') as pkl:
    pickle.dump(ts_fit_1, pkl)

print "－－－－－－－－"

pre_time = 12
predict_data_1 = joblib.load(path + model_1).predict(n_periods=int(pre_time))
print predict_data_1
