# -*- coding: utf-8 -*-
from selenium.common.exceptions import WebDriverException, TimeoutException

__author__ = 'batulu'
from scrapy.contrib.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban.items import WdjItem
from douban.utils.util_opt import *
from selenium import webdriver



import time


class WdjSpider(CrawlSpider):
    name = 'wdj'

    def __init__(self):
        self.start_urls = []
        self.init_start_url()


    def init_start_url(self):
        software_list = ['影音图像','网上购物','阅读学习','常用工具',
           '性能优化','社交网络','办公软件','通讯聊天',
           '美化手机','便捷生活','出行必用','新闻资讯',
           '金融理财','育儿母婴']

        game_list = ['休闲时间','宝石消除','动作射击','儿童益智',
                    '体育格斗','经营策略','跑酷竞速','网络游戏',
                    '扑克棋牌','塔防守卫','角色扮演']


        for software in software_list:
            url = 'http://www.wandoujia.com/tag/%s'%(software)
            print url
            self.start_urls.append(url)

        for game in game_list:
            url = 'http://www.wandoujia.com/tag/%s'%(game)
            print url
            self.start_urls.append(url)

    def parse(self, response):
        try:
            #br = webdriver.PhantomJS()
            br = webdriver.Firefox()
            br.get(response.url)
            time.sleep(10)
            page = 0
            soup=BeautifulSoup(br.page_source)
            appName_list = soup.find_all(attrs={'class':'name'})
            init_num = len(appName_list)
            while True:
                try:
                    link = br.find_element_by_id('j-refresh-btn')
                    soup=BeautifulSoup(br.page_source)
                    temp = soup.find_all(attrs={'class':"last"})
                    numonepage = 12
                    category = ''
                    if len(temp) > 1:
                        category = soup.find_all(attrs={'class':"last"})[1].get_text().strip().encode('utf-8')
                        print category
                    appName_list = soup.find_all(attrs={'class':'name'})
                    if page ==0 :
                        start=0
                    elif page == 1:
                        start = init_num
                    else:
                        start = init_num + numonepage*(page-1)
                    if start >= len(appName_list):
                        break
                    #print start
                    print len(appName_list)
                    for appInd in range(start,len(appName_list)):
                        item = WdjItem()
                        item['name'] = appName_list[appInd].get_text().strip().encode('utf-8')
                        item['category'] = category.strip().encode('utf-8')
                        item['source'] = WdjSpider.__name__
                        yield item
                    link.click()
                    time.sleep(10)
                    page = page + 1

                except:
                    break
            br.quit()
        except (WebDriverException, TimeoutException):
            try:
                br.quit()
            except AttributeError:
                pass

        pass


if __name__ == "__main__":
    #br = webdriver.Firefox()
    br = webdriver.PhantomJS()
    #br.get('http://www.wandoujia.com/tag/%E5%BD%B1%E9%9F%B3%E5%9B%BE%E5%83%8F')
    br.get('http://www.wandoujia.com/tag/%E5%BD%B1%E9%9F%B3%E5%9B%BE%E5%83%8F')
    time.sleep(10)
    page = 0
    init_num = 24
    while True:
        link = br.find_element_by_id('j-refresh-btn')
        try:
            soup=BeautifulSoup(br.page_source)
            temp = soup.find_all(attrs={'class':"last"})
            numonepage = 12
            category = ''
            if len(temp) > 1:
                category = soup.find_all(attrs={'class':"last"})[1].get_text().strip().encode('utf-8')
                print category
            appName_list = soup.find_all(attrs={'class':'name'})
            if page ==0 :
                start=0
            elif page == 1:
                start = init_num
            else:
                start = init_num + numonepage*(page-1)
            # if start > len(appName_list):
            #     break
            print start
            print len(appName_list)
            for appInd in range(start,len(appName_list)):
                print appName_list[appInd].get_text()
            link.click()
            time.sleep(10)
            page = page + 1

        except:
            break
