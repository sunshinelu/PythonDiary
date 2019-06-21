#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2019/5/5  9:41
@note：      EvayAI Data Mining for data process
"""
import re
from math import isnan
import pandas as pd
from mysql_conn import *


# 数据预处理
def data_preprocess(input_sql, output_sql, temp_table, new_table, process, params):
    """
    :param temp_table: 数据表
    :param new_table: 结果表
    :param process:
    :param params:
    :return: df
    """
    preprocess_dict = {
        'data_null':
            {'save': nan_data_null,
             'drop': nan_dele_data,
             'mean_data': nan_mean_data,
             'mode_data': nan_mode_data,
             'constant': nan_fill_constant,
             'donothing': nan_donothing
             }
    }

    global data_prepro
    sql_df = input_sql.read_sql(temp_table)

    if process[0] in preprocess_dict.keys():
        data_prepro = preprocess_dict[process[0]][process[1]](sql_df, params)

    if isinstance(data_prepro, str):
        Code = -1  # 数据预处理成功，但结果为空
        return Code, data_prepro
    else:
        if output_sql.write_sql(new_table, data_prepro) is None:
            Code = 0
            data_prepro = 'write to %s success' % new_table
            return Code, data_prepro


# 保存空值
def nan_data_null(df, cols):
    """
    isnull output
    :return:
    """
    isnull = df[df[cols].isnull().values == True].drop_duplicates()

    return 'Null data is None' if isnull.empty else isnull


# 删除空值
def nan_dele_data(df, cols):
    # 过滤缺失数据
    drop_data = df.dropna(subset=cols)
    return 'All data is None' if drop_data.empty else drop_data


# 对空值填充均值
def nan_mean_data(df, cols):
    # 插补均值
    val = df[cols].mean()
    df[cols] = df[cols].fillna(val)
    return 'All data is None' if df.empty else df


# 对空值填充中位数
def nan_median_data(df, cols):
    # 插补[中位数]
    val = df[cols].median()
    df[cols] = df[cols].fillna(val)
    return 'All data is None' if df.empty else df


# 对空值填充众数
def nan_mode_data(df, cols):
    # 插补[众数]
    val = df[cols].mode().iloc[0]
    df[cols] = df[cols].fillna(val)
    return 'All data is None' if df.empty else df


# 对空值填充固定值
def nan_fill_constant(df, cols):
    # 插固定值
    df[cols[:-1]] = df[cols[:-1]].fillna(cols[-1])
    return 'All data is None' if df.empty else df


# 对空值不做处理
def nan_donothing(df, cols):
    # 插补[不处理]
    donoth = df
    return 'data do nothing' if donoth.empty else donoth

