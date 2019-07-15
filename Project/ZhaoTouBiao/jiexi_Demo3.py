from lxml import etree


content = """
<div class="vF_detail_content"> 
 <p>　　北京首建项目管理有限公司受华润置地（北京）物业管理有限责任公司的委托，就“航天云岗区域“三供一业”维修改造项目（设计）”项目（项目编号：BSJ19-27）组织采购，评标工作已经结束，中标结果如下：</p>
 <p></p>
 <p>&nbsp;</p>
 <p><strong>一、项目信息</strong></p>
 <p>项目编号：BSJ19-27</p>
 <p>项目名称：航天云岗区域“三供一业”维修改造项目（设计）</p>
 <p>项目联系人：亢工</p>
 <p>联系方式：010-68386575</p>
 <p>&nbsp;</p>
 <p><strong>二、采购单位信息</strong></p>
 <p>采购单位名称：华润置地（北京）物业管理有限责任公司</p>
 <p>采购单位地址：北京市西城区太平街甲2号3层</p>
 <p>采购单位联系方式：亢工 010-68386575</p>
 <p>&nbsp;</p>
 <p><strong>三、项目用途、简要技术要求及合同履行日期：</strong></p>
 <p></p>
 <p style="text-indent: 21pt;">招标范围及内容：涉及航天云岗区域“三供一业”维修改造项目全部建设内容的设计服务，包括与产权单位沟通改造内容、确定并优化设计方案、初步设计（含概算编制）、施工图设计、施工过程中的施工现场服务（包括设计变更及洽商、竣工验收等）。包括设计过程中因原图纸不全或不完整所需的测量测绘（完成设计所需），以及产权单位提供档案、图纸后设计单位为完成设计工作所需的复印、扫描、转换成电子文档等，均由中标人自行完成或委托第三方完成，费用包括在投标报价中。（具体内容见第二章“设计条件及要求”。）</p>
 <p style="text-indent: 21pt;">设计服务期限：自合同签订之日起30日历天内完成设计文件的编制工作。服务期限至项目竣工验收完成配合招标人完成结算审计及相关决算审计完成为止。</p>
 <p style="text-indent: 21pt;">质量标准：符合国家的设计规范和标准，满足三供一业项目维修改造要求，设计图纸能通过相关审查。</p>
 <p></p>
 <p>&nbsp;</p>
 <p></p>
 <p><strong>四、采购代理机构信息</strong></p>
 <p>采购代理机构全称：北京首建项目管理有限公司</p>
 <p>采购代理机构地址：北京市丰台区西局西街273号安助置业院内东侧楼一层</p>
 <p>采购代理机构联系方式：束婷 15811156126</p>
 <p>&nbsp;</p>
 <p><strong>五、中标信息</strong></p>
 <p>招标公告日期：2019年05月22日</p>
 <p>中标日期：2019年06月12日</p>
 <p>总中标金额：0.0 万元（人民币）</p>
 <p>中标供应商名称、联系地址及中标金额：</p>
 <p></p>
 <table border="1" cellpadding="0" cellspacing="0"> 
  <tbody> 
   <tr> 
    <td>序号</td> 
    <td>中标供应商名称</td> 
    <td>中标供应商联系地址</td> 
    <td>中标金额(万元)</td> 
   </tr> 
   <tr> 
    <td>1</td> 
    <td>华诚博远工程技术集团有限公司</td> 
    <td>&nbsp;</td> 
    <td>0.000000</td> 
   </tr> 
   <tr> 
    <td>2</td> 
    <td>北京实创博威建筑设计院有限公司</td> 
    <td>&nbsp;</td> 
    <td>0.000000</td> 
   </tr> 
   <tr> 
    <td>3</td> 
    <td>国策众合（北京）建筑工程设计有限公司</td> 
    <td>&nbsp;</td> 
    <td>0.000000</td> 
   </tr> 
  </tbody>
 </table>
 <p></p>
 <p><b>本项目招标代理费总金额：0.0 万元（人民币）</b></p>
 <p>本项目招标代理费收费标准：</p>
 <p>参照《招标代理服务收费管理暂行办法》计价格【2002】1980号文和发改价格【2011】534号文</p>
 <p>&nbsp;</p>
 <p>评审专家名单：</p>
 <p>\</p>
 <p>&nbsp;</p>
 <p>中标标的名称、规格型号、数量、单价、服务要求：</p>
 <p></p>
 <p>中标标的名称：航天云岗区域“三供一业”维修改造项目（设计）</p>
 <p>规格型号：\</p>
 <p>数量：1</p>
 <p>单价：\</p>
 <p>服务要求：涉及航天云岗区域“三供一业”维修改造项目全部建设内容的设计服务，包括与产权单位沟通改造内容、确定并优化设计方案、初步设计（含概算编制）、施工图设计、施工过程中的施工现场服务（包括设计变更及洽商、竣工验收等）。包括设计过程中因原图纸不全或不完整所需的测量测绘（完成设计所需），以及产权单位提供档案、图纸后设计单位为完成设计工作所需的复印、扫描、转换成电子文档等，均由中标人自行完成或委托第三方完成，费用包括在投标报价中。（具体内容见第二章“设计条件及要求”。）</p>
 <p>设计服务期限：自合同签订之日起30日历天内完成设计文件的编制工作。服务期限至项目竣工验收完成配合招标人完成结算审计及相关决算审计完成为止。</p>
 <p>质量标准：符合国家的设计规范和标准，满足三供一业项目维修改造要求，设计图纸能通过相关审查。</p>
 <p></p>
 <p>&nbsp;</p>
 <p><strong>六、其它补充事宜</strong></p>
 <p></p>
 <p>本中标候选人公示截止日期：2019年7月16日</p>
 <p></p>
 <p>&nbsp;</p>
 <p></p>
 <p></p>
 <p></p>
 <p></p>
 <p>&nbsp;</p>
 <p></p> 
</div>
"""

def run_123():
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.parse('123.txt', parser=parser)
    p_seletors = html.xpath('//*[@class="vF_detail_content"]/*')
    p_list = []
    for p_seletor in p_seletors:
        p_content = p_seletor.xpath('.//text()')
        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        # print(p_content)
        p_list.append(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)


def run_123(content):
    parser = etree.HTMLParser(encoding="utf-8")
    # html = etree.parse('123.txt', parser=parser)
    html = etree.HTML(str(content), parser=parser)
    p_seletors = html.xpath('//*[@class="vF_detail_content"]/*')
    p_list = []
    for p_seletor in p_seletors:
        p_content = p_seletor.xpath('.//text()')
        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        # print(p_content)
        p_list.append(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)


def run_456():
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.parse('456.txt', parser=parser)
    table_seletors = html.xpath('//table//tr')
    p_list = []
    for table_seletor in table_seletors:
        p_content = table_seletor.xpath('.//text()')
        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        p_list.append(p_content)
        #print(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)

def run_456_2(content):
    parser = etree.HTMLParser(encoding="utf-8")
    # html = etree.parse('456.txt', parser=parser)
    html = etree.HTML(str(content), parser=parser)
    table_seletors = html.xpath('//table//tr')
    p_list = []
    for table_seletor in table_seletors:
        p_content = table_seletor.xpath('.//text()')

        p_content = map(lambda x: x.strip(), p_content)
        p_content = "".join(p_content)
        p_list.append(p_content)
        # print(p_content)
    file_content = '\n'.join(p_list)
    print(file_content)


if __name__ == '__main__':
    # run_123()
    # run_456()
    # run_456_2(content)
    run_123(content)
