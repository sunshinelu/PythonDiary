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
             },
        'data_duplicate':
            {'save': data_duplicate,
             'drop': data_drop_duplicate
             },
        'data_invalid':
            {'contain': data_invalid_contain,
             'length': data_invalid_length,
             'number': data_invalid_number
             },
        're_data_filter':
            {'id_check': idCardcheck,
             'telephone_check': teleNumcheck,
             'email_check': emailCheck,
             'regex_check': regularCheck
             },
        'data_abnormal':
            {'drop': data_abnormal_drop,
             'mean_data': data_abnormal_mean,
             'miss_data': data_abnormal_missing,
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


# 保存重复值
def data_duplicate(df, cols):
    """
    All Duplicate data  output
    :return:
    """
    isduplicated = df[df[cols].duplicated(keep=False)]

    return 'Duplicate data is None' if isduplicated.empty else isduplicated


# 删除重复值
def data_drop_duplicate(df, cols):
    """
    All Duplicate data  output
    :return:
    """
    drop_duplicated = df.drop_duplicates(subset=cols)

    return 'Duplicate data is None' if drop_duplicated.empty else drop_duplicated


# 无效数据做包含过滤
def data_invalid_contain(df, cols):
    """
    :param df: data frame
    :param cols: columns
    :return: data frame
    """
    if cols[1] == 'in':
        # in
        f = lambda x: x.find(cols[-1]) >= 0
        # isinvalid = df[df[cols[0]].str.contains(cols[-1])]  # 单行代码速度最快，但是加到整体流程中，会增加0.5s和 find无差
        # isinvalid = df[df[cols[0]].str.match(cols[-1])]
        isinvalid = df[df[cols[0]].apply(f)]

    elif cols[1] == 'notin':
        # notin
        f = lambda x: x.find(cols[-1]) < 0
        # df[df["TYPE_DESC"].str.contains(cols[-1]) == False]
        # isinvalid = df[df[cols[0]].str.match(cols[-1]) == False]  # 同上
        isinvalid = df[df[cols[0]].apply(f)]
    elif cols[1] == 'equal':
        # f = lambda x: x.find(cols[-1]) == 0  # 字符长度太短，过滤结果不准
        isinvalid = df[df[cols[0]].isin([cols[-1]])]
        # isinvalid = df[df[cols[0]].apply(f)]

    # isinvalid = df[df[cols[0]].apply(f)]

    return 'Invalid data is None' if isinvalid.empty else isinvalid


# 无效数据做长度过滤
def data_invalid_length(df, cols):
    """
    :param df: data frame
    :param cols: columns
    :return: data frame
    """

    operator = 'len(x)' + cols[1] + cols[-1]
    f = lambda x: eval(operator)
    notnull = df[df[cols[0]].isnull().values == False].drop_duplicates()
    isinvalid = notnull[notnull[cols[0]].apply(f)]

    return 'Invalid data is None' if isinvalid.empty else isinvalid


# 无效数据做固定值过滤
def data_invalid_number(df, cols):
    """
    :param df: data frame
    :param cols: columns
    :return: data frame
    """

    # number < > != = <= >=
    operator = 'x' + cols[1] + cols[-1]
    f = lambda x: eval(operator)
    notnull = df[df[cols[0]].isnull().values == False].drop_duplicates()
    isinvalid = notnull[notnull[cols[0]].apply(f)]

    return 'Invalid data is None' if isinvalid.empty else isinvalid


# 身份证校验
def idCardcheck(df, cols):
    """
    身份证校验
    :param df:
    :param cols:
    :return:
    """
    id_check = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"
    if cols[1] == 'check_true':
        isinvalid = df[df[cols[0]].str.contains(id_check, regex=True) == True]
    elif cols[1] == 'check_false':
        isinvalid = df[df[cols[0]].str.contains(id_check, regex=True) == False]

    return 'id check is None' if isinvalid.empty else isinvalid


# 电话号码校验
def teleNumcheck(df, cols):
    """
    电话号码校验
    :param df:
    :param cols:
    :return:
    """
    telenum_re = r"^1[3456789]\d{9}$"
    if cols[1] == 'check_true':
        isinvalid = df[df[cols[0]].str.contains(telenum_re, regex=True) == True]
    elif cols[1] == 'check_false':
        isinvalid = df[df[cols[0]].str.contains(telenum_re, regex=True) == False]

    return 'mobile phone check is None' if isinvalid.empty else isinvalid


# email校验
def emailCheck(df, cols):
    """
    邮箱校验
    :param df:
    :param cols:
    :return:
    """
    email_re = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'
    if cols[1] == 'check_true':
        isinvalid = df[df[cols[0]].str.contains(email_re, regex=True) == True]
    elif cols[1] == 'check_false':
        isinvalid = df[df[cols[0]].str.contains(email_re, regex=True) == False]

    return 'email data check is None' if isinvalid.empty else isinvalid


# 输入正则校验
def regularCheck(df, cols):
    """
    输入正则表达式校验
    :param df:
    :param cols:
    :return:
    """
    if cols[1] == 'check_true':
        isinvalid = df[df[cols[0]].str.contains(cols[2], regex=True) == True]
    elif cols[1] == 'check_false':
        isinvalid = df[df[cols[0]].str.contains(cols[2], regex=True) == False]

    return 'regex check is None' if isinvalid.empty else isinvalid


# 异常值
def z_score(df, cols):
    """
    z score 异常值处理
    :param df:
    :param cols:
    :return:
    """
    df_zscore = df[cols[:-1]].copy()  # 存储Z-score得分的数据框
    for col in cols[:-1]:
        zscore = (df[col] - df[col].mean()) / df[col].std()  # 计算每列的Z-score得分
        df_zscore[col] = (zscore.abs() > float(cols[-1]))

    return df_zscore


# 删除异常值
def data_abnormal_drop(df, cols):
    """
    :param df:
    :param cols:
    :return:
    """
    df_zscore = z_score(df, cols)

    df[df_zscore] = None
    df_drop = df.dropna()
    return 'All data is None' if df_drop.empty else df_drop


# 不处理异常值
def data_abnormal_donothing(df, cols):
    """
    :param df:
    :param cols:
    :return:
    """
    return 'All data is None' if df.empty else df


# 异常值视为缺失值
def data_abnormal_missing(df, cols):
    """
    :param df:
    :param cols:
    :return:
    """
    df_zscore = z_score(df, cols)
    df[df_zscore] = None
    return 'All data is None' if df.empty else df


# 异常值视为平均值
def data_abnormal_mean(df, cols):
    """
    :param df:
    :param cols:
    :return:
    """
    df_zscore = z_score(df, cols)
    df[df_zscore] = df[cols[:-1]].mean().iloc[0]

    return 'All data is None' if df.empty else df

