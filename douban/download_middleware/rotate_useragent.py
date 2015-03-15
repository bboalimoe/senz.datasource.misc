# -*-coding:utf-8-*-

from scrapy import log
import os,sys
reload(sys)
import socket
import time
from scrapy.http import Request
from douban.spiders.doubanspider import  DoubanSpider


import urllib
import urllib2
from urllib2 import URLError, HTTPError

"""避免被ban策略之一：使用useragent池。

使用注意：需在settings.py中进行相应的设置。
"""

import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            #显示当前使用的useragent
            #print "********Current UserAgent:%s************" %ua

            #记录
            log.msg('Current UserAgent: '+ua, level='INFO')
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
       
class ProxyMiddleware(object):

 #       detect_service_url = 'http://xxx.xxx.xxx.xxx/apps/proxydetect.php'
 #       local_ip = 'xxx.xxx.xxx.xxx'
 #       proxy_  = str('http://%s:%s' % (str(item['address']), str(item['port'])))
 #       proxies = {'http':proxy_}
 #       try:
 #          data  = urllib.urlopen(detect_service_url, proxies=proxies).read()
 #       except exceptions.IOError:
 #          raise DropItem("curl download the proxy %s:%s is bad" % (item['address'],str(item['port'])))
 #       if '' == data.strip():
    def __init__(self):
        self.proxy_agent_list = []
        self.proxy_init()
    dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    def proxy_init(self):
        file_handler = open('%s/download_middleware/agent_server'%(self.dir_path),'r')
        proxy_agent_list = file_handler.readlines()

        self.url_list = []
        for proxy_agent in proxy_agent_list:
            proxy_line = proxy_agent.strip('\r\n').split(' ')
            if len(proxy_line) > 1:
                ip = proxy_line[0]
                port = proxy_line[1]

                if self.proxy_verify(ip,port) == True:
                   url = 'http://%s:%s' % (ip,port)
                   #self.url_list.append([ip,port])
                   self.url_list.append(url)
        self.num_proxy = len(self.url_list)
        file_handler.close()

    def proxy_verify(self,domain,port):
        print "正在验证：%s,%s" % (domain,port)

        #验证代理的可用性
        #创建一个TCP连接套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #设置10超时
        sock.settimeout(10)
        try:
            start = time.clock()

            #连接代理服务器
            sock.connect((domain, int(port)))
            last_time = int((time.clock() - start) * 1000)
            sock.close()
            print "%s,%s 验证通过，响应时间：%d ms." % (domain,port,last_time)
            return True
        except Exception, e:
            print "%s,%s 验证失败." % (domain,port)
            return False
           
    def process_request(self, request, spider):
        # while True:
        #    index = random.randint(0, self.num_proxy -1)
        #    if self.proxy_verify(self.url_list[index][0],self.url_list[index][1]) == True:
        #        break
        # url = 'http://%s:%s' % (self.url_list[index][0],self.url_list[index][1])
        # proxy_agent = url
        index = random.randint(0, self.num_proxy -1)
        proxy_agent = self.url_list[index]

        request.meta['proxy'] = proxy_agent
        print request.meta['proxy']

    def process_exception(self,request,exception,spider):
        print '********************************'
        return request

if __name__ == "__main__":
    px = ProxyMiddleware()

