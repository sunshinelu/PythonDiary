#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2019/5/6  11:49
@note：      connection mysql | shengtong sql | ......
"""
import pandas as pd

# mysql
from sqlalchemy import create_engine


class Mysql(object):
    """
    mysql database read and write
    url['username']:username
    url['password']:password
    url['host']:host
    url['database']:database
    """

    def __init__(self, username, password, host, database):

        mysql_db = 'mysql+pymysql://' + str(username) + ':' + str(password) + '@' \
             + str(host) + '/' + str(database) + '?charset=utf8'
        self.sql_conn = create_engine(mysql_db, echo=False)

    def read_sql(self, temp_table):

        sql = "select * from %s" % temp_table
        sql_df = pd.read_sql(sql, self.sql_conn)
        print('read sql success: ' + sql)
        return "%s is null" % temp_table if sql_df.empty else sql_df

    def write_sql(self, new_table, df):
        sql_df = pd.DataFrame(df)
        sql_result = sql_df.to_sql(new_table, self.sql_conn, if_exists='replace', index=False)
        print("write to new_table success:" + new_table)
        return sql_result

    def drop_table(self, temp_table):
        print('drop table beginning ......')
        sql = "DROP TABLE %s" % temp_table
        self.sql_conn.execute(sql)
        return True

