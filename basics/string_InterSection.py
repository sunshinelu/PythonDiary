# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 20/5/29 上午11:29 
 @File    : string_InterSection.py
 @Note    : 

 https://blog.csdn.net/zhou01yang/article/details/12798959
 https://stackoverflow.com/questions/12028204/python-cant-import-set-from-sets-no-module-named-sets
 """



# import sets
# magic_char = sets.Set('abcde')
# poppins_chars = sets.Set('bdxyz')
magic_char = set('abcde')
poppins_chars = set('bdxyz')
print(''.join(magic_char & poppins_chars))	#InterSection
print(''.join(magic_char | poppins_chars))	#Union
