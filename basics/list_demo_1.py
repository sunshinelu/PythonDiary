# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/30 下午1:36 
 @File    : list_demo_1.py
 @Note    : 

 python寻找list中最大值、最小值并返回其所在位置的方法
 """

c = [-100, -5, 0, 5, 3, 10, 15, -20, 25]

print(c.index(min(c)))  # 返回最小值
print(c.index(max(c)))  # 返回最大值