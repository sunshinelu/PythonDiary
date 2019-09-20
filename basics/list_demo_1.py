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



col_name = ["identification_type","identification_id","email","mobile_phone","rand1"]
print(len(col_name))
# expr_col_1 = "Kafka_value." + col_name
#
# expr_col_1 = [lambda x:"Kafka_value."+str(x),col_name]
# print(expr_col_1)
# print(type(expr_col_1))

expr_col_1 = ["Kafka_value." +i for i in col_name]
print(expr_col_1)
print(type(expr_col_1))
print(* expr_col_1)

import uuid
print(uuid.uuid4())