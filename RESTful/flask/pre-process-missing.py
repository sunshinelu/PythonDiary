#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2018/10/10  11:15
@note：      big data pre processing
@include：   本脚本包含 {参数} 及 {方法} 说明
            参数：
            temp_table      临时表名
            option          预处理方法
            new_table       新表名
            constant        固定值传参
            方法：
            dele_data       删除
            donothing       不处理
            mean_data       均值
            median_data     中位数
            mode_data       众数
            fill_constant   固定值
"""
from __future__ import print_function

from flask import Flask, request
import pymysql
import pandas as pd
from sqlalchemy import create_engine

"""
    @ 缺失值处理：
    @ 方法：删除、不处理、插补[均值]、插补[中位数]、插补[众数]、插补[固定值]、插补[回归方法]
"""

def dele_data(self):

    # 过滤缺失数据
    drop_data = self.dropna()
    return drop_data

def donothing(self):

    # 插补[不处理]
    return self

def mean_data(self):

    # 插补均值
    fill_mean = self.fillna(self.mean())
    return fill_mean

def median_data(self):

    # 插补[中位数]
    # col_median = self.iloc[0:-1]
    fill_median = self.fillna(self.median())
    return fill_median

def mode_data(self):

    # 插补[众数]
    # col_mode = self.iloc[0:-1]
    fill_mode = self.fillna(self.mode())
    return fill_mode

def fill_constant(self,constant):

    # 插固定值
    fill_value = self.fillna(constant)
    return fill_value


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
    # 固定值参数
    constant = request.args.get('constant')

    print(temp_table, option, new_table, constant)

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

        # 实例化MissValue类
        # missvalue = MissValue()

        # 删除
        if option == 'dele_data':
            right_data = dele_data(data)
        # 不处理
        if option == 'donothing':
            right_data = donothing(data)
        # 均值
        if option == 'mean_data':
            right_data = mean_data(data)

        # 中位数
        if option == 'median_data':
            right_data = median_data(data)
        # 众数
        if option == 'mode_data':
            right_data = mode_data(data)
        # 固定值
        if option == 'fill_constant':
            right_data = fill_constant(data, constant)
        # 插值[回归]



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
    app.run(debug=False, port=8088)
    
