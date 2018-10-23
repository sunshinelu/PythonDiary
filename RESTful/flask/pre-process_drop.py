#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2018/10/10  11:15
@note：      big data pre processing
@include：   缺失值、异常值......
"""
from __future__ import print_function

from flask import Flask, request
import MySQLdb
import pandas as pd
from sqlalchemy import create_engine

"""
    @ 缺失值处理：
    @ 方法：删除、不处理、插补[均值]、插补[均值]、插补[中位数]、插补[固定值]、插补[回归方法]
    """

def dele_data(self):

    # 过滤缺失数据
    drop_data = self.dropna()
    return drop_data

def median_data(self):

    # 插补均值
    describe = self.describe()
    # 逐个判定元素是否需要插值
    for i in self.columns:
        for j in range(len(self)):
            if (self[i].isnull())[j]:  # 如果为空即插值
                self[i][j] = describe.loc['50%']
    return self


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

    print(temp_table, option, new_table)

    # (1) 从临时表查询数据；(2) 调用option对应方法处理；(3) 写入正式表，并删除 temp_table
    # 打开数据库连接
    db = MySQLdb.connect(host='localhost', port=3316, user='root', passwd='root', db='data_mining_DB')
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

        if option == 'dele_data':
            right_data = dele_data(data)
        if option == 'median_data':
            right_data = median_data(data)

        # 将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
        yconnect = create_engine('mysql+mysqldb://root:root@localhost:3316/data_mining_DB?charset=utf8')
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
    
