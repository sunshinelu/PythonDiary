#-*- coding: UTF-8 -*-

"""


Python基础代码爬取超链接文字及链接
https://blog.csdn.net/zjy18886018024/article/details/80590828
"""

# import urllib.request # python3中使用
import urllib

from bs4 import BeautifulSoup
import requests
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

num = []
lianjie = []
# url = "https://blog.csdn.net/zjy18886018024?t=1"
# url = "http://law.bjtu.edu.cn/xygk/szll/zzjs/index.htm"
# url = "http://aad.bjtu.edu.cn/content/unit_teacher.asp?topic=%E6%95%99%E5%AD%A6%E5%9B%A2%E9%98%9F&menuName=%E5%B8%88%E8%B5%84%E9%98%9F%E4%BC%8D&classid=28"
url = "http://faculty.bjtu.edu.cn/yyxy/jsml.html?xm=&dw=&zc=&xk=&ds=&szm="


con = requests.get(url).text
# content = urllib.request.urlopen(url).read() ＃ python3中使用
content = urllib.urlopen(url).read()
soup = BeautifulSoup(content, "html.parser")
top = soup.find_all(attrs={"class": "text-truncate"})
lianji = re.findall('href="(.*?details\/\d{8})', con)
i = 0
nu = []
while i < len(top):
    num.append(top[i].get_text())
    nu.append(num[i].replace("原", ""))
    i = i + 1
j = 0
strc = []
while j < len(nu):
    # print(nu[j].strip(),lianji[i])
    strc.append(nu[j].strip())
    j = j + 1
m = 0
tops = ""
while m < len(strc):
    tops += str(strc[m]) + "\t" + lianji[m] + "\n"
    m = m + 1
print(tops)
# k = 0
# while k < len(tops):
#     with open("C:\\Users\\ASUS\\Desktop\\txt1\\neirong.txt", "a+") as f:
#         f.write(tops[k])
#         k = k + 1
#         f.close()
#
# print("写入成功")
