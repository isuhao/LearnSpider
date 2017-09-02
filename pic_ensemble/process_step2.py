#-*- coding: utf-8 -*-
# 这是www.piaoliangmm.cn网站的后台处理脚本,
# 脚本用于从百度网盘获取分享的链接,并生成html文本
# Author: zhaoyu
# Email: zhaoyuafeu@gmail.com
# Date: 2017-3-3

import re
import numpy as np
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime
import time
import win32api  
import win32clipboard as w
import win32con  
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# class PythonOrgSearch(unittest.TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome('C:\Python27\chromedriver.exe')

#     def test_search_in_python_org(self):
#         driver = self.driver
#         driver.get("http://www.python.org")
#         self.assertIn("Python", driver.title)
#         elem = driver.find_element_by_name("q") 
#         elem.send_keys("pycon")
#         elem.send_keys(Keys.RETURN)
#         assert "No results found." not in driver.page_source

#     def tearDown(self):nologin.php
#         self.driver.close()

# if __name__ == "__main__":
#     unittest.main()

def create_html(pic_info,sum_pic,upload_path,yun_link):
    """create a templete html, and each created hmtl just copy and replace
    arg: 
        pic_info: str info of beauty's , pic size pic num 
        sum_pic: list each  name of 4 picture
        upload_path: website path to store pictures
        yun_link: tumple the fisrt element is baiduyun link,
                    the second element is code 
    return: 
        titile: [str] the title of specified beauty
        html: [str] generated html code of specified beauty
    """
    title=pic_info
    html="""
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <span style="color: #FF0000; font-size: 24px;">百度云:
    </span>
    <a href="%s" target="_blank" 
    style="font-size: 24px; text-decoration: underline;">
        <span style="font-size: 24px;">%s
        </span>
    </a> 
    <span style="font-size: 24px;">
        <span style="color: #FF0000; font-size: 24px;">密码:
        </span>
        %s
    </span>
    </p>\n

    <font size="2">[套图编号] : [ISHOW爱秀]爱图客原创写真 2017-03-18 NO.093 余诗婧Jenny<br/>[套图尺寸] : [5760×3840]<br/>[套图大小] : [30+1P/184M]<br/>[解压密码] : <span style="color:#ff0000 ">piaoliangmm</span></font>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    """%(upload_path,sum_pic[0],sum_pic[0],upload_path,sum_pic[1],sum_pic[1],
         upload_path,sum_pic[2],sum_pic[2],upload_path,sum_pic[3],sum_pic[3],
         yun_link[0],yun_link[0],yun_link[1])

    #生成的html内容写入本地txt
    with open('content.txt', 'a') as f:
        f.write(title)
        f.write(html)
        f.close()
    return title, html

def yun_link(file_name='yun.txt'):
    yun_list=[]
    with open(file_name,'rb') as f:
        lines=f.readlines()
        for line in lines:
            regular=re.findall(':(.*?) code:(.*)',line)
            assert len(regular)!=0, "You should change:  lianjie: to link: , mima: to code: "
            yun_list.append(regular[0])
    return yun_list


def setText(aString):#写入剪切板  
    w.OpenClipboard()  
    w.EmptyClipboard()  
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)  
    w.CloseClipboard()  

def paste_Text():
    #自动粘贴剪切板中的内容  
    win32api.keybd_event(17,0,0,0)  #ctrl的键位码是17  
    win32api.keybd_event(86,0,0,0)#v的键位码是86  
    time.sleep(0.1)
    win32api.keybd_event(86,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0) 

def delete_Text():
    #删除剪贴板中的内容
    win32api.keybd_event(17,0,0,0)  #ctrl的键位码是17  
    win32api.keybd_event(65,0,0,0)#a的键位码是65
    time.sleep(0.1)
    win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0) #释放按键  
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.1)
    win32api.keybd_event(8,0,0,0)#a的键位码是65
    win32api.keybd_event(8,0,win32con.KEYEVENTF_KEYUP,0)


if __name__=="__main__":
    # #################################
    # #######step1:生成html文件########
    # #################################
    #加载本地文件信息和图片信息
    folder_info_list=np.load('folder_info_list.npy').tolist()
    all_extract_pic_list=np.load('all_extract_pic_list.npy').tolist()
    upload_path='http://piaoliangmm.cn/zb_users/upload/xiuren/'
    yun_file='yun.txt'
    yun_list=yun_link(yun_file)
    assert len(yun_list)==len(folder_info_list), "you should check weather two txt len euqal"
    
    title_list=[] #构造title列表保存title
    html_list=[] #构造html列表保存html
    for index in range(len(folder_info_list)):
        title, html=create_html(folder_info_list[index], all_extract_pic_list[index], upload_path,yun_list[index])
        title_list.append(title)
        html_list.append(html)
    # ################################
    # ######step2:写入后台文件中########
    # # ################################
    driver=webdriver.Chrome('C:\Python27\chromedriver.exe')
    #------------登录-------------------------------------
    driver.get("http://piaoliangmm.cn/zb_system/login.php")
    username=driver.find_element_by_name("edtUserName")
    password=driver.find_element_by_name("edtPassWord")
    username.send_keys('zhaoyu106')
    password.send_keys("Zhaoyu611113")
    driver.find_element_by_name("btnPost").click()

    #---------添加文章--------------------------
    published_num=100
    for index in xrange(published_num):
        driver.find_element_by_id("aArticleEdt").click()
        title_input=driver.find_element_by_id("edtTitle") #找到title输入框
        # title_input.send_keys(u'[XIUREN秀人网]XR20130911N00010 2013.09.11 刘雪妮Verna[65P59M]') #输入title
        title_input.send_keys(title_list[index].decode('GBK')) #输入title
        html_btn=driver.find_element_by_id("edui23").click() #点击html按钮
        #在正文框内填入内容
        # driver.switch_to_frame("ueditor_0")
        html_input=driver.find_element_by_xpath('//div[@class="CodeMirror-lines"]//pre[last()]')
        delete_Text()
        
        setText(html_list[index].decode('utf-8'))
        paste_Text()
        time.sleep(1)
        # html_input.clear()
        # html_input.send_keys("22222222")
        # driver.switch_to_default_content() #返回上层frame
        #下拉框内选择秀人网
        Select(driver.find_element_by_id("cmbCateID")).select_by_value('10')
        #下拉框内选择草稿
        Select(driver.find_element_by_id("cmbPostStatus")).select_by_value('1')
        #填入发布日期
        time.sleep(1)
        date=datetime.datetime.now()+datetime.timedelta(days=index)
        date_str=date.strftime("%Y-%m-%d %H:%M:%S") #转换格式
        date_input=driver.find_element_by_id("edtDateTime")
        date_input.clear()
        date_input.send_keys(date_str)
        date_input.send_keys(Keys.ENTER) 
        #选择定时发布
        # auto_publisher=driver.find_element_by_xpath("//@imgcheck")
        # result = html.xpath('//li/a[@href="link1.html"]')
        auto_publisher=driver.find_element_by_xpath('//div[@id="response3"]//span[@class="imgcheck"]')
        auto_publisher.click()
        #点击提交按钮
        time.sleep(1)
        driver.find_element_by_id('btnPost').click()
        time.sleep(3)





