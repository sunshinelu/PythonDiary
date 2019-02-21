#-*- coding: UTF-8 -*-

import re

# s = """
# <body>    <div id="wrap">     <div class="masthead">        <div class="logo">        <div class="link_logo widget_search">                 <div class="clearfix"></div>         				 		 		 		          <form id="searchform" name="dataForm" action="/cms/search/searchResults.jsp" target="_blank" method="post" accept-charset="utf-8" onsubmit="document.charset='utf-8';">				<p><a href="http://www.bjtu.edu.cn/pub/fxyyw/" target="_blank">English</a></p>				<p>					<input name="siteID" value="64" type="hidden">					<input id="s" name="query" placeholder="Search" type="text">					<button type="submit" id="searchsubmit" name="Submit"></button>				</p>			</form>               </div>        </div>                        <div class="clearfix"></div>                <nav id="navigation" class="navigation">						<ul> 			    				<li><a href="http://law.bjtu.edu.cn/">首&nbsp;页</a></li>													     <li>									  				   															    							<a href="../../xyjj/index.htm">											 					 					 学院概况</a></li>				   					     <li>									  				   															    							<a href="../../../bkjx/zsjz/index.htm">											 					 					 本科事务</a></li>				   					     <li>									  				   															    							<a href="../../../yjspy/zsjz2/index.htm">											 					 					 研究生事务</a></li>				   					     <li>									  				   															    							<a href="../../../xzky/kygg/index.htm">											 					 					 学术科研</a></li>				   					     <li>									  				   					 <a href="../../../dwjl/index.htm"> 					 					 对外交流</a></li>				   					     <li>									  				   															    														  <a href="../../../djgz/jgdjjgkhd/jgsz_20150420155801323192/index.htm">																		 					 					 党团建设</a></li>				   					     <li>									  				   															    							<a href="../../../xstd/xyfc/index.htm">											 					 					 校友天地</a></li>				   					     <li>									  				   					 <a href="../../../jyxx/index.htm"> 					 					 就业工作</a></li>				   				   							</ul>								</nav><!--/ #navigation-->              </div>            <div class="top-panel clearfix">		<div class="row-fluid">        	<div class="span12">            	<img src="../../../images/list.jpg">                        </div>		</div>	</div>      <!-- Example row of columns -->  <div class="row-fluid bggay">        <div class="span4">                   <div class="leftbox_top">          <div class="blog_sidebar">                <h4 class="h4border"><img src="../../../images/listtitle.png">学院概况</h4>				 <ul class="main_ul">                                                   <li class="main_li"><div class="main_a"><a href="../../xyjj/index.htm">学院简介</a></div></li>                                                                      <li class="main_li"><div class="main_a"><a href="../../yzjy/index.htm">院长寄语</a></div></li>                                                                       <li class="main_li"><div class="main_a"><a href="javascript:;">学院机构</a></div>                  <ul class="sec_li">                                    <li><i class="icon-star-empty"></i><a href="../../xyjg/lddw/index.htm">领导队伍</a></li>                                    <li><i class="icon-star-empty"></i><a href="../../xyjg/xzjg2/index.htm">行政机构</a></li>                                    <li><i class="icon-star-empty"></i><a href="../../xyjg/jxjg/index.htm">教学机构</a></li>                                    <li><i class="icon-star-empty"></i><a href="../../xyjg/kyjg/index.htm">科研机构</a></li>                                    <li><i class="icon-star-empty"></i><a href="../../xyjg/xsjg/index.htm">学术机构</a></li>                                    </ul>                  </li>                                                                       <li class="main_li"><div class="main_a"><a href="javascript:;">师资力量</a></div>                  <ul class="sec_li">                                    <li><i class="icon-star-empty"></i><a class="active" href="index.htm">专职教师</a></li>                                    <li><i class="icon-star-empty"></i><a href="../jzjs/index.htm">兼职教师</a></li>                                    </ul>                  </li>                                                      <div class="clearfix"></div>               </ul>              <div class="clearfix"></div>            </div>          </div>                                 </div>                <div class="span8">          <div class="mainleft_box ">                 				<h4 class="h4border">专职教师</h4>                                   <div class="MsoNormal" style="line-height: 150%; margin-left: 10.5pt"><div class="MsoNormal" style="line-height: 150%; margin-left: 10.5pt"><div class="MsoNormal" style="line-height: 150%; margin-left: 10.5pt"><p><span style="font-size:18px"><span style="font-family:宋体"><strong><span style="color:black">教&nbsp;授</span></strong></span></span></p><p><br><span style="font-size:16px"><span style="font-family:宋体"><span style="color:black"><a href="http://faculty.bjtu.edu.cn/1092/">施先亮</a>&nbsp;&nbsp;</span></span></span><a href="http://faculty.bjtu.edu.cn/6389/" style="font-family: 宋体; font-size: 16px;">张瑞萍</a><span style="font-size:16px"><span style="font-family:宋体"><span style="color:black"> &nbsp;<a href="http://faculty.bjtu.edu.cn/7279/">毕&nbsp;</a></span><a href="http://faculty.bjtu.edu.cn/7279/">颖</a>&nbsp;&nbsp;</span></span><span style="font-size:16px"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/1584/">张长青</a>&nbsp;&nbsp;<a href="http://faculty.bjtu.edu.cn/1587/">南玉霞</a>&nbsp;&nbsp;<a href="http://faculty.bjtu.edu.cn/5875/">高晓莹</a></span></span></p><p><span style="font-size:16px"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/7841/">吴文嫔</a>&nbsp;&nbsp;</span></span><a href="http://faculty.bjtu.edu.cn/8186/" style="font-family: 宋体; font-size: 16px;">陶&nbsp;杨</a>&nbsp; &nbsp; &nbsp;&nbsp;<a href="http://faculty.bjtu.edu.cn/8622/" style="font-family: 宋体; font-size: 16px;">郭&nbsp;烁</a></p><p>&nbsp;</p><p><br><span style="font-size:18px"><span style="font-family:宋体"><strong><span style="color:black">副教授</span></strong></span></span></p><p><br><span style="font-family: 宋体; font-size: 16px; color: black;"><a href="http://faculty.bjtu.edu.cn/5997/">郑&nbsp;</a></span><a href="http://faculty.bjtu.edu.cn/5997/" style="font-family: 宋体; font-size: 16px;">翔</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><a href="http://faculty.bjtu.edu.cn/6984/" style="font-family: 宋体; font-size: 16px;">王世海</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/6173/" style="font-family: 宋体; font-size: 16px;">栾志红</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/7668/" style="font-family: 宋体; font-size: 16px;">李文华</a>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<span style="font-size:16px"><span style="font-family:宋体"><span style="color:black"><a href="http://faculty.bjtu.edu.cn/6178/">陈力铭</a></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/6226/" style="font-family: 宋体; font-size: 16px;">贺旭红</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span></p><p><span style="font-size:16px"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/7694/">朱本欣</a></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><a href="http://faculty.bjtu.edu.cn/7780/" style="font-family: 宋体; font-size: 16px;">王&nbsp;霞</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/7843/" style="font-family: 宋体; font-size: 16px;">张保华</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/8190/" style="font-family: 宋体; font-size: 16px;">孙向齐</a>&nbsp;<span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/8190/" style="font-family: 宋体; font-size: 16px;">孙向齐</a><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><a href="http://faculty.bjtu.edu.cn/8185/" style="font-family: 宋体; font-size: 16px;">李巍涛</a></p><p><a href="http://faculty.bjtu.edu.cn/8101/" style="font-family: 宋体; font-size: 16px;">杨&nbsp;军</a><span style="font-family: 宋体; font-size: 16px;">&nbsp; &nbsp;</span><a href="http://faculty.bjtu.edu.cn/8866/" style="font-family: 宋体; font-size: 16px;">蔡曦蕾</a></p><p><span style="font-size:16px"><span style="font-family:宋体">&nbsp;&nbsp;</span></span><span style="font-size:16px"><span style="font-family:宋体">&nbsp;</span></span></p><p><br><span style="font-size:18px"><span style="font-family:宋体"><strong><span style="color:black">讲&nbsp;师</span></strong></span></span></p><p><br><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><span style="color:black"><a href="http://faculty.bjtu.edu.cn/6177/">许庆彤</a></span></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/6055/">张春雨</a></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><span style="color:black"><a href="http://faculty.bjtu.edu.cn/7692/">徐晓峰</a></span></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><span style="color:black"><a href="http://faculty.bjtu.edu.cn/8361/">马&nbsp;</a></span><a href="http://faculty.bjtu.edu.cn/8361/">宁</a></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/8439/">周&nbsp;琼</a></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/7953/">高建学</a></span></span></span></p><p><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/8360/">夏晓红</a></span></span></span><span style="font-family: 宋体; font-size: 16px;">&nbsp;&nbsp;</span><font color="#000000">&nbsp;</font><span style="font-size:16px"><span style="line-height:2"><span style="font-family:宋体"><a href="http://faculty.bjtu.edu.cn/8736/">郑&nbsp;飞</a>&nbsp; &nbsp;<a href="http://faculty.bjtu.edu.cn/9273/">吕宁宁</a></span></span></span></p><p>&nbsp;</p><p>&nbsp;</p></div></div></div>                                                                                                       <div class="clearfix"></div>                       </div>                                                                              </div>              </div>                   <div class="row-fluid bgblue">                <div class="span12">                   <div class="leftbox_top">                             <div class="project">                    		<h4 class="h4border"><img src="../../../images/linktitle.png">相关链接</h4>                   					   <div class="link">                           <div class="link_l"><p>学术网站：</p></div>                           <div class="link_r"><p>                                                         <a href="http://www.bjtu.edu.cn/pub/skjsyjy/">            北京社会建设研究院     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.chinalegaleducation.com/">            中国法学教育网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.jus.cn/index.asp">            中国法理网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.calaw.cn/">            中国宪政网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.criminallaw.com.cn/">            中国刑事法律网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.civillaw.com.cn/">            中国民商法律网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        </p></div>                            <div class="clearfix"></div>                       </div>					   <div class="clearfix"></div>										   <div class="link">                           <div class="link_l"><p>数据库：</p></div>                           <div class="link_r"><p>                                                         <a href="http://www.zgfxqk.org.cn/Index.shtml">            中国法学期刊网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://vip.chinalawinfo.com/">            北大法律信息网     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.faxuejia.org.cn/CN/volumn/home.shtml">            《法学家》杂志     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://www.wipo.int/wipolex/zh">            WIPO知识产权法律与条约数据库     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        </p></div>                            <div class="clearfix"></div>                       </div>					   <div class="clearfix"></div>										   <div class="link">                           <div class="link_l"><p>校内网站：</p></div>                           <div class="link_r"><p>                                                         <a href="http://www.njtu.edu.cn/">            北京交通大学     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://jwc.bjtu.edu.cn/">            教务处     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://gs.njtu.edu.cn/cms/">            研究生院     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://lib.njtu.edu.cn/">            图书馆     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        <a href="http://zhixing.bjtu.edu.cn/forum.php">            知行信息交流平台     </a>&nbsp;&nbsp;&nbsp;&nbsp;                                                        </p></div>                            <div class="clearfix"></div>                       </div>					   <div class="clearfix"></div>					 	              			       </div>          </div>                </div>              </div>     <div id="push"></div>    </div> <!-- /wrap -->          <div id="footer">        <p><b>地址：北京市海淀区上园村3号 &nbsp;&nbsp;&nbsp;&nbsp;  邮编：100044 &nbsp;&nbsp;&nbsp;&nbsp;  联系电话：010-51688714  &nbsp;&nbsp;&nbsp;&nbsp; Email:bjtulaw@bjtu.edu.cn </b></p>        <p> 备案号:BJTUICP备12120303号 &nbsp;&nbsp;&nbsp;&nbsp;  北京交通大学法学院 &nbsp;&nbsp; All Rights Reserved. </p>      </div>         <!-- Le javascript    ================================================== -->    <!-- Placed at the end of the document so the pages load faster --><!--    <script src="../assets/js/jquery.js"></script>    <script src="../assets/js/bootstrap-transition.js"></script>    <script src="../assets/js/bootstrap-alert.js"></script>    <script src="../assets/js/bootstrap-modal.js"></script>    <script src="../assets/js/bootstrap-dropdown.js"></script>    <script src="../assets/js/bootstrap-scrollspy.js"></script>    <script src="../assets/js/bootstrap-tab.js"></script>    <script src="../assets/js/bootstrap-tooltip.js"></script>    <script src="../assets/js/bootstrap-popover.js"></script>    <script src="../assets/js/bootstrap-button.js"></script>    <script src="../assets/js/bootstrap-collapse.js"></script>    <script src="../assets/js/bootstrap-carousel.js"></script>    <script src="../assets/js/bootstrap-typeahead.js"></script>        -->  </body>
# """

