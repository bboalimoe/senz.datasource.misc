# -*- coding: utf-8 -*-
import re

__author__ = 'batulu'
    #url = 'http://t.dianping.com/list/beijing-category_1'
from scrapy.contrib.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban.items import  DzdpItem
from douban.utils.util_opt import *
from json import *
import time
import requests
from scrapy.settings import Settings
import os
import random

headers = { "User-Agent": " Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Host": "t.dianping.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Cookie":"Hm_lvt_9c7f4d9b7c00cb5aba2c637c64a41567=1421654832,1421728515,1421827791,1421982989; tma=88525828.4893887.1420332716520.1421901287602.1421982989863.14; tmd=91.88525828.4893887.1420332716520.; nforum-left=00100; left-index=00000000000; main[UTMPUSERID]=batulu12; main[UTMPKEY]=41480197; main[UTMPNUM]=16797; Hm_lpvt_9c7f4d9b7c00cb5aba2c637c64a41567=1422001897; main[PASSWORD]=o%257E%257Fi%252C%250D%2528%257C%257D%2504U%255C%2540uKLB%251E%2529%251D%250A%2523%2509%2508; main[XWJOKE]=hoho; bfd_session_id=bfd_g=b56c782bcb75035d00006ef20011174a54a88f0d; tmc=1.88525828.74332260.1421986459313.1421986459313.1421986459313",
            "Referer":"http://t.dianping.com/",
            "X-Requested-With":"XMLHttpRequest"
}

class DzdpSpider(CrawlSpider):
    name = 'dzdp'

    def __init__(self):
        self.start_urls = []
        self.mcid={'shanghai':1,'beijing':2,'guangzhou':4,'shenzhen':7,'wuhan':16,
                   'tianjin':10,'xian':17,'nanjing':5,'hangzhou':3,'chengdu':8,'chongqing':9,
                   'suzhou':6,'ningbo':11,'hefei':110,'shenyang':18,'dalian':19}

        self.ncid={u'上海':'shanghai',u'北京':'beijing',u'广州':'guangzhou',
                  u'深圳':'shenzhen',u'武汉':'wuhan',u'天津':'tianjin',
                  u'西安':'xian',u'南京':'nanjing',u'杭州':'hangzhou',
                  u'成都':'chengdu',u'重庆':'chongqing',u'苏州':'suzhou',
                  u'宁波':'ningbo',u'合肥':'hefei',u'沈阳':'shenyang',
                  u'大连':'dalian'}
        self.host = 'http://t.dianping.com'
        self.init_start_url()
        # dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        # settings = Settings({'LOG_FILE': dir_path+'/'+self.name+'.log'})
        # settings.overrides['LOG_FILE'] = {'Accept':'text/heml,application/xhtml+xml;q=0.9,*/*;q=0.8','Accept-Language':'ch',}



    def init_start_url(self):

        for k,v in self.ncid.items():
            url = 'http://t.dianping.com/list/%s-category_1'%(v)
            print url
            self.start_urls.append(url)

    def parse(self, response):
        soup=BeautifulSoup(response.body)
        allItem=soup.find_all(attrs={'class':'tg-floor-title'})

        if len(allItem) > 0:
            #list page
            for theitem in allItem:
                if theitem != None:
                    url = self.host + theitem.get('href')
                    request = Request(url, callback=self.parse)
                    request.meta['name'] =  theitem.h3.get_text()
                    #get name id
                    name_re = re.compile(r'http\:\/\/t\.dianping\.com\/deal\/(\d+)')
                    name_id = re.findall(name_re,url)
                    request.meta['name_id'] = name_id[0]
                    #get cityid
                    city_re = re.compile(r'http\:\/\/t\.dianping\.com\/list\/(\w+)-category_1\.*')
                    city_id = re.findall(city_re,response.url)
                    if len(city_id) > 0:
                        request.meta['city_id'] = city_id[0]
                    else:
                        request.meta['city_id'] =''
                    yield request

            next_page = soup.find_all(attrs={'class':'tg-paginator-next'})[0].get('href')
            #http://t.dianping.com/list/beijing-category_1?pageIndex=1
            catergorycn_re = re.compile(r'(http\:\/\/t\.dianping\.com\/list\/\w+-category_1)\.*')
            catergory_list = re.findall(catergorycn_re,response.url)


            if len(catergory_list) > 0:
                next_page = catergory_list[0]+next_page
                yield Request(next_page, callback=self.parse)
            #detail page
        else:
            title = response.meta['name']
            score = soup.find(attrs={'class':'star-rate'}).get_text().strip().encode('utf-8')
            print title
            print score

            #get the address
            name_id = response.meta['name_id']
            print name_id
            if self.mcid.has_key(response.meta['city_id']):
                city_id = self.mcid[response.meta['city_id']]
                print city_id
                pageurl = "http://t.dianping.com/ajax/dealGroupShopDetail?" \
                      "dealGroupId=%s&cityId=%s&action=shops&page=%s"%(name_id,city_id,"1")
                session = requests.session()
                jsonpage =(session.get(pageurl,headers=headers,timeout = 3)).text
                json_dict = JSONDecoder().decode(jsonpage)
                time.sleep(5)
                if json_dict['msg'].has_key('pages'):
                    pages = json_dict['msg']['pages']
                    address = ''
                    for adr in json_dict['msg']['shops']:
                            address = address + adr['address']+';'

                    for page in range(2,pages+1):
                        pageurl = "http://t.dianping.com/ajax/dealGroupShopDetail?" \
                          "dealGroupId=%s&cityId=%s&action=shops&page=%s"%(name_id,city_id,str(page))
                        jsonpage =(session.get(pageurl,headers=headers,timeout = 3)).text
                        json_dict = JSONDecoder().decode(jsonpage)
                        time.sleep(5)
                        for adr in json_dict['msg']['shops']:
                            address = address +adr['address']+';'
                else:
                    address = json_dict['msg']['shops']
            else:
                address = ''


            item = DzdpItem()
            item['name'] = title
            item['score'] = score
            item['address'] = address
            print address
            item['popularity'] = ''
            item['source'] = DzdpSpider.__name__
            yield item
        pass

if __name__ == "__main__":
        # br = webdriver.PhantomJS()
        # br.get('http://movie.douban.com/')
        # time.sleep(2.5)
        # print br.find_elements_by_class_name('more')[0]
        # link = br.find_elements_by_class_name('more')[0]
        # link.click()
        # print br.page_source

        # category = ['热门','经典','日本','最新','可播放','豆瓣高分',
        #             '冷门佳片','华语','欧美','韩国','动作','喜剧',
        #             '科幻','悬疑','恐怖','成长']
        #url = 'http://movie.douban.com/tag/%s'%(category_list[0])
        #print url
        # stri = u'有一个地方只有我们知道 (豆瓣)'
        # stri.strip(u'(豆瓣)')
        # print stri
        # url = 'http://t.dianping.com/list/beijing-category_1'
        # newpage=get_source(url)
        # soup=BeautifulSoup(newpage,"html.parser")
        # url = soup.find_all(attrs={'class':'tg-floor-title'})
        # y = soup.find_all(attrs={'class':'tg-paginator-next'})[0].get('href')
        #  #http://t.dianping.com/list/beijing-category_1?pageIndex=1
        # catergorycn_re = re.compile(r'(http\:\/\/t\.dianping\.com\/list\/beijing-category_1)\?.*')
        # catergory_list = re.findall(catergorycn_re,'http://t.dianping.com/list/beijing-category_1?pageIndex=1')
        # city_re = re.compile(r'http\:\/\/t\.dianping\.com\/list\/(\w+)-category_1\.*')
        # city = re.findall(city_re,'http://t.dianping.com/list/beijing-category_1')
        # name_re = re.compile(r'http\:\/\/t\.dianping\.com\/deal\/(\d+)')
        # name = re.findall(name_re,'http://t.dianping.com/deal/6390770')

        #get the address
        session = requests.session()
        pageurl = "http://t.dianping.com/ajax/dealGroupShopDetail?" \
              "dealGroupId=%s&cityId=%s&action=shops&page=%s"%("5018451","2","1")
        #jsonpage =get_source(pageurl)
        print pageurl
        jsonpage =session.get(pageurl,headers=headers,timeout = 3).text
        print jsonpage
        json_dict = JSONDecoder().decode(jsonpage)
        time.sleep(random.randint(1,5))
        # print jsonpage
        # if json_dict['msg'].has_key('pages'):
        #     pages = json_dict['msg']['pages']
        #     for item in json_dict['msg']['shops']:
        #             print item['address']
        #     for page in range(2,pages+1):
        #         pageurl = "http://t.dianping.com/ajax/dealGroupShopDetail?" \
        #           "dealGroupId=%s&cityId=%s&action=shops&page=%s"%("6152153","19",str(page))
        #         jsonpage =get_source(pageurl)
        #         json_dict = JSONDecoder().decode(jsonpage)
        #         for item in json_dict['msg']['shops']:
        #             print item['address']
        # else:
        #     print json_dict['msg']['shops']

        if json_dict['msg'].has_key('pages'):
                pages = json_dict['msg']['pages']
                address = ''
                for adr in json_dict['msg']['shops']:
                        address = address + adr['address']+';'

                for page in range(2,pages+1):
                    pageurl = "http://t.dianping.com/ajax/dealGroupShopDetail?" \
                      "dealGroupId=%s&cityId=%s&action=shops&page=%s"%("5018451","2",str(page))
                    jsonpage =(session.get(pageurl,headers=headers,timeout = 3)).json()
                    json_dict = JSONDecoder().decode(jsonpage)
                    time.sleep(random.randint(1,5))
                    for adr in json_dict['msg']['shops']:
                        address = address +adr['address']+';'
        else:
            address = json_dict['msg']['shops']
        print address
        # jp = json.dumps(jsonpage)
        # print jp
        # if len(catergory_list) > 0:
        #     next_page = catergory_list[0]+y
        # print next_page
        # for theitem in url:
        #         #print theitem
        #         if theitem != None:
        #             print theitem.get('href')
        #
        #             print theitem.h3.get_text()
        # url = 'http://t.dianping.com/deal/6390770'
        # newpage=get_source(url)
        # soup=BeautifulSoup(newpage,"html.parser")
        # score = soup.find(attrs={'class':'star-rate'}).get_text().strip().encode('utf-8')
        # print score
        # score = soup.find(attrs={'class':'star-rate'}).get_text().strip().encode('utf-8')
        #http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId=10853868&cityId=1&action=shops&page=2&regionId=0
        pass