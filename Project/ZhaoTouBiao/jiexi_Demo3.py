from lxml import etree


content = """
<tr> 
 <td background="images/erji/er_bk_04.jpg">&nbsp;</td> 
 <td bgcolor="#FFFFFF" align="center">
  <table width="100%" border="0" cellspacing="0" cellpadding="0"> 
   <tbody>
    <tr> 
     <td align="center"><b class="Font9"> </b></td> 
    </tr> 
    <tr> 
     <td background="images/main/table_bk_04.jpg"></td> 
    </tr> 
    <tr> 
     <td class="aa"> 
      <table border="0" width="99%" height="30" cellpadding="5" cellspacing="5"> 
       <tbody>
        <tr> 
         <td align="center" class="font1" colspan="2"> 济南高新技术产业开发区东区街道办事处路灯养护项目采购需求公示 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2" colspan="2"> 一、项目概况及预算情况：<br>2019年东区街道办事处辖区内现有交接管理市政道路33条,涉及路灯5200盏，智能控制器33套，路灯高压变压器46台以及整个区域的电缆维修，路灯维修等。 项目分包情况：1个包。 预算情况：167万元。 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2" colspan="2"> 二、采购标的具体情况：<br>1.采购内容、数量及单项预算安排:详见附表。 2.需实现的功能或者目标：满足国家相关标准、行业标准、地方标准或其他标准、规范。 3.需满足的国家相关标准、行业标准、地方标准或者其他标准、规范：符合相关法律规定。 4.需满足的质量、安全、技术规格、物理特性等要求：符合相关规定。 5.需满足的采购政策要求：节能环保、中小微型企业扶持、监狱企业扶持等政府采购政策。 6.项目交付或者实施的地点 交付或实施地点：招标人指定地点。 7.需满足的服务标准、期限、效率等要求：现行国家验收标准、施工 规范、质量检验评定统一标准及当地政府有关文件规定。 8.项目售后及验收标准：自行验收 9.满足技术服务等要求。 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2" colspan="2"> 三、论证意见：<br> 详见附件。 </td> 
        </tr> 
        <tr> 
         <td height="24" align="left" valign="middle" class="font2" colspan="2"> 四、公示时间：本项目采购需求公示期限为3天：自2019年6月4日起，至2019年6月7日止 </td> 
        </tr> 
        <tr> 
         <td height="24" align="left" valign="middle" class="font2" colspan="2"> 五、意见反馈方式：<br>本项目采购需求方案公示期间接受社会公众及潜在供应商的监督。<br> 请遵循客观、公正的原则，对本项目需求方案提出意见或者建议，并请于2019-06-08前将书面意见反馈至采购人或者采购代理机构，采购人或者采购代理机构应当于公示期满5个工作日内予以处理。<br> 采购人或者采购代理机构未在规定时间内处理或者对处理意见不满意的，异议供应商可就有关问题通过采购文件向采购人或者采购代理机构提出质疑；质疑未在规定时间内得到答复或者对答复不满意的，异议供应商可以向采购人同级财政部门提出投诉。 </td> 
        </tr> 
        <tr> 
         <td height="24" align="left" valign="middle" class="font2" colspan="2"> 六、项目联系方式 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2"> 1、采购单位：济南高新技术产业开发区东区街道办事处 </td> 
         <td height="24" align="left" valign="middle" class="font2"> 地址：济南市高新区大正路3007号 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2"> 联系人：李爽 </td> 
         <td height="24" align="left" valign="middle" class="font2"> 联系方式：0531-88253711 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2"> 2.采购代理机构：山东新世纪招标有限公司 </td> 
         <td height="24" align="left" valign="middle" class="font2"> 地址：山东济南历下奥体中路4267四楼 </td> 
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="font2"> 联系人：魏娜 </td> 
         <td height="24" align="left" valign="middle" class="font2"> 联系方式：0531-69982888 </td> 
        </tr> 
        <tr>
         <td></td>
        </tr> 
        <tr>
         <td></td>
        </tr> 
        <tr>
         <td></td>
        </tr> 
        <tr>
         <td></td>
        </tr> 
        <tr> 
         <td align="left" valign="middle" class="Font9Black"> 附件：<a href="javascript:openFile(200531362)">『需求方案论证专家签到表及意见表.zip』</a> </td>
        </tr> 
       </tbody>
      </table> </td> 
    </tr> 
    <tr> 
     <td height="20"><span id="file_list"></span></td> 
    </tr> 
    <tr> 
     <td height="20" align="right" class="Font9">发布人：山东新世纪招标有限公司管理员</td> 
    </tr> 
    <tr> 
     <td height="20" align="right" class="Font9">发布时间：2019年06月04日 14时45分35秒</td> 
    </tr> 
    <tr> 
     <td background="images/main/table_bk_04.jpg"></td> 
    </tr> 
    <tr> 
     <td height="30"><b class="lg"> <img border="0" src="images/huan.jpg" width="11" height="11">&nbsp; 相关信息</b> </td> 
    </tr> 
    <tr>
     <td><img src="images/arrow4.gif" width="7" height="5"><a href="readneed.jsp?id=200035762">1、济南高新技术产业开发区东区街道办事处济南高新技术产业开发区东区街道办事处路灯养护项目需求公开</a></td>
    </tr> 
   </tbody>
  </table></td> 
 <td background="images/erji/er_bk_05.jpg">&nbsp;</td> 
</tr>
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
    run_456_2(content)
