# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/30 下午2:37 
 @File    : get_path.py
 @Note    : 
 获取项目路径
 参考链接：
 python获取当前目录路径和上级路径
 https://blog.csdn.net/leorx01/article/details/71141643
 """

import os
print(os.getcwd()) #获取当前工作目录路径
print(os.path.abspath(os.curdir)) #获取当前工作目录路径
curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)

#  '***获取上级目录***'
dataPath = os.path.abspath(os.path.join(os.getcwd(), "../data"))
print(dataPath)

print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
print(os.path.abspath(os.path.dirname(os.getcwd())))
print(os.path.abspath(os.path.join(os.getcwd(), "..")))

import sys
print(sys.argv[0])