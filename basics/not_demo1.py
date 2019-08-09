# -*- coding: utf-8 -*-
"""
 not与逻辑判断句if连用，代表not后面的表达式为False的时候，执行冒号后面的语句.
 string为None的时候，print None；
 string不为None的时候，什么都不print
"""
string = None
string = "s"

if not string:
     print(string)

print("===========")

if string is None:
     print(string)