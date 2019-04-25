#encoding=utf-8
from urllib.parse import quote
import urllib
import json
import numpy as np

import urllib.request

"""
复旦KG(CN-DBpedia)使用(python) 
http://f.dataguru.cn/thread-918592-1-1.html

"""

#请求1：输入实体指称项名称，返回对应实体(entity)的列表，json格式
#格式http://shuyantech.com/api/cndbpedia/avpair?q=**      # **是查询的实体名
ch_str = quote('苹果')
en_url = 'http://shuyantech.com/api/cndbpedia/ment2ent?q='
url = en_url + ch_str
response1 = urllib.request.urlopen(url)
print(response1.read().decode('utf-8'))

#请求2：输入实体名，返回实体全部的三元组知识
#格式：http://shuyantech.com/api/cndbpedia/value?q=**&attr=**    # 前**是查询的实体名；后**是查询的属性名
ch_str = quote('复旦大学')
en_url = 'http://shuyantech.com/api/cndbpedia/avpair?q='
url = en_url + ch_str
response2 = urllib.request.urlopen(url)
print(response2.read().decode('utf-8'))


#请求3：给定实体名和属性名，返回属性值
ch_str1 = quote('复旦大学')
ch_str2 = quote('英文名称')
en_url = 'http://shuyantech.com/api/cndbpedia/value?q='
url = en_url + ch_str1 + '&attr=' + ch_str2
response2 = urllib.request.urlopen(url)
print(response2.read().decode('utf-8'))