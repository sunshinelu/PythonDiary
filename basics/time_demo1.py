# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/9/16 下午4:04 
 @File    : time_demo1.py
 @Note    : 
 
 """

from datetime import datetime

s1 = "1984-10-26T03:52:14.449+0000"


endtime = datetime.now()
print(endtime)
# s2 = s1.toLocalDateTime().toLocalDate()
#
# print(s2)


# fmt = "%Y-%m-%dT%H:%M:%S.sss+0000"
fmt = "yyyy-MM-dd'T'HH:mm:ss.SSSZ"
start_date_dt = datetime.strptime(s1, fmt)
print(start_date_dt)

endtime = datetime.datetime.now()
print(endtime)
# end_date_dt = datetime.strptime(end_date, fmt)