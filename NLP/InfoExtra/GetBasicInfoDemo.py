#-*- coding: UTF-8 -*-

import pandas as pd
import pymysql
import numpy as np
from lxml import etree
import re
import chardet
import urllib2
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
print "-------"

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
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
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
    GetName(str(i).encode('utf-8'))

for i, j in property.iteritems():
    print i

print(property)


"""

外文名
拼音
生于
主要研究方向
职称
党籍
毕业
开本
行政职务
笔名
人物类型
军衔
简介
从事专业
专利
代表作品
院系
所属学科
研究所中心
页数
记载
博导
出生年月
任职
毕业院校
出版年
研究科目
本名
姓别
学校
释义
具体工作单位
所属课题组
最后毕业学校
出生地
职位
字号
党派
姓名
定价
专业
祖籍
别名
在职单位
学位学历
学科领域
广泛应用
主要作品
荣誉
专业方向
单位
中文名称
主要成就
运动项目
博导专业
作者
教学职称
政治面貌
社会兼职
就职
学历学位
地理位置
临床职称
学历
星座
民族
硕导
粉丝
学术代表作
职务
血型
执业地点
主讲科目
中文名
主要讲授课程
研究领域
研究方向
学科
教学课程
民族族群
逝世日期
工作单位
用途
主要社会价值
学科专业
现任
生日
就读学校
指导学科
主讲
籍贯
信仰
经纪公司
类别
身高
性别
出生时间
总流域面积
详细解释
所处时代
书名
身份
曾获荣誉
硕导专业1
出版社
专业领域
出生年
最后学历
职业
出生地址
体重
国籍
出生日期
出版时间
学位
"""