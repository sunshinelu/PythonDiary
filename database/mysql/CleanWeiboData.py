#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from lxml import etree
import re
import chardet

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
print df1.count()

df1['text_length'] = df1['TEXT'].apply(len)

df1 = df1[df1.text_length > 10]
print df1.count()

# 提取正文
def xpathFunc(arg1):
    selector = etree.HTML(arg1.decode('utf-8'))
    html_data = selector.xpath('//text()')
    result = ""
    for i in html_data:
        result = result + i
    return result.encode('utf-8')
#
# df2 = df1[1:100]
# col_text = df2["TEXT"].tolist()
# col_content = []
# for i in col_text:
#     s = xpathFunc(i.encode("utf-8"))
#     col_content = col_content + [s]
#
# df2["content"] = col_content
# df2.head()


col_test = df1['TEXT']
col_test2 = []
for i in col_test:
    s = i#.encoder('utf-8')
    col_test2 = col_test2 + [s]

# print df1.ix[320:322]

# j = 1
# for i in col_test2:
#     s = xpathFunc(i)
#     print s
#     print j
#     j += 1

col_content = []
for i in col_test2:
    s = xpathFunc(i)
    col_content = col_content + [s]

df1['CONTENT'] = col_content

print df1.head(5)
print df1.describe()

print "======="
df2 = df1[df1.CONTENT.str.contains(u'\u3010')]
print df2['CONTENT'].head(5)

print "======="

print "++++++++++"
df2 = df1[df1.CONTENT.str.contains('【')]
print df2['CONTENT'].head(5)

print "++++++++++"

# df2 = df1[df1.TEXT.str.contains("福建")]
print df2.count()

# check strings' coder for each string in list
# for x in col_content:
#     fencoding = chardet.detect(x)
#     print fencoding

for x in col_content:
    # print(type(x))
    s1 = re.findall(r"【(.*)】", x)
    s2 = ""
    for i in s1:
        s2 = s2 + i.encode('utf-8')
    # s2 = re.sub(s1,"【|】")
    print s2.encode('utf-8')

# col_content2 = []
# for i in col_content:
#     s = i.decoder("utf-8").encoder('utf-8')
#     col_content2 = col_content2 + [s]
#
# for i in col_content2:
#     print i

# print df2.dtypes
#
# df2["CONTENT"] = df2['CONTENT'].astype("str")
# print df2.dtypes

# print "=====取list里面的第一个======="
# for x in col_content:
#     s1 = re.findall(r"【(.*)】", x)
#     if len(s1) >= 1:
#         s2 = s1[0].encode('utf-8')
#     else:
#         s2 = "".encode('utf-8')
#     print s2.encode('utf-8')


print "=====取list里面的第一个======="
for x in col_content:
    s1 = re.findall(r"【(.{1,100})】", x)
    if len(s1) >= 1:
        s2 = s1[0].encode('utf-8')
    else:
        s2 = "".encode('utf-8')
    print s2.encode('utf-8')