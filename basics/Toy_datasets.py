# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/7/12 下午4:16 
 @File    : Toy_datasets.py
 @Note    : 
 
 """


from sklearn.datasets import load_linnerud,load_boston
linnerud = load_boston()

df = linnerud.data

df_label = linnerud.target

print(df_label)
