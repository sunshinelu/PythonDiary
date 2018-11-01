#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2018/10/23  15:24
@introduction：      本脚本包含 {参数} 及 {方法} 说明------>zScore 实现异常值预处理v1.0
            参数：
            temp_table      临时表名
            option          预处理方法
            new_table       新表名
            zscore_con          评分
            方法：
            dele_data       删除
            donothing       不处理
            miss_data       缺失值
            mean_data       均值
"""

from __future__ import print_function

from flask import Flask, request
import pymysql
import pandas as pd
from sqlalchemy import create_engine

"""
    @ 异常值处理：
    @ 方法：删除、不处理、视为缺失值、平均值修正
"""

def dele_data(df, zscore):
    # 删除异常值
    df[zscore] = None
    df_dele = df.dropna()
    return df_dele

def donothing(df):
    # 不处理
    return df

def miss_data(df, zscore):
    # 视为缺失值
    df[zscore] = None
    return df

def mean_data(df, zscore):
    # 平均值修正
    df_mean = df.fillna(df.mean())
    return df_mean

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
    # 评分
    zscore_con = request.args.get('zscore_con')

    print(temp_table, option, new_table, zscore_con)

    # (1) 从临时表查询数据；(2) 调用option对应方法处理；(3) 写入正式表，并删除 temp_table
    # for 144
    # db = pymysql.connect(host='172.16.10.144', port=3316, user='root', passwd='bigdata', db='test')

    # for local test
    db = pymysql.connect(
        host="localhost",  # 127.0.0.1
        database="data_mining_DB",
        user="root",
        password="123456",
        port=3306,
        charset='utf8'
    )
    cursor = db.cursor()
    # 查询数据
    sql_data = "select * from %s" % (temp_table)
    cursor.execute(sql_data)
    # 获取查询记录
    data = cursor.fetchall()
    # 提交到数据库执行
    db.commit()

    if len(data) != 0:
        data = list(data)
        data = [list(i) for i in data]
        data = pd.DataFrame(data)
        right_data = []

        # 采用zSore方法实现异常值预处理v1.0
        data_zscore = data.copy() # 用来存储Z-score得分的数据框
        cols = data.columns # 获取各列名
        # print(cols)
        for col in cols:
            data_col = data[col]
            z_score = (data_col - data_col.mean()) / data_col.std()  # 计算每列的Z-score得分
            data_zscore[col] = (z_score.abs() > float(zscore_con))

        print(data_zscore)
        # 删除
        if option == 'dele_data':
            right_data = dele_data(data, data_zscore)
        # 不处理
        if option == 'donothing':
            right_data = donothing(data)
        # 不处理
        if option == 'miss_data':
            right_data = miss_data(data, data_zscore)
        # 均值
        if option == 'mean_data':
            right_data = mean_data(data, data_zscore)

        # 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
        yconnect = create_engine('mysql+mysqldb://root:bigdata@172.16.10.144:3316/test?charset=utf8')
        pd.io.sql.to_sql(right_data, new_table, yconnect, if_exists='append', index=False, index_label=None)

        # 删除缓存表
        sql_table = "DROP TABLE %s" % (temp_table)
        # 执行 sql 语句
        cursor.execute(sql_table)
        # 提交到数据库执行
        db.commit()
        cursor.close()

        return 'success'


if __name__ == '__main__':
    app.run(debug=False, port=8089)


