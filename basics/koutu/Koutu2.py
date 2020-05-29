# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/12/25 下午5:09 
 @File    : Koutu2.py
 @Note    : 
 
 """

from removebg import RemoveBg
import os

rmbg = RemoveBg("gFmFd4NdUN4G6J5uc9KDAr5t", "error.log")
path = '%s/picture'%os.getcwd() #图片放到程序的同级文件夹 picture 里面
for pic in os.listdir(path):
    # print("%s/%s"%(path,pic))
    rmbg.remove_background_from_img_file("%s/%s"%(path,pic))