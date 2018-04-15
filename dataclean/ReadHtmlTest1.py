#-*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from lxml import etree

s = """<a class='k' href='https://m.weibo.cn/k/%E7%A6%8F%E5%B7%9E%E8%BA%AB%E8%BE%B9%E4%BA%8B?from=feed'>#福州身边事#</a>【永泰梧桐镇果农用传统手工 制出原汁原味柿饼】<a href='https://m.weibo.cn/n/海峡都市报'>@海峡都市报</a>：秋季的福州乡村除了层林尽染，绵延无尽的斑斓美景，还有乡亲们收秋晒秋的忙碌身影。在永泰梧桐镇，山里柿子红彤彤挂满枝头，村民们趁着柿子还没软就采摘下来，开始一年一度传统手工劳作：去皮、晾晒、出霜，做成美味的柿饼。vi ​​​...<a href="/status/4040267663381680">全文</a>"""
print s#.decode("utf-8")#.encode("utf-8")


html=etree.HTML(s.decode('utf-8'))
print(html)
result = etree.tostring(html)
print(result.decode("utf-8"))

html_data = html.xpath('//a/@href')
print html_data

selector=etree.HTML(s.decode('utf-8'))
html_data = selector.xpath('//a/text()')
for i in html_data:
    print i#.decode('utf-8')#.encode('utf-8')

selector=etree.HTML(s.decode('utf-8'))
html_data = selector.xpath('//a//text()')
for i in html_data:
    print i.decode('utf-8').encode('utf-8')

print "＝＝＝＝＝＝＝＝＝＝＝＝"
selector=etree.HTML(s.decode('utf-8'))
html_data = selector.xpath('//text()')
for i in html_data:
    print i.decode('utf-8').encode('utf-8')