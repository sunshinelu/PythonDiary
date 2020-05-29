# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/12/25 下午4:57 
 @File    : Koutu1.py
 @Note    : 
 https://blog.csdn.net/holly_z_p_f/article/details/100565065
 https://cloud.tencent.com/developer/article/1485934
 """
from removebg import RemoveBg
rmbg = RemoveBg("gFmFd4NdUN4G6J5uc9KDAr5t", "error.log") # 引号内是你获取的API
rmbg.remove_background_from_img_file("/Users/sunlu/Workspaces/PyCharm/PythonDiary/basics/koutu/test1.jpg") #图片地址