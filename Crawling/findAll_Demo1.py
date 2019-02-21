#-*- coding: UTF-8 -*-

"""
[python] 常用正则表达式爬取网页信息及分析HTML标签总结
http://www.voidcn.com/article/p-fqzvfpup-ps.html

Python正则表达式指南
http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html

[python学习] 简单爬取图片网站图库中图片
http://www.voidcn.com/article/p-wuuzgmcy-po.html
"""

import re
import urllib
import os


"""
1.获取<tr></tr>标签之间内容
"""


language = '''<tr><th>性別：</th><td>男</td></tr><tr>'''

#正则表达式获取<tr></tr>之间内容
res_tr = r'<tr>(.*?)</tr>'
m_tr =  re.findall(res_tr,language,re.S|re.M)
for line in m_tr:
    print line
    #获取表格第一列th 属性
    res_th = r'<th>(.*?)</th>'
    m_th = re.findall(res_th,line,re.S|re.M)
    for mm in m_th:
        print unicode(mm,'utf-8'),  #unicode防止乱
    #获取表格第二列td 属性值
    res_td = r'<td>(.*?)</td>'
    m_td = re.findall(res_td,line,re.S|re.M)
    for nn in m_td:
        print unicode(nn,'utf-8')


"""
2.获取超链接<a href=..></a>之间内容
"""

content = '''
<td>
<a href="https://www.baidu.com/articles/zj.html" title="浙江省">浙江省主题介绍</a>
<a href="https://www.baidu.com//articles/gz.html" title="贵州省">贵州省主题介绍</a>
</td>
'''

#获取<a href></a>之间的内容
print u'获取链接文本内容:'
res = r'<a .*?>(.*?)</a>'
mm = re.findall(
res, content, re.S|re.M)
for value in mm:
    print value

#获取所有<a href></a>链接所有内容
print u'\n获取完整链接内容:'
urls=re.findall(r"<a.*?href=.*?<\/a>", content, re.I|re.S|re.M)
for i in urls:
    print i

#获取<a href></a>中的URL
print u'\n获取链接中URL:'
res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
link = re.findall(res_url ,  content, re.I|re.S|re.M)
for url in link:
    print url


"""
3.获取URL最后一个参数命名图片或传递参数
"""
urls = "http://i1.hoopchina.com.cn/blogfile/201411/11/BbsImg141568417848931_640*640.jpg"
values = urls.split('/')[-1]
print values


url = 'http://localhost/test.py?a=hello&b=world'
values = url.split('?')[-1]
print values
for key_value in values.split('&'):
    print key_value.split('=')


"""
4.爬取网页中所有URL链接
"""


url = "http://www.csdn.net/"
content = urllib.urlopen(url).read()
urls = re.findall(r"<a.*?href=.*?<\/a>", content, re.I)
for url in urls:
    print unicode(url, 'utf-8')

link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", content)
for url in link_list:
    print url


"""
5.爬取网页标题title两种方法 
"""
url = "http://www.csdn.net/"
content = urllib.urlopen(url).read()

print u'方法一:'
title_pat = r'(?<=<title>).*?(?=</title>)'
title_ex = re.compile(title_pat,re.M|re.S)
title_obj = re.search(title_ex, content)
title = title_obj.group()
print title

print u'方法二:'
title = re.findall(r'<title>(.*?)</title>', content)
print title[0]

"""
6.定位table位置并爬取属性-属性值 
"""

start = content.find(r'<table class="infobox vevent"') #起点记录查询位置
end = content.find(r'</table>')
infobox = language[start:end]
print infobox



s = '''<table>  
<tr>  
<td>序列号</td><td>DEIN3-39CD3-2093J3</td>  
<td>日期</td><td>2013年1月22日</td>  
<td>售价</td><td>392.70 元</td>  
<td>说明</td><td>仅限5用户使用</td>  
</tr>  
</table>
'''

res = r'<td>(.*?)</td><td>(.*?)</td>'
m = re.findall(res,s,re.S|re.M)
for line in m:
    print unicode(line[0],'utf-8'),unicode(line[1],'utf-8') #unicode防止乱码


