#-*- coding: UTF-8 -*-

import re
import urllib
import os
from bs4 import BeautifulSoup

"""
2.获取超链接<a href=..></a>之间内容
  <div class="para" label-module="para">  </div> 之间内容
"""

content = '''
<div class="main-content"> 
 <div class="top-tool"> 
  <a class="add-sub-icon top-tool-icon" href="javascript:;" title="添加义项" nslog-type="50000101"> <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_add-subLemma-solid"></em> </a> 
  <a href="/divideload/%E4%B8%98%E4%BA%AC%E8%BE%89" title="拆分词条" target="_blank" class="split-icon top-tool-icon" style="display:none;" nslog-type="50000104"> <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_lemma-split"></em> </a> 
  <div class="top-collect top-tool-icon" nslog="area" nslog-type="50000102"> 
   <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_star-solid"></em> 
   <span class="collect-text">收藏</span> 
   <div class="collect-tip">
    查看
    <a href="/uc/favolemma" target="_blank">我的收藏</a>
   </div> 
  </div> 
  <a href="javascript:void(0);" id="j-top-vote" class="top-vote top-tool-icon" nslog-type="10060801"> <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_zan-solid"></em> <span class="vote-count">0</span> <span class="vote-tip">有用+1</span> <span class="voted-tip">已投票</span> </a>
  <div class="bksharebuttonbox top-share"> 
   <a class="top-share-icon top-tool-icon" nslog-type="9067"> <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_share"></em> <span class="share-count" id="j-topShareCount">0</span> </a> 
   <div class="new-top-share" id="top-share"> 
    <ul class="top-share-list"> 
     <li class="top-share-item"> <a class="share-link bds_qzone" href="javascript:void(0);" nslog-type="10060501"> <em class="cmn-icon cmn-icons cmn-icons_logo-qzone"></em> </a> </li> 
     <li class="top-share-item"> <a class="share-link bds_tsina" href="javascript:void(0);" nslog-type="10060701"> <em class="cmn-icon cmn-icons cmn-icons_logo-sina-weibo"></em> </a> </li> 
     <li class="top-share-item"> <a class="bds_wechat" href="javascript:void(0);" nslog-type="10060401"> <em class="cmn-icon cmn-icons cmn-icons_logo-wechat"></em> </a> </li> 
     <li class="top-share-item"> <a class="share-link bds_tqq" href="javascript:void(0);" nslog-type="10060601"> <em class="cmn-icon cmn-icons cmn-icons_logo-qq"></em> </a> </li> 
    </ul> 
   </div> 
  </div> 
 </div> 
 <div style="width:0;height:0;clear:both"></div>
 <dl class="lemmaWgt-lemmaTitle lemmaWgt-lemmaTitle-"> 
  <dd class="lemmaWgt-lemmaTitle-title"> 
   <h1>丘京辉</h1> 
   <a href="javascript:;" class="edit-lemma cmn-btn-hover-blue cmn-btn-28 j-edit-link"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a> 
   <a class="lock-lemma" nslog-type="10003105" target="_blank" href="/view/10812319.htm" title="锁定"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_lock-lemma"></em>锁定</a> 
  </dd> 
 </dl>
 <div class="edit-prompt">
  本词条缺少
  <strong>名片图</strong>，补充相关内容使词条更完整，还能快速升级，赶紧来
  <a class="edit-prompt-link j-edit-link">编辑</a>吧！
 </div> 
 <div class="promotion-declaration"> 
 </div>
 <div class="lemma-summary" label-module="lemmaSummary"> 
  <div class="para" label-module="para">
   丘京辉 教授。1947年8月出生，广东大埔人。1974年毕业于江苏师范学院数学系。现任苏州大学数学科学学院教授。是美国《数学评论》杂志评论员，英国剑桥国际名人传记中心顾问委员会荣誉会员。1966年以来一直坚持自学数学，1970年代曾从事充氦飞船体积计算和专用机床摇摆凸轮廓线的设计，获得了准确的计算公式。近20年主要致力于“泛函分析”的理论研究，在中国、美国、德国等10余种学术期刊上发表数学论文40余篇。在诱导极限理论方面，提出了新的研究思路，获得了一系列成果，改进并推广了前人的结论，特别解决了（Mo）型（LF）空间的正则性问题。在开映照与闭图定理方面，给出了Kalton闭图定理的完全推广，进而在拓扑向量空间的框架下，建立了连续、弱连续、团图和弱奇异算子的开映照定理的最一般形式。这使得已有这方面成果，如Ptak、Husain和Adasch等开映照定理均成为其一般形式的特例。在几何泛函分析方面，与美国学者Mckennon共同提出了严格端点的理论，揭示了在无穷维空间中凸集在端点处的几何结构与相关映照的分析性质之间的内在联系，被认为“可能是一个非常有趣的研究领域的良好开创”。1997年获苏州市政府颁发的自然科学优秀论文特等奖，1998年获江苏省优秀科技工作者荣誉称号，1999年获曾宪梓教师奖(三等奖)。简历与成就曾被英国剑桥国际名人传记中心和美国《世界名人录》收录。
  </div> 
 </div> 
 <div class="configModuleBanner"> 
 </div>
 <div class="basic-info cmn-clearfix"> 
  <dl class="basicInfo-block basicInfo-left"> 
   <dt class="basicInfo-item name">
    中文名
   </dt> 
   <dd class="basicInfo-item value">
     丘京辉 
   </dd> 
   <dt class="basicInfo-item name">
    国&nbsp;&nbsp;&nbsp;&nbsp;籍
   </dt> 
   <dd class="basicInfo-item value">
     中国 
   </dd> 
   <dt class="basicInfo-item name">
    民&nbsp;&nbsp;&nbsp;&nbsp;族
   </dt> 
   <dd class="basicInfo-item value">
     汉族 
   </dd> 
  </dl>
  <dl class="basicInfo-block basicInfo-right"> 
   <dt class="basicInfo-item name">
    出生地
   </dt> 
   <dd class="basicInfo-item value">
     江苏南京 
   </dd> 
   <dt class="basicInfo-item name">
    出生日期
   </dt> 
   <dd class="basicInfo-item value">
     1947年8月 
   </dd> 
   <dt class="basicInfo-item name">
    职&nbsp;&nbsp;&nbsp;&nbsp;业
   </dt> 
   <dd class="basicInfo-item value">
     大学教师 
   </dd> 
  </dl>
 </div> 
 <div class="lemmaWgt-lemmaCatalog"> 
  <div class="lemma-catalog"> 
   <h2 class="block-title">目录</h2> 
   <div class="catalog-list column-1"> 
    <ol> 
     <li class="level1"> <span class="index">1</span> <span class="text"><a href="#1">基本情况</a></span> </li> 
     <li class="level1"> <span class="index">2</span> <span class="text"><a href="#2">个人简介</a></span> </li> 
    </ol> 
   </div> 
  </div> 
 </div> 
 <div class="anchor-list"> 
  <a name="1" class="lemma-anchor para-title"></a> 
  <a name="sub1460967_1" class="lemma-anchor "></a> 
  <a name="基本情况" class="lemma-anchor "></a> 
 </div>
 <div class="para-title level-2" label-module="para-title"> 
  <h2 class="title-text"><span class="title-prefix">丘京辉</span>基本情况</h2> 
  <a class="edit-icon j-edit-link" data-edit-dl="1" href="javascript:;"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a> 
 </div> 
 <div class="para" label-module="para">
  姓名 ： 丘京辉
 </div> 
 <div class="para" label-module="para">
  任教专业 ： 理学-数学类
 </div> 
 <div class="para" label-module="para">
  在职情况 ： 在
 </div> 
 <div class="para" label-module="para">
  性别 ： 男
 </div> 
 <div class="para" label-module="para">
  所在院系 ： 数学科学学院
 </div> 
 <div class="para" label-module="para">
  所教课程 ：
 </div> 
 <div class="para" label-module="para">
  研究方向 ： 泛函分析领域的研究
 </div>
 <div class="anchor-list"> 
  <a name="2" class="lemma-anchor para-title"></a> 
  <a name="sub1460967_2" class="lemma-anchor "></a> 
  <a name="个人简介" class="lemma-anchor "></a> 
 </div>
 <div class="para-title level-2" label-module="para-title"> 
  <h2 class="title-text"><span class="title-prefix">丘京辉</span>个人简介</h2> 
  <a class="edit-icon j-edit-link" data-edit-dl="2" href="javascript:;"><em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma"></em>编辑</a> 
 </div> 
 <div class="para" label-module="para">
  <a target="_blank" href="/item/%E8%8B%8F%E5%B7%9E%E5%A4%A7%E5%AD%A6">苏州大学</a>教授教授，男，1947年8月生，江苏南京人，祖籍广东客家人生于江苏南京，成长于江苏昆山。1974年毕业于
  <a target="_blank" href="/item/%E8%8B%8F%E5%B7%9E%E5%A4%A7%E5%AD%A6">苏州大学</a>数学专业，现为苏州大学数学专业博士生导师。
 </div> 
 <div class="para" label-module="para">
  主要从事泛函分析领域的研究工作，主持省教育厅基金项目。在数学学报、美国数学会会报、波兰数学研究、德国数学通讯等国内外重要数学刊物上发表论文60多篇。1998年获“江苏省优秀科技工作者”。自1993年起指导硕士研究生，所指导研究生已有5人获硕士学位。
 </div> 
 <div class="para" label-module="para">
  代表性论文 ： 《关于凸过程的开映照与闭图定理》《σ 半凸性与Ekeland 变分原理》
  <sup class="sup--normal" data-sup="1"> [1]</sup>
  <a class="sup-anchor" name="ref_[1]_1460967">&nbsp;</a> 
 </div> 
 <div class="go-auth-box"> 
  <div class="go-auth-con"> 
   <em class="cmn-icon wiki-lemma-icons wiki-lemma-icons_info"></em> 百度百科内容由网友共同编辑，如您发现自己的词条内容不准确或不完善，欢迎使用本人词条编辑服务（免费）参与修正。
   <a href="/personal/auth/丘京辉/831973?bk_fr=lemma" target="_blank" nslog-type="10090202">立即前往&gt;&gt;</a> 
  </div> 
 </div> 
 <dl class="lemma-reference collapse nslog-area log-set-param" data-nslog-type="2" log-set-param="ext_reference"> 
  <dt class="reference-title">
   参考资料
  </dt> 
  <dd class="reference-list-wrap"> 
   <ul class="reference-list"> 
    <li class="reference-item reference-item--type1 " id="reference-[1]-1460967-wrap"> <span class="index">1.</span> <a class="gotop anchor" name="refIndex_1_1460967" id="refIndex_1_1460967" title="向上跳转" href="#ref_[1]_1460967">&nbsp;&nbsp;</a> <a rel="nofollow" href="/redirect/a3a4I2SWHW4KJfvt9J1lyN-mUW15ZqdE8C_qKh4kHLeac3trpa-2Uhy69Frsi8udH75_2tCB_bPUKt7gJVdgetfNwub2fg" target="_blank" class="text">丘京辉<span class="linkout">&nbsp;</span></a> </li>
   </ul> 
  </dd> 
 </dl> 
 <div id="open-tag"> 
  <div class="open-tag-title">
   词条标签：
  </div> 
  <dd id="open-tag-item"> 
   <span class="taglist"> 行业人物 </span> ，
   <span class="taglist"> 教育 </span> ，
   <span class="taglist"> 教师 </span> ，
   <span class="taglist"> 大学教师 </span> ，
   <span class="taglist"> 人物 </span> 
  </dd> 
  <div class="open-tag-collapse" id="open-tag-collapse"></div> 
 </div> 
 <div class="clear"></div> 
</div>
'''

res = r'<div class="para" label-module="para">(.*?)</div>'
mm = re.findall(res, content, re.S|re.M)
# print mm
for value in mm:
    print(value)

print("==================")

soup = BeautifulSoup(content, "html.parser")
print(soup)