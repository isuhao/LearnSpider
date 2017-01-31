#-*- coding: utf-8 -*-
__author__ = 'ZhaoYu'
# Learn to use crawler, the script is to scrawl data from www.qiushibaike
import urllib
import urllib2
import re
# start_page = 1
# url = 'http://www.qiushibaike.com/hot/page/' + str(start_page)
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent': user_agent}
# request = urllib2.Request(url, headers=headers)
# response = urllib2.urlopen(request)
# content = response.read().decode('utf-8')
# pattern = re.compile(
#     '<div class="article block untagged mb15".*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>.*?<div class="single-clear"></div>', re.S)
# items = re.findall(pattern, content)
# for item in items:
#     print "author: " + item[0]
#     print "content: " + item[1]
#     print "zan_num: " + item[2]
#     print "comment_num: " + item[3]
#     print '----------------------------------'


class QSBK_Spider(object):
    def __init__(self, sum_page):
        self.start_page = 1
        self.root_url = 'http://www.qiushibaike.com/hot/page/'

    def get_page_content(self, page_num):
        """get all content of specified page
        parameters: 
                page_num: [num] the num of page
        return 
                content: [str] all content  
        """
        print "I am getting contents of page {}...".format(page_num)
        url = self.root_url + str(page_num)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request)
            content = response.read()
            # print content
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败,错误原因", e.reason
                return None

    def get_items(self, content):
        """get items of each page, items are author, content, zan_num, content_num
        	argument:
        		content: [str] content of specified page
        	return: 
        		items: [list] each items 
        """
        
        f=open("QiuBai.txt",'a')
        pattern = re.compile(
        '<div class="article block untagged mb15".*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>.*?<div class="single-clear"></div>', re.S)
        items = re.findall(pattern, content)
        for item in items:
            # print "author: " + item[0]
            # print "content: " + item[1]
            # print "zan_num: " + item[2]
            # print "comment_num: " + item[3]
            # print '------------------------------------------------------'
            f.write("author: "+item[0]+'\n'+
            	    "content: " + item[1]+'\n'+
            	    "zan_num: " + item[2]+'\n'+
            	    "comment_num: " + item[3]+'\n\n'            	    )
        f.close()



    def start_crawl(self):
        for num in range(sum_page):
            # step1: get webpage contents
            num += 1  # start from 1
            content = self.get_page_content(num)
            # step2: get interested contents
            self.get_items(content)
            # step3: store them into a .txt file


if __name__ == "__main__":
    # step1: define initial varibles
    sum_page = 10
    # step2: create an object of spider
    spider = QSBK_Spider(sum_page)
    # step3: start to crawl and store it in txt file
    spider.start_crawl()
