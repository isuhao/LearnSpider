#-*- coding: utf-8 -*-
__author__ = 'ZhaoYu'
# Try to crawl all pictures and info of http://www.mzitu.com and then
# store them at local
import urllib
import urllib2
import re
import os


class Spider(object):
    def __init__(self, sum_page):
        self.root_url = "http://www.mzitu.com/all"
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def get_all_urls(self):
        """ get all pictures' urls from root url
        argument: root_url [str] root url
        return: urls_list [list] list of urls of pictures
        """
        print "I am getting the url list of pictures..."
        request = urllib2.Request(self.root_url, headers=self.headers)
        response = urllib2.urlopen(request)
        content = response.read()  # get the content of root webpage

        pattern = re.compile(
            'href="(http://www.mzitu.com/\d+)" target="_blank">', re.S)
        url_lists = re.findall(pattern, content)
        return url_lists

    def savePic(self, pic_url_list, path):
        """save picture to local
        argument:
            pic_url_list: [list] list of the picture address online
        return:
            None
        """
        # print pic_url_list
        for pic_url in pic_url_list:
            u = urllib.urlopen(pic_url)
            data = u.read()
            file_name = pic_url.split('/')[-1]
            f = open(path+'/'+file_name, 'wb')
            f.write(data)
            f.close()

    def saveInfo(self, pic_title, pic_class, pic_label_list, path):
        """save picture info to local txt file
        argument:
            pic_title [str] the title of the girl's webpage
            pic_class [str] the class of the girl's webpage
            pic_label_list [list] the labels of the girl's webpage
        return:
            None
        """
        with open(path+'/'+'girl_info', 'w') as f:
            f.write(pic_title + '\n' + pic_class + '\n')
            for pic_label in pic_label_list:
                f.write(pic_label + '\t')

    def get_items(self, pic_url):
        """get items of each page, items are title, class, tags, pictures
            argument:
               pic_url: [str] the url of a girl
            return: 
                info: [list] each element means each girl's info, which is 
                             titile, class, tags, pictures, and both shape of tags
                             and pictures are lists
        """

        print "I am crawling info of page {} ...".format(pic_url)
        request = urllib2.Request(pic_url, headers=self.headers)
        response = urllib2.urlopen(request)
        content = response.read()  # get the content of the girl's webpage

        pattern = re.compile(
            '<h2 class="main-title">(.*?)</h2>.*?rel="category tag">(.*?)</a>.*?rel="tag">(.*?)</a>', re.S)
        items = re.findall(pattern, content)
        pic_title = items[0][0]
        pic_class = items[0][1]
        pattern = re.compile('rel="tag">(.*?)</a>')
        pic_label_list = re.findall(pattern, content)

        pattern = re.compile("<span class='dots'>.*?<span>(.*?)</span>", re.S)
        pic_sum_num = int(re.findall(pattern, content)[0])
        pattern = re.compile('<img src="(.*?)" alt=".*?" />', re.S)
        pic_num_url = re.findall(pattern, content)[0]
        pic_url_list = []
        for num in range(pic_sum_num):
            num += 1
            if num < 10:
                new_pic_url = pic_num_url.replace('1.jpg', str(num) + '.jpg')
            else:
                new_pic_url = pic_num_url.replace('01.jpg', str(num) + '.jpg')
            pic_url_list.append(new_pic_url)

        info = [pic_title, pic_class, pic_label_list, pic_url_list]

        return info

    def Mztu_Spider(self):
        """contains main steps to get all pictures' urls and
        then crawl all info and store them at local
        """
        #--------------------------------
        # step1: get all picutues' urls
        #--------------------------------
        url_list = self.get_all_urls()
        num = 0
        for url in url_list:
            num+=1
            #--------------------------------
            # step2: crawl all intrested info
            #--------------------------------
            pic_title, pic_class, pic_label_list, pic_url_list = self.get_items(url)
            print "I have crawled {} girls info ...".format(num)
            #--------------------------------
            # step3: store them at local
            #--------------------------------
            try:
                os.path.isdir(str(num))
            except:
                raise NameError
            os.mkdir(str(num))
            path=os.getcwd()+'/'+str(num)
            self.savePic(pic_url_list, path)
            self.saveInfo(pic_title, pic_class, pic_label_list, path)
            print "I have stored {} girls info at local".format(num)

if __name__ == "__main__":
    sum_page = 40
    spider = Spider(sum_page)
    spider.Mztu_Spider()
