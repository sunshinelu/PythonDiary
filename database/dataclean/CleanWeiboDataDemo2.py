#-*- coding: UTF-8 -*-

"""
读取本地mysql微博数据进行数据清洗
并将结果保存到本地csv文件和mysql数据库中。

将结果保存到csv中运行成功。
将结果保存到mysql数据库中出现错误，原始数据的TEXT列无法存入数据库，目前尚未解决。

"""
import pandas as pd
import pymysql
import numpy as np
from lxml import etree
import re
import chardet
from sqlalchemy import create_engine

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# connect mysql
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="localhost", # 127.0.0.1
  database="text_summarization",
  user="root",
  password="root",
  port=3306,
  charset='utf8'
 )

# sql语句
sqlcmd = "select * from DA_WEIBO"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd,dbconn)

# get specific columns
columns = ["ID", "TEXT"]
df1 = df[columns]

# 计算TEXT列的长度
df1['text_length'] = df1['TEXT'].apply(len)
# 根据TEXT列的长度进行数据过滤
df1 = df1[df1.text_length > 10]

# 提取正文function
def xpathFunc(arg1):
    selector = etree.HTML(arg1.decode('utf-8'))
    html_data = selector.xpath('//text()')
    result = ""
    for i in html_data:
        result = result + i
    return result.encode('utf-8')

# 对TEXT列使用xpathFunc函数
df1['CONTENT'] = df1['TEXT'].apply(xpathFunc)

# 过滤CONTENT列中有'【'的行
df2 = df1[df1.CONTENT.str.contains('【')]

# print(df1.count())
# print(df2.count())
# print(df2[['TEXT','CONTENT']])
# print(df2['CONTENT'])

# 提取CONTENT中"中括号"里面的内容
def getTitle(x):
    s1 = re.findall(r"【(.{5,100})】", x)
    if len(s1) >= 1:
        s2 = s1[0].encode('utf-8')
    else:
        s2 = "".encode('utf-8')
    return s2
df2['TITLE'] = df2['CONTENT'].apply(lambda x: getTitle(x))
# print(df2['TITLE'].head())

"""
对CONTENT进行数据清洗:
【主题】
URL
//@用户名
@的用户
#话题#

"""
# print(df2[df2.CONTENT.str.contains("@")]['CONTENT'].head())


def cleanContent(x):
    s1 = re.sub(r"【(.*)】","",x) # 去除 【主题】
    s2 = re.sub(r"((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+", "", s1) # 去除URL
    s3 = re.sub(r"(@|//@)(.{3,40})(：|:| )", "", s2) # 去除//@用户名和@的用户
    s4 = re.sub(r"#[^#]+#", "", s3) # 去除#话题#
    s5 = re.sub(r"..全文", "", s4)  # 去除#话题#
    return s5.decode("utf-8", "replace").encode("utf-8")

df2['STR'] = df2['CONTENT'].apply(lambda x: cleanContent(x))
pd.set_option('display.max_rows', None)
# print(df2[['STR','CONTENT']].head())

# STR的长度进行过滤
df2['str_length'] = df2['STR'].apply(len)
df2 = df2[df2.str_length > 10]

df3 = df2[["ID","CONTENT","TITLE","STR"]] # 可以保存到mysql中

# df3 = df2[["ID", "TEXT","CONTENT","TITLE","STR"]] # 保存到mysql中报错，TEXT列有问题
# df3["TEXT"] = df3["TEXT"].apply(lambda x: x.encode("utf-8"))

# test_col = []
# text_col = df3['TEXT'].tolist()
# for i in text_col:
#     print(type(i))
#
# title_col = df3["TITLE"].tolist()
# print title_col
# for i in title_col:
#     print("CONTENT type is: " + type(i))


# 将清洗后数据保存到csv文件中
df3.to_csv('/Users/sunlu/Workspaces/PyCharm/PythonDiary/database/dataclean/cleanWeiboData.csv',
           encoding = 'utf-8',
           index = False)

"""
报错；
UnicodeDecodeError: 'utf8' codec can't decode byte 0xe8 in position 204: invalid continuation byte
参考链接；
https://stackoverflow.com/questions/12173255/utf8-codec-cant-decode-byte-0xd0-in-position-0-invalid-continuation-byte
解决方案：
s5.decode("utf-8", "replace").encode("utf-8")
"""


##将数据写入mysql的数据库，但需要先通过sqlalchemy.create_engine建立连接,且字符编码设置为utf8，否则有些latin字符不能处理
yconnect = create_engine('mysql+mysqldb://root:root@localhost:3306/text_summarization?'
                         'charset=utf8')
pd.io.sql.to_sql(df3,'tablename', yconnect, schema='text_summarization',
                 if_exists='replace')
