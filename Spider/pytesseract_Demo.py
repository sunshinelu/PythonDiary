# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/11/14 下午3:11 
 @File    : pytesseract_Demo.py
 @Note    : 
 参考链接：
 Python3.6使用tesseract-ocr的正确姿势：https://blog.csdn.net/qq_14998713/article/details/78824859
 使用 python 识别简单验证码：https://www.jianshu.com/p/f28dc8af1aee
 tesseract-ocr/tesseract：https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows
 """

import pytesseract
from PIL import Image

image = Image.open('01.png')
code = pytesseract.image_to_string(image)
print(code)