s = """
<body><center><table align="center" border="0" cellpadding="0" cellspacing="0" width="890">  <!--DWLayoutTable-->  <tbody><tr>    <td height="103" valign="top" width="890"><table style="margin-top:20px" border="0" cellpadding="0" cellspacing="0" width="100%">      <!--DWLayoutTable-->      <tbody><tr>        <td height="83" width="260"><img src="/images/logo.gif" alt="北京交通大学建筑与艺术系" height="83" width="260"></td>        <td style="line-height:22px;" align="right" width="630">		|		&nbsp;&nbsp;<a href="/index.asp" target="_self">首 页</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/content/main.asp?classid=27">学院概况</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/content/main.asp?classid=28">师资队伍</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/content/main.asp?classid=29">本科生工作</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/content/main.asp?classid=30">研究生工作</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/content/main.asp?classid=31">学科与实验室</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/xsgz/index.asp" target="_new">学生工作</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="/dangjian/index.asp" target="_new">党建之窗</a>&nbsp;&nbsp;|		 <br>		 <span style="padding-right:1px;"><a href="http://aad.bjtu.edu.cn/en/index.asp" target="_new">ENGLISH VERSION</a></span></td>      </tr>	  	   <tr>        <td colspan="2" align="center" height="220" valign="middle" width="890"><object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=7,0,19,0" align="middle" height="190" width="874">            <param name="movie" value="/images/flash.swf">            <param name="quality" value="high">            <embed src="/images/flash.swf" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" align="middle" height="190" width="874">        </object></td>      </tr>    </tbody></table></td>  </tr>  <tr>    <td height="335" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%">      <!--DWLayoutTable-->      <tbody><tr>	  <td style="padding-right:10px;padding-left:3px;" valign="top" width="184">	  <div id="side_menu_item">	  	  <ul class="side_menu">	                                <li><a href="/content/unit_teacher.asp?unit_name=建筑系" class="wlink">•&nbsp;&nbsp;建筑系</a></li>							                                <li><a href="/content/unit_teacher.asp?unit_name=城市规划系" class="wlink">•&nbsp;&nbsp;城市规划系</a></li>							                                <li><a href="/content/unit_teacher.asp?unit_name=媒体与设计艺术系" class="wlink">•&nbsp;&nbsp;媒体与设计艺术系</a></li>							                              <li><a href="../index.asp">•&nbsp;&nbsp;返回主页</a></li>														</ul>	</div>								  </td>	          <td height="450" valign="top" width="706">		<div id="main_right">		<table border="0" cellpadding="0" cellspacing="0" width="706">      <!--DWLayoutTable-->      <tbody><tr>        <td height="40" valign="top" width="706"><table border="0" cellpadding="0" cellspacing="0" width="100%">          <!--DWLayoutTable-->          <tbody><tr>            <td align="right" background="../images/blank.gif" height="40" valign="middle" width="706">			<div class="subtitle" align="left">&nbsp;师资队伍 &gt;&gt; 教学团队</div>			 </td>            </tr>        </tbody></table></td>      </tr>      <tr>        <td style="padding:10px 30px;" align="left" height="410" valign="top">				        <div style="height:30px;padding:5px 30px;">                         </div>	<div id="rightMain_body">				<p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><p></p><table align="center" bgcolor="#999999" border="0" cellpadding="3" cellspacing="1" width="580">                                      <tbody><tr bgcolor="#cccccc">                      <td align="center" height="30" valign="center" width="80"><strong>姓名</strong></td>                      <td align="center" height="30" valign="center" width="88"><strong>职称</strong></td>                      <td align="center" valign="center" width="135"><strong>电话</strong></td>                      <td align="center" valign="center" width="228"><strong>E-Mail</strong></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=dongxiaofeng" target="_blank">董晓峰</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:xfdong@bjtu.edu.cn" title="xfdong@bjtu.edu.cn">xfdong@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=dongyuxiang" target="_blank">董玉香</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51683713</span></td>                      <td align="left" width="228"><a href="mailto:yxdong@bjtu.edu.cn" title="yxdong@bjtu.edu.cn">yxdong@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=hanlinfei" target="_blank">韩林飞</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">010-51684196</span></td>                      <td align="left" width="228"><a href="mailto: hanlf@bjtu.edu.cn; usi2000@126.com" title=" hanlf@bjtu.edu.cn; usi2000@126.com"> hanlf@bjtu.edu.cn; usi2000@126.com</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=hanxiang" target="_blank">韩翔</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51684916</span></td>                      <td align="left" width="228"><a href="mailto:xhan@bjtu.edu.cn" title="xhan@bjtu.edu.cn">xhan@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=jiangyinan" target="_blank">姜忆南</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51683713</span></td>                      <td align="left" width="228"><a href="mailto:ynjiang@bjtu.edu.cn" title="ynjiang@bjtu.edu.cn">ynjiang@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=mengxiaoying" target="_blank">蒙小英</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:xymeng@bjtu.edu.cn" title="xymeng@bjtu.edu.cn">xymeng@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=wanglijun" target="_blank">王丽君</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">本人已调到北京理工大学设计与艺术学院工作</span></td>                      <td align="left" width="228"><a href="mailto:6120180162@bit.edu.cn" title="6120180162@bit.edu.cn">6120180162@bit.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=wangmin" target="_blank">王珉</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51684916</span></td>                      <td align="left" width="228"><a href="mailto:minwang@bjtu.edu.cn" title="minwang@bjtu.edu.cn">minwang@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=xiahaishan" target="_blank">夏海山</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">010-51687259</span></td>                      <td align="left" width="228"><a href="mailto:hshxia@bjtu.edu.cn" title="hshxia@bjtu.edu.cn">hshxia@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=yixiao" target="_blank">易晓</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">010-51684916</span></td>                      <td align="left" width="228"><a href="mailto:xyi@bjtu.edu.cn" title="xyi@bjtu.edu.cn">xyi@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=zhanghonghong" target="_blank">张红红</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">010-51684916</span></td>                      <td align="left" width="228"><a href="mailto:hhzhang@bjtu.edu.cn" title="hhzhang@bjtu.edu.cn">hhzhang@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=baoyinghua" target="_blank">鲍英华</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">01051683913</span></td>                      <td align="left" width="228"><a href="mailto:yhbao@bjtu.edu.cn" title="yhbao@bjtu.edu.cn">yhbao@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=changgong" target="_blank">常工</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51683913</span></td>                      <td align="left" width="228"><a href="mailto:chg7239@126.com" title="chg7239@126.com">chg7239@126.com</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=chenlan" target="_blank">陈岚</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51684538</span></td>                      <td align="left" width="228"><a href="mailto:lchen2@bjtu.edu.cn" title="lchen2@bjtu.edu.cn">lchen2@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=chenyongquan" target="_blank">陈泳全</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:chenyongquan@bjtu.edu.cn" title="chenyongquan@bjtu.edu.cn">chenyongquan@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=duxiaohui" target="_blank">杜晓辉</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:xhdu@bjtu.edu.cn" title="xhdu@bjtu.edu.cn">xhdu@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=gaowei" target="_blank">高巍</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text">51683705</span></td>                      <td align="left" width="228"><a href="mailto:wgao2@bjtu.edu.cn" title="wgao2@bjtu.edu.cn">wgao2@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=genghan" target="_blank">耿涵</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:hgeng@bjtu.edu.cn" title="hgeng@bjtu.edu.cn">hgeng@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=huyingdong" target="_blank">胡映东</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:ydhu@bjtu.edu.cn" title="ydhu@bjtu.edu.cn">ydhu@bjtu.edu.cn</a></td>                    </tr>				  				  								                    <tr bgcolor="#ffffff">                      <td align="center" height="19" width="80"><a href="tea_preview.asp?teacher_id=lixujia" target="_blank">李旭佳</a></td>                      <td align="center" width="88"><span class="teacherInfo_text">副教授</span></td>                      <td align="center" width="135"><span class="teacherInfo_text"></span></td>                      <td align="left" width="228"><a href="mailto:xjli@bjtu.edu.cn" title="xjli@bjtu.edu.cn">xjli@bjtu.edu.cn</a></td>                    </tr>				  				</tbody></table>				          <div id="pageDiv"> <a href="/content/unit_teacher.asp?Page=1&amp;teacher_name=&amp;unit_name=">第一页</a>                             <a href="/content/unit_teacher.asp?Page=0&amp;teacher_name=&amp;unit_name=">上一页</a>                             <a href="/content/unit_teacher.asp?Page=2&amp;teacher_name=&amp;unit_name=">下一页</a>                             <a href="/content/unit_teacher.asp?Page=3&amp;teacher_name=&amp;unit_name=">最后一页</a>&nbsp;                             <input name="teacher_name" value="" type="hidden">					每页20条/共53条&nbsp;当前第1页/共3页				</div>	</div>		</td>      </tr>    </tbody></table>		</div>		</td>      </tr>          </tbody></table></td>    </tr>  <tr>    <td height="75" valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%">      <!--DWLayoutTable-->      <tbody><tr>        <td height="17" width="890"><img src="/images/botlinegif.gif" alt="" height="17" width="890"></td>      </tr>      <tr>        <td style="padding:2px 18px 0 0;" align="right" height="58" valign="top">SCHOOL OF ARCHITECTURE AND DESIGN. All RIGHTS RESERVED | COPYRIGHT © 2019 BEIJING JIAOTONG UNIVERSITY<br>          2019 北京交通大学建筑与艺术学院 版权所有 | 学院信箱: saad@bjtu.edu.cn|备案号：BJTUICP设备12113001</td>      </tr>    </tbody></table></td>  </tr></tbody></table></center></body>
"""

# lianji = re.findall('href="(.*?details\/\d{8})', s)
lianji = re.findall("(?isu)(http\://[a-zA-Z0-9\.\?/&\=\:]+)",s)

print(lianji)