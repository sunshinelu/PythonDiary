#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from lxml import etree
import re
import chardet
import urllib.request
from lxml import etree
import re
import json


# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

# connect mysql
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="localhost", # 127.0.0.1
  database="cnki",
  user="root",
  password="root",
  port=3306,
  charset='utf8'
 )

# sql语句
sqlcmd = "select * from cnki_details"

# 利用pandas 模块导入mysql数据
df = pd.read_sql(sqlcmd,dbconn)

# get specific columns
columns = ["url"]
df1 = df[columns]#.head(10)
# print df1
list1 = df1.values.tolist()
# print list1


list2 = []
for k in df1.values:
    for j in k:
        list2.append(j)


# df1 = df[df.url.str.contains("http:")]
# print df1.count()

# df1['text_length'] = df1['TEXT'].apply(len)
#
# df1 = df1[df1.text_length > 10]
# print df1.count()

xx = u"[\u4e00-\u9fa50-9]+"
pattern = re.compile(xx)

property_name_list = []
property_value_list = []
property = dict()

def GetName(url):
    if "baike.baidu.com" in url:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        html = response.read()
        html = etree.HTML(html.decode('utf8', 'ignore'))
        # property_name_list = []
        # property_value_list = []
        # property = dict()
        if html.xpath('//div[@class="basic-info cmn-clearfix"]/dl'):
            for t in html.xpath('//div[@class="basic-info cmn-clearfix"]/dl'):
                for dt in t.xpath('./dt[@class="basicInfo-item name"]'):
                    property_name = ''.join(pattern.findall(''.join(dt.xpath('./text()'))))
                    property_name_list.append(property_name)
                for dd in t.xpath('./dd[@class="basicInfo-item value"]'):
                    property_value = (''.join(dd.xpath('.//text()')).replace("\n",""))
                    property_value_list.append(property_value)
        for i in range(len(property_value_list)):
            property.setdefault(property_name_list[i],property_value_list[i])
            # print property

# print list1
for i in list2:
    # print i
    GetName(i)

for i, j in property.items():
    print(i)

print(property)