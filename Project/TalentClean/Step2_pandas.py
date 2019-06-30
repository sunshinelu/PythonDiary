# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
import numpy as np
from sqlalchemy import create_engine

from datetime import datetime

import re
import numpy
import pandas
import constant
from sqlalchemy import create_engine


## 加上字符集参数，防止中文乱码
dbconn = pymysql.connect(
    host="localhost",  # 127.0.0.1
    database="talentscout",
    user="root",
    password="root",
    port=3306,
    charset='utf8'
)
# sql语句
# 性别
sex_sql = 'SELECT name,sort FROM `dict_new` where classify = "性别" or classify = "性别（数字）" ORDER BY sort'
# 利用pandas 模块导入mysql数据
dict_content = pd.read_sql(sex_sql, dbconn).drop_duplicates()

data_sql = "select * from sunlu_step1"
source_content = pd.read_sql(data_sql, dbconn)["sex"].drop_duplicates()

match=1.0
multi=False
match_symbol_regex = re.compile('[\s,，、]+')
def takeSecond(elem):
    return elem[2]

def get_field_similarity(target, source):
    """获取两个字段的相似度"""
    target = list(target)
    source = list(source)
    s1 = set(target)
    s2 = set(source)
    actual_jaccard = round(len(s1.intersection(s2)) / len(s1.union(s2)), 2)
    return actual_jaccard

def __to_standard(string, dicts, match=1, multi=False):
    """
    标准换到字典
    :param string: 需要进行标准化的内容
    :param dicts: 标准
    :param match:匹配度大于等于该值是不进行继续匹配
    :param multi 是否可通过分隔符来清洗，清洗完通过,拼接
    :return: 标准话之后的内容(匹配内容，匹配度，重要度)
    """
    # 查看是否存在多项 是否有,来分割
    strings = string.split('、')
    results = []
    for dict_str in strings:
        result_match_degree = 0
        result = None
        # print(string)
        for dict_item in dicts.values:
            # damerau_levenshtein = textdistance.damerau_levenshtein.normalized_similarity(dict_str, item[0])
            # jaro_winkler = textdistance.jaro_winkler.normalized_similarity(dict_str, item[0])
            # smith_waterman = textdistance.smith_waterman.normalized_similarity(dict_str, item[0])
            # average_match_degree = damerau_levenshtein * 0.65 + jaro_winkler * 0.25 + smith_waterman * 0.1
            # average_match_degree = Simhash(item[0]).hamming_distance(Simhash(dict_str))
            index = dict_str.find('$')
            if index != -1:
                dict_str = dict_str[:index]
            for item in dict_item[0].split(' '):  # 存在空格隔开多值情况
                average_match_degree = get_field_similarity(item, dict_str)
                # print(item[0] + ',' + dict_str + ":" + str(average_match_degree))
                if average_match_degree > result_match_degree:
                    result_match_degree = average_match_degree
                    result = (item, result_match_degree, dict_item[1])
                    # if result_match_degree >= match:
                    #    break
                    # print("result:" + result + ";" + str(result_match_degree))
        if result:
            results.append(result)

    if not results:
        # 没有匹配
        return None
    if multi:
        # 需要多值
        results = [t for t in set(_ for _ in results)]
        key = "、".join(list(map(lambda x: x[0], results)))
        value = "、".join(list(map(lambda x: str(x[1]), results)))
        return (key, value, 1)
    else:
        # 不需要多值
        results.sort(key=takeSecond)
        return (results[0][0], results[0][1], results[0][2])

def split_standard(string, dicts, match=1, multi=False):
    """
    替换分隔符进行标准化,将空格、替换为中文，
    :param string: 需要进行标准化的内容
    :param dicts: 标准
    :param multi 是否可通过分隔符来清洗，清洗完通过,拼接
    :return: 标准话之后的内容(原内容，匹配内容，匹配度，重要程度，值越小越重要)
    """
    if not string or string.strip() == '':
        return None
    # 替换
    string_after = re.sub(match_symbol_regex, "、", string).strip('、').strip()
    result = __to_standard(string_after, dicts, match, multi)
    index = string.find('$')
    if index != -1:
        index = index + 1
        string = string[index:]
    if not result:
        return (string, None, 0, 1)
    return (string, result[0], result[1], result[2])

result = source_content.map(lambda item: split_standard(item, dict_content, match, multi))

print(result)