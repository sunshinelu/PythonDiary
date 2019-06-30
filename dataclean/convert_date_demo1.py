# -*- coding: utf-8 -*-

import datetime
import locale

locale.setlocale(locale.LC_CTYPE, 'chinese')

"""
处理时间，将时间转换成YYYY-MM-DD
"""
def convert_date(string):
    if not string:
        return string
    # 1942-04-28
    try:
        date = datetime.datetime.strptime(string, "%Y-%m-%d")
        return string
    except ValueError:
        pass
    # 1900-01-25 00:00:00
    try:
        date_str = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        return date_str
    except ValueError:
        pass
    # 1963年03月13日
    try:
        date_str = datetime.datetime.strptime(string, "%Y年%m月%d日").strftime("%Y-%m-%d")
        return date_str
    except ValueError:
        pass
    # 1971-00-00 1963-11-00
    string = string.replace('00', '').strip('-').strip('日').strip('月').strip()
    try:
        date_str = datetime.datetime.strptime(string, "%Y-%m").strftime("%Y-%m")
        return date_str
    except ValueError:
        pass
    try:
        date_str = datetime.datetime.strptime(string, "%Y").strftime("%Y")
        return date_str
    except ValueError:
        print('无法解析的日期' + string)

# s = "1942-04-28"
# s = None
# s = "1900-01-25 00:00:00"
s = "1963年03月13日"
s = "1971-00-00 1963-11-00"
s = "是"
s ="2190"

result = convert_date(s)
print(result)
print(type(result))