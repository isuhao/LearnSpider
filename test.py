#-*- coding: utf-8 -*-
# author: zhaoyu
# date: 2017.03.08
# 本脚本是http://www.itokoo.com/read.php?tid=31396的爬虫代码，用于将爱图客上ISHOW
# 子栏的所有图片名、下载链接、预览图等信息采集到本地

import os
import os
import requests
from bs4 import BeautifulSoup


soup=BeautifulSoup(open('2.html'), 'lxml')

#find the descprition info
# info=soup.find('font', size="2").encode('utf-8') #encode the tag
# new_info=info.replace('http://www.itokoo.com/','piaoliangmm') 
# print new_info

#find all thumbnails url
# thumbnails=soup.find_all('span', class_="f12")
# for thumnail in thumbnails:
#     print thumnail.find('img').get('src').split('/')[-1]

# name=soup.title.string.split(' - ')[0].replace('/', '_')
# print name
# os.mkdir(name)

download_links=soup.find_all('a',class_="down")
for link in download_links:
    if link.string.encode('utf-8').find('百度')!=-1:
        download_link=link.get('href')
        download_code=link.next_sibling
download_stuff={'link':download_link,'code': download_code}
with open('download.txt','wb') as f:
    f.write(download_stuff['link']+'\t'+download_stuff['code'].encode('utf-8'))
    f.write('\n')



