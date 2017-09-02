#-*- coding: utf-8 -*-
# author: zhaoyu
# date: 2017.03.08
# 本脚本是http://www.itokoo.com/read.php?tid=31396的爬虫代码，用于将爱图客上ISHOW
# 子栏的所有图片名、下载链接、预览图等信息采集到本地

import os
import requests
from bs4 import BeautifulSoup
from Download import request


class itokoo(object):
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        self.root_url = "http://www.itokoo.com/read.php?tid=31364"

    def get_all_pic_link(self):
        """ 得到主页面上，所有套图的文件名和链接
            arugment:
                None
            return: 
                pic_link_list: [list] each link of beauties
        """
        # 巨坑!!! content能自动识别网站编码，优于text
        html = requests.get(self.root_url).content

        soup = BeautifulSoup(html, 'lxml')
        pic_info_list = soup.find('div', class_="f14 mb10").find_all('a')
        pic_link_list = []  # 构造列表存储图片链接
        for pic_info in pic_info_list:
            pic_link_list.append(pic_info['href'])
        for index in range(len(pic_link_list)):
            with open('test.txt', 'a') as f:
                f.write(pic_link_list[index])
                f.write('\n')
        return pic_link_list

    def get_each_pic_info(self, pic_link):
        """scrawl each beauti's download link, code, description and thumbnails
                   argument: 
            pic_link: [str] picture link
           return:
            download_stuff: [dict] the dictionary has 2 elements: 
                            download link and code
            new_info: [str] a string, which is html code and include title, size, 
                            pic numbers, and unzip code.
            thumnails: [list] a list who has the thumnails of the beauty
        """
        html = request.get(pic_link, 3).content
        soup = BeautifulSoup(html, 'lxml')
 

        # store info at local
        try:
            info = soup.find('font', size="2").encode('utf-8')  # encode the tag
        except:
            return
        new_info = info.replace('http://www.itokoo.com/', 'piaoliangmm')

        # find download link and code
        download_links = soup.find_all('a', class_="down")
        for link in download_links:
            if link.string.encode('utf-8').find('百度') != -1:
                download_link = link.get('href')
                download_code = link.next_sibling
        try:
            download_stuff = {'link': download_link, 'code': download_code}
        except:
            return
        
        # create a folder to store info and pictures
        folder_name = soup.title.string.split(' - ')[0].replace('/', '_')       
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        else:
            return

        with open(folder_name + '/' + 'name.txt', 'wb') as f:
            f.write(new_info)

        # find all thumbnails url
        thumbnails = soup.find_all('span', class_="f12")
        for thumnail in thumbnails:
            src_url = thumnail.find('img').get('src')
            img_html = requests.get(src_url)
            pic_name = src_url.split('/')[-1].split('?')[0]
            with open(folder_name + '/' + pic_name, 'ab') as f:
                f.write(img_html.content)
            with open(ensemble_pic + '/' + pic_name , 'ab') as f:
                f.write(img_html.content)

        with open('download.txt', 'ab') as f:
            f.write(folder_name.encode('utf-8') + '\t' + download_stuff['link'] + '\t' +
                    download_stuff['code'].encode('utf-8'))
            f.write('\n')
        return download_stuff


if __name__ == '__main__':
    # step1: 得到主页面上，所有套图的文件名和链接
    # step2: 进入每个套图链接，得到文字说明、预览图、下载链接
    # step3: 保存资料到本地磁盘
    itokoo = itokoo()
    pic_link_list = itokoo.get_all_pic_link()
    num = 0
    print "There are %d links need to be processed in total" % len(pic_link_list)
    
   #create a folder to store all picutres
    ensemble_pic='pic'
    if os.path.exists(ensemble_pic):
        os.removedirs(ensemble_pic)
    os.mkdir(ensemble_pic)

    for pic_link in pic_link_list:
        num += 1
        print 'processing with number: %d ' % num
        itokoo.get_each_pic_info(pic_link)

   
