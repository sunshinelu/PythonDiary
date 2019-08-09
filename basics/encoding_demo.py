# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/31 上午8:43 
 @File    : encoding_demo.py
 @Note    : 
 
 """

import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
print(sys.getdefaultencoding())

print(sys.stdout.encoding)

print(sys.stdout)

line = '\\'

s2 = str(line)

print(s2)

strlist = ['Hello', '/', 'World', '!']
print(''.join(strlist))