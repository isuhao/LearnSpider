#-*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
from Download import request


class mzitu(object):
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        self.root_url = "http://www.mzitu.com/all"

    def get_all_url(self):
        start_html = request.get(self.root_url, 3).text
        soup = BeautifulSoup(start_html, "lxml")
        contents_list = soup.find('div', class_='all').find_all('a')
        info_list = []
        for content in contents_list:
            # print content
            href = content['href']
            title = content.get_text().replace('?', '_')
            # print title
            each_content = (href, title)
            info_list.append(each_content)
        print "I have gotten all pic urls"
        return info_list

    def get_pictures(self, pic_url):
        pic_html = requests.get(pic_url, headers= self.headers).text
        soup=BeautifulSoup(pic_html, "lxml")
        max_num=soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        pic_url_list=[]
        for num in range(1, int(max_num)+1):
        	new_pic_url=pic_url+'/'+str(num)
        	new_pic_html=request.get(new_pic_url, 3).text
        	soup=BeautifulSoup(new_pic_html, "lxml")
        	real_pic_url=soup.find('img')['src']
        	# print real_pic_url
        	pic_url_list.append(real_pic_url)
        return pic_url_list

    def store_pic(self,pic_info, pic_url_list):
    	if not os.path.exists(pic_info[1]):
    		os.mkdir(pic_info[1])
    	
    	for pic_url in pic_url_list:
    		img_html=request.get(pic_url, 3)
    		img_name=pic_url[-6:-4]
    		f=open(pic_info[1]+'/'+ img_name+'.jpg', 'ab')
    		f.write(img_html.content)
    		f.close()

    def start_crawl(self):
        info_list = self.get_all_url()
        num=0
        for info in info_list:
            num+=1
            pic_url = info[0]
            print "I am dealing with {}".format(pic_url)
            pic_url_list=self.get_pictures(pic_url)
            self.store_pic(info, pic_url_list)
            print "I have processed {} girls' pictures".format(num)


if __name__ == "__main__":
    spider = mzitu()
    spider.start_crawl()