"""
7.过滤<span></span>等标签 
"""


language = '''
<table class="infobox bordered vcard" style="width: 21em; font-size: 89%; text-align: left;" cellpadding="3">
<caption style="text-align: center; font-size: larger;" class="fn"><b>周恩来</b></caption>
<tr>
<th>性別：</th>
<td>男</td>d
</tr>
<tr>
<th>異名：</th>
<td><span class="nickname">(字) 翔宇</span></td>
</tr>
<tr>
<th>政黨：</th>
<td><span class="org"><a href="../articles/%E4%B8%AD9A.html" title="中国共产党">中国共产党</a></span></td>
</tr>
<tr>
<th>籍貫：</th>
<td><a href="../articles/%E6%B5%9981.html" title="浙江省">浙江省</a><a href="../articles/%E7%BB%8D82.html" title="绍兴市">绍兴市</a></td>
</tr>
</table>
'''

#获取table中tr值
res_tr = r'<tr>(.*?)</tr>'
m_tr =  re.findall(res_tr,language,re.S|re.M)
for line in m_tr:
    #获取表格第一列th 属性
    res_th = r'<th>(.*?)</th>'
    m_th = re.findall(res_th,line,re.S|re.M)
    for mm in m_th:
        if "href" in mm: #如果获取加粗的th中含超链接则处理
            restr = r'<a href=.*?>(.*?)</a>'
            h = re.findall(restr,mm,re.S|re.M)
            print unicode(h[0],'utf-8'), #逗号连接属性值 防止换行
        else:
            print unicode(mm,'utf-8'),   #unicode防止乱

    #获取表格第二列td 属性值
    res_td = r'<td>(.*?)</td>'  #r'<td .*?>(.*?)</td>'
    m_td = re.findall(res_td,line,re.S|re.M)
    for nn in m_td:
        if "href" in nn: #处理超链接<a href=../rel=..></a>
            res_value = r'<a .*?>(.*?)</a>'
            m_value = re.findall(res_value,nn,re.S|re.M)
            for value in m_value:
                print unicode(value,'utf-8'),
        elif "span" in nn: #处理标签<span>
            res_value = r'<span .*?>(.*?)</span>'
            m_value = re.findall(res_value,nn,re.S|re.M) #<td><span class="nickname">(字) 翔宇</span></td>
            for value in m_value:
                print unicode(value,'utf-8'),
        else:
            print unicode(nn,'utf-8'),
        print ' ' #换行


"""
8.获取<script></script>等标签内容 
"""


content = '''
<script>var images = [  
{ "big":"http://i-2.yxdown.com/2015/3/18/KDkwMHgp/6381ccc0-ed65-4422-8671-b3158d6ad23e.jpg",  
  "thumb":"http://i-2.yxdown.com/2015/3/18/KHgxMjAp/6381ccc0-ed65-4422-8671-b3158d6ad23e.jpg",  
  "original":"http://i-2.yxdown.com/2015/3/18/6381ccc0-ed65-4422-8671-b3158d6ad23e.jpg",  
  "title":"","descript":"","id":75109},  
{ "big":"http://i-2.yxdown.com/2015/3/18/KDkwMHgp/fec26de9-8727-424a-b272-f2827669a320.jpg",  
  "thumb":"http://i-2.yxdown.com/2015/3/18/KHgxMjAp/fec26de9-8727-424a-b272-f2827669a320.jpg",  
  "original":"http://i-2.yxdown.com/2015/3/18/fec26de9-8727-424a-b272-f2827669a320.jpg",  
  "title":"","descript":"","id":75110},   
</script>  
'''

html_script = r'<script>(.*?)</script>'
m_script = re.findall(html_script,content,re.S|re.M)
for script in m_script:
    res_original = r'"original":"(.*?)"' #原图
    m_original = re.findall(res_original,script)
    for pic_url in m_original:
        print pic_url
        filename = os.path.basename(pic_url) #去掉目录路径,返回文件名
        urllib.urlretrieve(pic_url, 'E:\\'+filename) #下载图片