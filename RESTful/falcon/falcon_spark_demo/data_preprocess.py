# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/9 下午1:03
 @File    : data_preprocess.py
 @Note    : 
 
 """

from MySQL_conn import *
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from functools import reduce

# 数据预处理
def data_preprocess(ipt_db_type, opt_db_type, temp_table, new_table, process, params):
    """
    :param temp_table: 数据表
    :param new_table: 结果表
    :param process:
    :param params:
    :return: df
    """
    preprocess_dict = {
        'data_null':
            {#'save': nan_data_null,
             'drop': nan_dele_data,
             #'mean_data': nan_mean_data,
             # 'mode_data': nan_mode_data,
             'constant': nan_fill_constant,
             'donothing': nan_donothing
             }
    }

    global data_prepro
    df = ipt_db_type.read_sql(temp_table)

    if process[0] in preprocess_dict.keys():
        data_prepro = preprocess_dict[process[0]][process[1]](df, params)

    if isinstance(data_prepro, str):
        Code = -1  # 数据预处理报错
        return Code, data_prepro
    else:
        if opt_db_type.write_sql(new_table, data_prepro) is None:
            Code = 0
            data_prepro = 'write to %s success' % new_table
            return Code, data_prepro


# 缺失值处理：删除空值 √
def nan_dele_data(df, cols):
    # 过滤缺失数据
    try:
        drop_data = df.na.drop(subset=cols)
        return drop_data
    except Exception as e:
        return str(e)

# 缺失值处理：不做任何处理 √
def nan_donothing(df,cols):
    try:
        donothing_data = df
        return donothing_data
    except Exception as e:
        return str(e)

# 缺失值处理：缺失值填补常量 √
def nan_fill_constant(df,cols):
    try:
        fill_na_data = df.na.fill(cols[-1], subset=cols[:-1])
        return fill_na_data
    except Exception as e:
        return str(e)

