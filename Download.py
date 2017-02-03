import os
import requests
import re
import random
import time


class download:

    def __init__(self):
        self.ip_list = []
        html = requests.get("http://haoip.cc/tiqu.htm")
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
        for ip in iplistn:
            self.ip_list.append(ip.strip())

        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

    def get(self, url, timeout, proxy=None, try_num=6):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA}
        if proxy == None:  # if not use proxy
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                return response
            except:  # if we cannot get response
                if timeout > 0:  # timeout means numbers of trial
                    print "get wrong to response, there still are {} times to try after 10 senconds".format(timeout)
                    time.sleep(10)
                    return self.get(url, timeout, proxy=None, try_num=try_num-1)
                else:
                    print "get wrong to use origin proxy, it will use proxy now..."
                    time.sleep(10)
                    ip = random.choice(self.ip_list)
                    proxy = {'http': ip}
                    return self.get(url, timeout, proxy=proxy, try_num=try_num-1)

        else:
            try:
            	ip=random.choice(self.ip_list)
            	proxy={'http': ip}
            	return requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            except:
            	if try_num>0:
            		print "get wrong to response, there still are {} times to try after 10 senconds".format(timeout)
            		time.sleep(10)
            		return self.get(url, timeout, proxy=proxy, try_num=try_num-1)
            	else:
            		print "proxy does not work, so it tansfers to origin proxy..."
            		return self.get(url, timeout)





            IP = random.choice(self.ip_list)
            proxy = {'http': IP}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
            return response

request=download()
# down = download()
# print down.get('http://www.mzitu.com', 3).headers
