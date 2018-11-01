# -*- coding: utf-8 -*-

from __future__ import print_function
import pandas as pd
from pyramid.arima import auto_arima

# For serialization:
from sklearn.externals import joblib
import pickle

# server & sql
from flask import Flask, request
import pymysql
from sqlalchemy import create_engine


def fit_tsa(df, path, model, maxp, maxq):
    # fitting a stepwise model:
    print(df)
    stepwise_fit = auto_arima(df, start_p=1, start_q=1, max_p=int(maxp), max_q=int(maxq), m=12,
                              start_P=0, seasonal=True, d=1, D=1, trace=True,
                              error_action='ignore',  # don't want to know if an order does not work
                              suppress_warnings=True,  # don't want convergence warnings
                              stepwise=True)  # set to stepwise

    stepwise_fit.summary()

    # save auto arima model
    # Serialize with Pickle
    with open(path + model, 'wb') as pkl:
        pickle.dump(stepwise_fit, pkl)


def load_model(model, path, pre_time):
    # load model & predict
    joblib_preds = joblib.load(path + model).predict(n_periods=int(pre_time))
    return joblib_preds


"""
 @ flask server connect with mysql
 @ note:
"""
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])

def get():
    # 传入临时表名
    temp_table = request.args.get("temp_table")
    # 处理方法
    option = request.args.get("option")
    # 写入表名
    new_table = request.args.get('new_table')
    # path
    path = request.args.get('path')
    # model name
    model = request.args.get('model')
    # max_p
    max_p = request.args.get('max_p')
    # max_q
    max_q = request.args.get('max_q')
    # predict_times
    pre_time = request.args.get('pre_time')

    print(temp_table, option, path, model, max_p, max_q, pre_time)

    # (1) 从临时表查询数据；(2) 调用option对应方法处理；(3) 写入正式表，并删除 temp_table
    # for 144
    # db = pymysql.connect(host='172.16.10.144', port=3316, user='root', passwd='bigdata', db='test')

    # for local test
    db = pymysql.connect(
        host="localhost",  # 127.0.0.1
        database="data_mining_DB",
        user="root",
        password="root",
        port=3306,
        charset='utf8'
    )
    # 查询数据
    sql_data = "select * from %s" % (temp_table)

    data = pd.read_sql(sql_data, db)
    test = pd.Series(data['value'].values, index=data['time'])

    if len(data) != 0:
        predict_data = []

        if option == 'all_flow':
            fit_tsa(test, path, model, max_p, max_p)
            predict_data = pd.DataFrame(load_model(model, path, int(pre_time)))
            print(type(predict_data))
            # to mysql
            yconnect = create_engine('mysql+pymysql://root:root@localhost:3306/data_mining_DB?charset=utf8')
            pd.io.sql.to_sql(predict_data, new_table, yconnect, if_exists='append', index=False, index_label=None)

        if option == 'fit_tsa':
            fit_tsa(test, path, model, max_p, max_p)
        # 不处理
        if option == 'load_model':
            predict_data = pd.DataFrame(load_model(model, path, int(pre_time)))
            print(type(predict_data))
           # to mysql
            yconnect = create_engine('mysql+pymysql://root:root@localhost:3306/data_mining_DB?charset=utf8')
            pd.io.sql.to_sql(predict_data, new_table, yconnect, if_exists='append', index=False, index_label=None)

        cursor = db.cursor()
        # 删除缓存表
        # sql_table = "DROP TABLE %s" % (temp_table)
        # 执行 sql 语句
        # cursor.execute(sql_table)
        # 提交到数据库执行
        db.commit()
        cursor.close()

        return 'success'


if __name__ == '__main__':
    app.run(debug=False, port=8090)