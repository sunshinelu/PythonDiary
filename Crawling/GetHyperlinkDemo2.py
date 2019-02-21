#-*- coding: UTF-8 -*-


"""
python3利用beautiful soup获取网页文本及src链接和http链接
https://blog.csdn.net/a_cx97/article/details/50762324
"""
# from urllib import request # python3中使用
import urllib
from bs4 import BeautifulSoup

# url = 'http://sports.163.com/special/unluckykaka/'
# url = "https://blog.csdn.net/zjy18886018024?t=1"

# url = "http://law.bjtu.edu.cn/xygk/szll/zzjs/index.htm"
# url = "http://aad.bjtu.edu.cn/content/unit_teacher.asp?topic=%E6%95%99%E5%AD%A6%E5%9B%A2%E9%98%9F&menuName=%E5%B8%88%E8%B5%84%E9%98%9F%E4%BC%8D&classid=28"
# url = "http://faculty.bjtu.edu.cn/yyxy/jsml.html?xm=&dw=&zc=&xk=&ds=&szm="
# url = "http://p.bjtu.edu.cn/szdw/jstd/jsml.htm"
# url = "http://p.bjtu.edu.cn/szdw/jstd/jslb.htm?zc=jiaoshou"
# url = "http://ncms.ustb.edu.cn/rencaipeiyang/daoshiduiwu/"
# url = "http://adma.ustb.edu.cn/xygk/szdw/index.html"
# url = "http://sfs.ustb.edu.cn/cn/shiziduiwu/shuoshishengdaoshi/"
# url  = "http://sem.ustb.edu.cn/szll/jsjs/szgk/index.htm"
url = "http://shuli.ustb.edu.cn/shiziduiwu/xisuojiansuo/"

# html = request.urlopen(url) ＃ python3中使用
html = urllib.urlopen(url)

soup = BeautifulSoup(html.read() ,"html.parser")
print(soup.body.text.encode('utf-8' ,'ignore').decode('utf-8'))

img_ = soup.find_all(name='img')
for each in img_:
    print(each.get('src'))
print('end')

href_ = soup.find_all(name='a')
for each in href_:
    print(each)
    if str(each.get('href'))[:4] == 'http':
        print(each.get('href'))
        print(each)
print('end')
