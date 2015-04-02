# -*- coding: utf-8 -*-
from selenium.common.exceptions import WebDriverException, TimeoutException

__author__ = 'batulu'
from scrapy.contrib.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban.items import AppStoreItem
from douban.utils.util_opt import *
from selenium import webdriver



import time


class AppStoreSpider(CrawlSpider):
    name = 'appstore'
    category_dict = {}

    def __init__(self):
        self.start_urls = []
        self.init_start_url()



    def init_start_url(self):
        #报刊杂志二级分类
        letter_list=['A','B','C','D','E','F','G',
                     'H','I','J','K','L','M','N',
                     'O','P','Q','R','S','T','U',
                     'V','W','X','Y','Z']
        url='https://itunes.apple.com/cn/genre/ios/id36?mt=8'
        newpage=get_source(url)
        soup=BeautifulSoup(newpage)
        toplevel_list = soup.find_all(attrs={'class':'top-level-genre'})
        for url in toplevel_list:
            if url.get_text() == u'游戏':
                first_category = url.get_text()
                seclevel_list = soup.find_all(attrs={'class':'list top-level-subgenres'})
                li_list = seclevel_list[0].find_all('li')
                for li in li_list:
                    for letter in letter_list:
                        key_url = li.a.get('href')+'&letter='+letter
                        category = first_category+'/'+li.get_text()
                        self.category_dict[key_url] = category
                        self.start_urls.append(key_url)
                        print 'url % s ,category %s' %(key_url,category)
            elif url.get_text() == u'报刊杂志':
                first_category = url.get_text()
                seclevel_list = soup.find_all(attrs={'class':'list top-level-subgenres'})
                li_list = seclevel_list[1].find_all('li')
                for li in li_list:
                    for letter in letter_list:
                        key_url = li.a.get('href')+'&letter='+letter
                        category = first_category+'/'+li.get_text()
                        self.category_dict[key_url] = category
                        self.start_urls.append(key_url)
                        print 'url % s ,category %s' %(li.a.get('href')+'&letter='+letter,first_category+'/'+li.get_text())
            else:
                for letter in letter_list:
                     key_url = url.get('href')+'&letter='+letter
                     category = url.get_text()
                     self.category_dict[key_url] = category
                     self.start_urls.append(key_url)
                     print 'url %s,category %s'%(url.get('href')+'&letter='+letter,url.get_text())

    def parse(self, response):
        if self.category_dict.has_key(response.url):
            category = self.category_dict[response.url]
        else:
            category = response.meta['category']
        soup=BeautifulSoup(response.body)
        app_list = soup.find(attrs={'id':'selectedcontent'}).find_all('li')
        for app in app_list:
            print app.a.get_text()
            item = AppStoreItem()
            item['name'] = app.a.get_text().strip().encode('utf-8')
            item['category'] = category
            item['source'] = AppStoreSpider.__name__
            yield item
        next = soup.find(attrs={'class':'paginate-more'})
        if next != None:
            next_page = soup.find(attrs={'class':'paginate-more'}).get('href')
            print 'next_url %s'%next_page
            request = Request(next_page, callback=self.parse)
            request.meta['category'] =  category
            yield request


if __name__ == "__main__":
    #报刊杂志二级分类
    # letter_list=['A','B','C','D','E','F','G',
    #              'H','I','J','K','L','M','N',
    #              'O','P','Q','R','S','T','U',
    #              'V','W','X','Y','Z']
    # url='https://itunes.apple.com/cn/genre/ios/id36?mt=8'
    # newpage=get_source(url)
    # soup=BeautifulSoup(newpage)
    # toplevel_list = soup.find_all(attrs={'class':'top-level-genre'})
    # for url in toplevel_list:
    #     if url.get_text() == u'游戏':
    #         first_category = url.get_text()
    #         seclevel_list = soup.find_all(attrs={'class':'list top-level-subgenres'})
    #         li_list = seclevel_list[0].find_all('li')
    #         for li in li_list:
    #             for letter in letter_list:
    #                 print 'url % s ,category %s' %(li.a.get('href')+'&letter='+letter,first_category+'/'+li.get_text())
    #     elif url.get_text() == u'报刊杂志':
    #         first_category = url.get_text()
    #         seclevel_list = soup.find_all(attrs={'class':'list top-level-subgenres'})
    #         li_list = seclevel_list[1].find_all('li')
    #         for li in li_list:
    #             for letter in letter_list:
    #                 print 'url % s ,category %s' %(li.a.get('href')+'&letter='+letter,first_category+'/'+li.get_text())
    #     else:
    #         for letter in letter_list:
    #             print 'url %s,category %s'%(url.get('href')+'&letter='+letter,url.get_text())

    newpage=get_source("https://itunes.apple.com/cn/genre/ios-bao-kan-za-zhi-lu-you-yu-de-yu/id13029?mt=8&letter=T")
    soup=BeautifulSoup(newpage)
    app_list = soup.find(attrs={'id':'selectedcontent'}).find_all('li')
    for app in app_list:
        print app.a.get_text()
    # seclevel_list = soup.find_all(attrs={'class':'list top-level-subgenres'})
    # for url in seclevel_list:
    #     li_list = url.find_all('li')
    #     for li in li_list:
    #         for letter in letter_list:
    #             print 'url % s ,category %s' %(li.a.get('href')+'&letter='+letter,li.get_text())
    #     #print 'url %s,category %s'%(url.get('href'),url.get_text())

