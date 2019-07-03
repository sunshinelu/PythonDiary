#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     weihua gao
@Contact:    synes9@163.com
@Time:       2019/5/5  9:41
@note：      EvayAI Data Mining for data process
"""
import re
from math import isnan
import pandas as pd
import operator
from pandas import Series, DataFrame
from mysql_conn import *
from functools import reduce
import jieba
from datetime import datetime
import uuid
# 数据预处理
def data_preprocess(input_sql, output_sql, temp_table, new_table, process, time):
    """
    :param temp_table: 数据表
    :param new_table: 结果表
    :param process:
    :param params:
    :return: df
    """
    preprocess_dict = {
        'area_type': type_area,  #项目项目类型区域分布
        'person_type': type_person, #采购人项目类型分布
        'person_title': title_person, #词云图分析
        'social': social_relationship #社交关系分析
    }
    global data_prepro
    #to ensure start time not larger than end time
    if datetime.strptime(time[0], '%Y-%m-%d') > datetime.strptime(time[1], '%Y-%m-%d'):
        Code = -1
        data_prepro = "time is wrong"
        return Code, data_prepro

    sql_df = input_sql.read_sql(temp_table)  #read all data
    data_prepro = date_process(sql_df, time) #collect data within required time
    if process in preprocess_dict.keys(): #??如果不在呢
        data_final = preprocess_dict[process](data_prepro) #进行数据处理

    if isinstance(data_final, str):
        Code = -1  # 数据预处理成功，但结果为空
        return Code, data_final
    else:
        if output_sql.write_sql(new_table, data_final) is None:
            Code = 0
            data_final = 'write to %s success' % new_table
            return Code, data_final

#deal with date
def date_process(df, time):
    cols = "data"
    ts = pd.Series(df[cols].values.reshape(-1))
    ts = ts.str.replace('.', '-')
    ts = ts.str.replace(' ', '')
    ts = ts.str.slice(0, 10)
    df[cols] = ts.to_frame()
    df[cols] = df[cols].astype('datetime64')
    df = df[(df.data >= time[0])&(df.data<=time[1])]  #认为[开始时间,结束时间]
    return df


def type_area(df): #1
    ts = pd.Series(df['type'].values.reshape(-1)) #change type
    ts = ts.str.replace(' ', '') #delete space
    df['type'] = ts.to_frame()
    df = df.groupby(by=['provinces', 'type'], as_index=False).count() #count number
    df.rename(columns={'id': 'quantity'}, inplace=True)  #change name
    for index in range(0, df.shape[0]):
        df.ix[index, 'id'] = str(uuid.uuid4())  #add new id
    df['analyze_time'] = datetime.now()
    df['analyzer'] = 'WEIHUA GAO'
    df['delete_flag'] = None
    df['delete_time'] = None
    df = df.drop(df[(df['provinces'] == '')].index.tolist())
    #return df.loc[:, ['id','provinces', 'type', 'quantity', 'analyze_time', 'analyzer', 'delete_flag', 'delete_time']]
    return 'All data is None' if df.empty else df.loc[:, ['id', 'provinces', 'type', 'quantity', 'analyze_time',
                                                          'analyzer', 'delete_flag', 'delete_time']]

def type_person(df): #2
    #type has space
    ts = pd.Series(df['type'].values.reshape(-1))
    ts = ts.str.replace(' ', '')  # delete space
    df['type'] = ts.to_frame()

    ag = df.groupby(by=['agency', 'type'], as_index=False).count()
    ag.rename(columns={'id': 'quantity'}, inplace=True)  # change name
    ag.rename(columns={'agency': 'institutional_name'}, inplace=True)
    ag['institutional_type'] = 'agency'
    #ag = ag.drop(ag[(ag['institutional_name'] == '')].index.tolist())

    df = df.groupby(by=['purchaser', 'type'], as_index=False).count() #count number
    df.rename(columns={'id': 'quantity'}, inplace=True)  #change name
    df.rename(columns={'purchaser': 'institutional_name'}, inplace=True)
    df['institutional_type'] = 'purchaser'

    df = df.append(ag, ignore_index=True)

    reg = ".*[\u4E00-\u9FA5]+.*"
    for index in range(0, df.shape[0]):
        text = df.ix[index, 'institutional_name']
        match_obj = re.match(reg, str(text))  # check institutional_name
        if match_obj is None:
            df.drop([index], inplace=True)
    df.reset_index(drop=True, inplace=True)

    for index in range(0, df.shape[0]):
        df.ix[index, 'id'] = str(uuid.uuid4())  #add new id
    df['analyze_time'] = datetime.now()
    df['analyzer'] = 'WEIHUA GAO'
    df['delete_flag'] = None
    df['delete_time'] = None

   # return df.loc[:, ['id', 'institutional_type', 'institutional_name', 'type', 'quantity', 'analyze_time', 'analyzer'
                       #  , 'delete_flag', 'delete_time']]
    return 'All data is None' if df.empty else df.loc[:, ['id', 'institutional_type', 'institutional_name', 'type',
                                                          'quantity', 'analyze_time', 'analyzer', 'delete_flag', 'delete_time']]


def title_person(df): #3
    #过滤数据
    reg = ".*[\u4E00-\u9FA5]+.*"
    for index in range(0, df.shape[0]):
        text_1 = df.ix[index, 'purchaser']
        text_2 = df.ix[index, 'agency']
        match_obj1 = re.match(reg, str(text_1))  #check institutional_name
        match_obj2 = re.match(reg, str(text_2))  #check relevant_name
        if match_obj1 is None or match_obj2 is None:
            df.drop([index], inplace=True)
    df.reset_index(drop=True, inplace=True) #恢复index

    ag = df.groupby(by='purchaser', as_index=False).count()  #按照purchaser进行分组
    df = df.set_index('purchaser') #设为index
    final_1 = pd.DataFrame(columns=['word', 'count', 'institutional_name'])
    for index in range(0, ag.shape[0]):
        text = ''
        if isinstance(df.loc[ag.ix[index, 'purchaser'], 'title'], pd.Series):
            text_frame = df.loc[ag.ix[index, 'purchaser'], 'title'].to_frame()  # series转dataframe
            text_frame.reset_index(drop=True, inplace=True)
            for index1 in range(0, text_frame.shape[0]):
                text += text_frame['title'][index1]
        else:
            text = df.loc[ag.ix[index, 'purchaser'], 'title']
        words = jieba.cut(text, cut_all=True)
        segments = []
        for word in words:
            if word != "":  # 去除空格
                segments.append({'word': word, 'count': 1})
        qs = pd.DataFrame(segments)
        qs = qs.groupby(by='word', as_index=False).count()   #统计总数量
        qs['institutional_name'] = ag.ix[index, 'purchaser'] #purchaser的名字
        final_1 = final_1.append(qs, ignore_index=True)
    final_1['institutional_type'] = 'purchaser'

    ag = df.groupby(by='agency', as_index=False).count()     #按照agency进行分组
    df.reset_index(drop=True, inplace=True)
    df = df.set_index('agency')  # 原数据

    final_2 = pd.DataFrame(columns=['word', 'count', 'institutional_name'])
    for index in range(0, ag.shape[0]):
        text = ''
        if isinstance(df.loc[ag.ix[index, 'agency'], 'title'], pd.Series):
            text_frame = df.loc[ag.ix[index, 'agency'], 'title'].to_frame() #series转dataframe
            text_frame.reset_index(drop=True, inplace=True)
            for index1 in range(0, text_frame.shape[0]):
                text += text_frame['title'][index1]
        else:
            text = df.loc[ag.ix[index, 'agency'], 'title']
        words = jieba.cut(text, cut_all=True)
        segments = []
        for word in words:
            if word != "":  #去除空格
                segments.append({'word': word, 'count': 1})
        qs = pd.DataFrame(segments)
        qs = qs.groupby(by='word', as_index=False).count()
        qs['institutional_name'] = ag.ix[index, 'agency']  # agency的名字
        final_2 = final_2.append(qs, ignore_index=True)
    final_2['institutional_type'] = 'agency'

    final_1 = final_1.append(final_2, ignore_index=True)  #合并
    final_1.reset_index(drop=True, inplace=True)  # 恢复index
    for index in range(0, final_1.shape[0]):
        final_1.ix[index, 'id'] = str(uuid.uuid4())  # add new id
    final_1['analyze_time'] = datetime.now()
    final_1['analyzer'] = 'WEIHUA GAO'
    final_1['delete_flag'] = None
    final_1['delete_time'] = None

    #return final_1.loc[:, ['id', 'institutional_type', 'institutional_name', 'word', 'count', 'analyze_time',
                           #'analyzer', 'delete_flag', 'delete_time']]
    return 'All data is None' if final_1.empty else final_1.loc[:, ['id', 'institutional_type', 'institutional_name',
                                                                    'word', 'count', 'analyze_time', 'analyzer',
                                                                    'delete_flag', 'delete_time']]

def social_relationship(df): #4
    #已经存入test_04
    #正确性已经测试，drop已经测试正常
    ag = df.groupby(by=['purchaser', 'agency'], as_index=False).count()  #统计数量
    ag.rename(columns={'id': 'weight'}, inplace=True)  # change name
    ag.rename(columns={'purchaser': 'institutional_name'}, inplace=True)
    ag.rename(columns={'agency': 'relevant_name'}, inplace=True)
    ag['institutional_type'] = 'purchaser'
    ag['relevant_type'] = 'agency'

    df = df.groupby(by=['agency', 'purchaser'], as_index=False).count()  #统计数量
    df.rename(columns={'id': 'weight'}, inplace=True)  # change name
    df.rename(columns={'agency': 'institutional_name'}, inplace=True)
    df.rename(columns={'purchaser': 'relevant_name'}, inplace=True)
    df['institutional_type'] = 'agency'
    df['relevant_type'] = 'purchaser'
    df = df.append(ag, ignore_index=True)  #拼接表格

    #过滤数据
    reg = ".*[\u4E00-\u9FA5]+.*"
    for index in range(0, df.shape[0]):
        text_1 = df.ix[index, 'institutional_name']
        text_2 = df.ix[index, 'relevant_name']
        match_obj1 = re.match(reg, text_1)  #check institutional_name
        match_obj2 = re.match(reg, text_2)  #check relevant_name
        #print(match_obj)
        if match_obj1 is None or match_obj2 is None:
            df.drop([index], inplace=True)

    df.reset_index(drop=True, inplace=True) #drop之后index会乱，所以要重新从0开始排列
    for index in range(0, df.shape[0]):
        df.ix[index, 'id'] = str(uuid.uuid4())
    df['relationship'] = '合作关系'
    df['analyze_time'] = datetime.now()
    df['analyzer'] = 'WEIHUA GAO'
    df['delete_flag'] = None
    df['delete_time'] = None
    #return df.loc[:, ['id', 'institutional_type', 'institutional_name', 'relevant_type', 'relevant_name', 'weight',
                      #'relationship', 'analyze_time', 'analyzer', 'delete_flag', 'delete_time']]

    return 'All data is None' if df.empty else df.loc[:, ['id', 'institutional_type', 'institutional_name',
                                                          'relevant_type', 'relevant_name', 'weight','relationship',
                                                          'analyze_time', 'analyzer', 'delete_flag', 'delete_time']]
