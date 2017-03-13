#-*- coding: utf-8 -*-
# author: zhaoyu
# date: 2017.03.08
# 本脚本是http://www.itokoo.com/read.php?tid=31396的爬虫代码，用于将爱图客上ISHOW
# 子栏的所有图片名、下载链接、预览图等信息采集到本地

import os
import requests
from bs4 import BeautifulSoup

class itokoo(object):
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        self.root_url = "http://www.itokoo.com/read.php?tid=31396"

    def get_all_pic_link(self):
        """ 得到主页面上，所有套图的文件名和链接
            arugment:
                None
            return: 
                pic_link_list: [list] each link of beauties
        """
        #巨坑!!! content能自动识别网站编码，优于text
        html = requests.get(self.root_url).content

        soup = BeautifulSoup(html,'lxml')
        pic_info_list=soup.find('div',class_="f14 mb10").find_all('a')
        pic_link_list=[] #构造列表存储图片链接
        for pic_info in pic_info_list:
            pic_link_list.append(pic_info['href'])
        for index in range(len(pic_link_list)):
            with open('test.txt','a') as f:
                f.write(pic_link_list[index])
                f.write('\n')
        return pic_link_list

    def get_each_pic_info(self,pic_link):
        """scrawl each beauti's download link, code, description and thumbnails
		   argument: 
            pic_link: [str] picture link
           return:
            download_stuff: [dict] the dictionary has 2 elements: 
                            download link and code
            description: [list] a list who has title, picture size, unzip code,
                        download postion  and so on infomation
            thumnails: [list] a list who has the thumnails of the beauty
    	"""
        html=requests.get(pic_link).content
        
        # soup=BeautifulSoup(html,'lxml')
        # title=soup.find('h1')
        # title_content=title.get_text().encode('utf-8')
        # # print len(title_content)
        # title_content=title_content.split(']')[1]+']' #delete useless info

        soup=BeautifulSoup(html,'lxml')
        info=soup.find(id="read_tpc")
        print type(info)
        print info
        print info.find(class_="down").get('href')

        




if __name__ == '__main__':
    # step1: 得到主页面上，所有套图的文件名和链接
    # step2: 进入每个套图链接，得到文字说明、预览图、下载链接
    # step3: 保存资料到本地磁盘
    itokoo=itokoo()
    pic_link_list=itokoo.get_all_pic_link()
    itokoo.get_each_pic_info(pic_link_list[0])

    
