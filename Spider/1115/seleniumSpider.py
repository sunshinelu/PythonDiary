# -*- coding: utf-8 -*-
# D:\drivers\chromedriver.exe
import codecs

import sys
from PIL import Image, ImageEnhance
from lxml import etree
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import string
import zipfile
import os
import re
import datetime
from datetime import timedelta
# 打码
import json, time, requests


class YDMHttp(object):
    apiurl = 'http://api.yundama.com/api.php'
    username = 'superdudu_01'
    password = 'mima8612648'
    appid = 9079
    appkey = '2f7ada7149d19860e708798b32d80c3'

    def __init__(self, username, password, appid, appkey):
        self.username = username
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response

    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    def report(self, cid):
        data = {'method': 'report', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid), 'flag': '0'}
        response = self.request(data)
        if (response):
            return response['ret']
        else:
            return -9001

    def post_url(self, url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb');
        res = requests.post(url, files=files, data=fields)
        return res.text


def shibie(file_name):
    # 普通用户的用户名和密码
    username = '***'
    password = '***'

    # 开发者id和密钥
    appid = 5119
    appkey = 'bc95a4b139c2d2523231381d97998500'

    filename = file_name
    codetype = 3000
    timeout = 60

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        yundama = YDMHttp(username, password, appid, appkey)
        cid, result = yundama.decode(filename, codetype, timeout);
        return result


def gen_dates(b_date, days):
    day = timedelta(days=1)
    # print(day)
    for i in range(days):
        # print(b_date + day*i)
        yield b_date + day*i


def main(start_date, end_date, parentID, childID,Type):
    option = webdriver.ChromeOptions()
    # browser = webdriver.Chrome(executable_path="chromedriver.exe") # For windows
    browser = webdriver.Chrome() # for Mac
    errorFile = open("error.log", "w")
    errorFile.truncate()
    errorFile.close()
    try:
        errorFile = open("error.log", "w")
        errorFile.write("start\n")
        errorFile.close()
        f_list = os.listdir()
        f_splits = []
        for i in f_list:
            if os.path.splitext(i)[1] == ".json" and str(os.path.splitext(i)[0]).startswith(childID):
                f_splits.append(os.path.splitext(i)[0].split("_")[1])
        if len(f_splits) != 0:
            start_date = f_splits[-1]

        option = webdriver.ChromeOptions()
        # option.add_argument("--start-maximized")
        # option.add_extension(proxy_auth_plugin_path)
         # for windows
        # browser = webdriver.Chrome() # for mac

        browser.maximize_window()
        browser.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB")
        # 左侧勾选
        browser.find_element_by_xpath('//div[@class="opt"]/input[@value="清除"]').click()

        browser.find_element_by_css_selector('div#'+Type+' span img#'+Type+'first').click()
        if start_date is not None:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if end_date is None:
            end = datetime.datetime.now()
        else:
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        for d in gen_dates(start, ((end - start).days + 1)):
            file = codecs.open(childID+"_"+d.strftime("%Y-%m-%d")+".json", 'w', encoding='utf-8')
            # 开始时间
            browser.find_element_by_id("publishdate_from").click()
            browser.find_element_by_id("publishdate_from").send_keys(d.strftime("%Y-%m-%d"))
            # 结束时间
            browser.find_element_by_id("publishdate_to").click()
            browser.find_element_by_id("publishdate_to").send_keys(d.strftime("%Y-%m-%d"))
            time.sleep(1)
            xpathStr = "//dl[@id='"+parentID+"']/dl[@id='"+childID+"']/preceding-sibling::dd[1]/a"
            browser.find_element_by_xpath(xpathStr).click()
            browser.find_element_by_xpath('//div[@class="btnPlace2"]/input[@id="btnSearch"]').click()
            WebDriverWait(browser, 2000).until(EC.visibility_of(browser.find_element(by=By.ID, value='iframeResult')))
            browser.switch_to.frame("iframeResult")
            time.sleep(4)
            browser.find_element_by_xpath('//div[@id="id_grid_display_num"]/a[3]').click()
            time.sleep(4)
            urls = "https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=%s&dbname=%s&filename=%s"
            nums = 0
            time.sleep(2)
            while(nums<=2):
                time.sleep(1)
                while("请输入验证码" in str(browser.page_source)):
                    if("验证码错误" in str(browser.page_source)):
                        break
                    # 2、截取屏幕内容，保存到本地
                    # browser.save_screenshot("01.png")
                    # 3、打开截图，获取验证码位置，截取保存验证码
                    imgelement = browser.find_element_by_xpath('//img[@id="CheckCodeImg"]')
                    imgelement.screenshot('01.png')
                    imageCode = Image.open("01.png")  # 图像增强，二值化
                    # imageCode.load()
                    sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)
                    sharp_img.save("02.png")
                    sharp_img.load()  # 对比度增强
                    time.sleep(2)
                    username = 'superdudu_01'
                    password = 'mima8612648'
                    appid = 9079
                    appkey = '2f7ada7149d19860e708798b32d80c34'
                    filename = "02.png"
                    codetype = 1005
                    timeout = 60
                    yundama = YDMHttp(username, password, appid, appkey)
                    cid, result = yundama.decode(filename, codetype, timeout)
                    #     CheckCode
                    time.sleep(2)
                    browser.find_element_by_xpath('//input[@id="CheckCode"]').send_keys(result)
                    time.sleep(1)
                    browser.find_element_by_xpath('//input[@id="CheckCode"]/following-sibling::input[1]').click()
                    time.sleep(1)

                while("验证码错误" in str(browser.page_source)):
                    nums = nums+1
                    if(nums>=2):
                        print("验证码输入错误次数过多！")
                        browser.close()
                        break
                    browser.save_screenshot("01.png")
                    # 3、打开截图，获取验证码位置，截取保存验证码
                    # CheckCodeImg
                    # 获取验证码的长宽
                    imgelement = browser.find_element_by_xpath('//img[@id="CheckCodeImg"]')
                    imgelement.screenshot('01.png')
                    imageCode = Image.open("01.png")  # 图像增强，二值化
                    # imageCode.load()
                    sharp_img = ImageEnhance.Contrast(imageCode).enhance(2.0)
                    sharp_img.save("02.png")
                    sharp_img.load()  # 对比度增强
                    time.sleep(2)
                    username = 'superdudu_01'
                    password = 'mima8612648'
                    appid = 9079
                    appkey = '2f7ada7149d19860e708798b32d80c34'
                    filename = "02.png"
                    codetype = 1005
                    timeout = 60
                    yundama = YDMHttp(username, password, appid, appkey)
                    cid, result = yundama.decode(filename, codetype, timeout)
                    #     CheckCode
                    time.sleep(1)
                    browser.find_element_by_xpath('//input[@id="CheckCode"]').send_keys(result)
                    time.sleep(2)
                    browser.find_element_by_xpath('//input[@id="CheckCode"]/following-sibling::input[1]').click()
                    time.sleep(1)
                time.sleep(2)
                t_selector = Selector(text=browser.page_source)
                time.sleep(1)
                titleUrls = t_selector.xpath("//table[@class='GridTableContent']/tbody/tr[contains(@bgcolor,'#f')]").extract()
                # if(len(titleUrls)== 0):
                #     browser.switch_to.default_content()
                #     print("1")
                #     break
                for url in titleUrls:
                    selectUrl = etree.HTML(url.replace('\n', ''))
                    title = selectUrl.xpath("string(//tr/td[2])").strip()
                    author = selectUrl.xpath("string(//tr/td[3])").strip()
                    source = selectUrl.xpath("string(//tr/td[4])").strip()
                    timeDate = selectUrl.xpath("string(//tr/td[5])").strip()
                    dbName = selectUrl.xpath("string(//tr/td[6])").strip()
                    # upload = "0" if len(selectUrl.xpath("//tr/td[8]/text()")) == 0 else selectUrl.xpath("//tr/td[8]/text()")[
                    #     0].strip()
                    detailUrlXpath =selectUrl.xpath("//a[@class='fz14']//@href")
                    detailUrl = "" if len(detailUrlXpath) == 0 else detailUrlXpath[0].strip()
                    reObject = re.match(".*FileName=([A-Z0-9]+).*DbName=([A-Z_]+).*DbCode=([A-Z]+).*", detailUrl)
                    try:
                        fileName = reObject.group(1)
                        Dbname = reObject.group(2)
                        Dbcode = reObject.group(3)
                    except:
                        filename = ""
                        Dbname = ""
                        Dbcode = ""
                    realUrl = urls % (Dbcode, Dbname, fileName)
                    dict = {"title":title,"author":author,"detailUrl":realUrl,"source":source,"dbName":dbName,"timeDate":timeDate}
                    line = json.dumps(dict, ensure_ascii=False) + "\n"
                    file.write(line)
                time.sleep(4)
                if(len(browser.find_elements_by_xpath('//a[@id="Page_next"]')) == 0):
                    browser.switch_to.default_content()
                    print("2")
                    break
                WebDriverWait(browser, 4000).until(EC.visibility_of(browser.find_element_by_xpath('//a[@id="Page_next"]')))
                time.sleep(4)
                browser.find_element_by_xpath('//a[@id="Page_next"]').click()
            file.close
    except Exception as e:
        errorFile = open("error.log", "w")
        errorFile.write("exceptions\n")
        browser.close()
        errorFile.close()


if __name__ == '__main__':
        main(sys.argv[1:])
#     start_date = '2018-04-06'
#     end_date = '2018-04-10'
#     main(start_date, end_date,"Echild","E059child","E")
#     # 传入参数
#     # python .\seleniumSpider.py '2018-03-01' '2018-03-02' 'Achild' 'A004child'
#     # main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
#
#
#
#
# # if int(infoNum) <= 20: