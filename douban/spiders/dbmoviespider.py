# -*- coding: utf-8 -*-
__author__ = 'batulu'
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban.items import DbMoiveItem
from douban.utils.util_opt import *
import requests
import re
import pycurl
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )


import time


class DbMovieSpider(CrawlSpider):
    name = 'dbmovie'

    def __init__(self):
        self.start_urls = []
        self.init_start_url()

    def init_start_url(self):
        category_list=[
        '爱情',	'喜剧',	'动画',	'科幻',
        '剧情',	'动作',	'经典',	'青春',
        '悬疑',	'犯罪',	'惊悚',	'文艺',
        '纪录片','励志',	'搞笑',	'恐怖',
        '战争',	'短片',	'魔幻',	'黑色幽默',
        '传记',	'情色',	'动画短片',	'感人',
        '暴力',	'音乐',	'童年',	'家庭',
        '黑帮',	'同志',	'女性',	'浪漫',
        '史诗',	'童话',	'烂片',	'cult']
        for category in category_list:
            url = 'http://movie.douban.com/tag/%s'%(category)
            print url
            self.start_urls.append(url)

    def parse(self, response):
        #print response.body.decode(response.encoding)
        #print response.body

        soup=BeautifulSoup(response.body)
        allMovieInfo=soup.find_all(attrs={'class':'item'})
        if len(allMovieInfo) > 0:
            for movieInfo in allMovieInfo:
                if movieInfo.a != None:
                    print movieInfo.a.get('href')
                    yield Request(movieInfo.a.get('href'), callback=self.parse)
            next_page = soup.find_all(attrs={'rel':'next'})
            if len(next_page) > 0:
                next_page =next_page[0].get('href')
                print next_page
                yield Request(next_page, callback=self.parse)
        else:
            # title = soup.find(attrs={'property':'v:itemreviewed'}).get_text().strip().encode('utf-8')
            # summary = soup.find(attrs={'property':'v:summary'}).get_text().strip().encode('utf-8')
            # score = soup.find(attrs={'class':'ll rating_num'}).get_text().strip().encode('utf-8')
            # poster = soup.find(attrs={'class':'j a_show_login lnk-sharing'}).get('data-image')
            # cf_list = soup.find_all(attrs={'property':'v:genre'})
            # classification = ''
            # for ci in cf_list:
            #     classification = classification + ci.get_text().strip().encode('utf-8')+'/'
            # print title
            # print summary
            # print score
            # print poster
            # print classification
            # item = DbMoiveItem()
            # item['name'] = title
            # item['score'] = score
            # item['summary'] = summary
            # item['classification'] = classification
            # item['poster']= poster
            # item['source'] = DbMovieSpider.__name__
            # yield item
            temp = response.url
            id_re = re.compile(r'http\:\/\/movie\.douban\.com\/subject\/(\d+)\/')
            dbMovieID = re.findall(id_re,temp)
            if len(dbMovieID)>0:
                # url = 'http://apiparser.avosapps.com/dbmovie/%s/update' % dbMovieID[0]
                # print url
                get_url = 'http://apiparser.avosapps.com/dbmovie/%s' % dbMovieID[0]
                # requests.post(url)
                session = requests.session()
                newpage=session.get(get_url)
                print newpage.text
                json_obj = json.loads(newpage.text)
                f = open('moviename.txt','a')
                #f = file('moviename.txt','w')
                print json_obj['name']
                f.write(json_obj['name']+'\r\n')
                f.close()
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
        # url = 'http://movie.douban.com/subject/1297863/'
        # newpage=get_source(url)
        # soup=BeautifulSoup(newpage,"html.parser")
        # cf_list = soup.find_all(attrs={'property':'v:genre'})
        # classification = ''
        # for ci in cf_list:
        #     classification = classification + ci.get_text().strip().encode('utf-8')+'/'
        # print classification
        # stri = u'有一个地方只有我们知道 (豆瓣)'
        # stri.strip(u'(豆瓣)')
        # print stri
        temp = 'http://movie.douban.com/subject/6875263/'
        id_re = re.compile(r'http\:\/\/movie\.douban\.com\/subject\/(\d+)\/')
        dbMovieID = re.findall(id_re,temp)
        print dbMovieID
        url = 'http://apiparser.avosapps.com/dbmovie/%s/update' % dbMovieID[0]
        print url
        get_url = 'http://apiparser.avosapps.com/dbmovie/%s' % dbMovieID[0]
        # requests.post(url)
        session = requests.session()
        newpage=session.get(get_url)
        print newpage.text
        json_obj = json.loads(newpage.text)
        f = open('moviename.txt','a')
        print json_obj['name']
        f.write(json_obj['name']+'\r\n')
        f.write(json_obj['name']+'\r\n')
        f.write(json_obj['name']+'\r\n')
        f.close()
        # pc = pycurl.Curl()
        # pc.setopt(pycurl.POST, 1)
        # pc.setopt(pycurl.URL, url)
        # pc.perform()
        # pc.close()
        pass