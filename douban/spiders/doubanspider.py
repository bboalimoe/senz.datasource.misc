#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'batulu'
from scrapy.contrib.spiders import CrawlSpider,Rule
from douban.items import DoubanItem
from bs4 import BeautifulSoup
from scrapy.http import Request

import re
from douban.utils.geo_coding import GeoCoder
from douban.utils.util_opt import *

class DoubanSpider(CrawlSpider):
    	def __init__(self):
            self.categoryDict={'音乐':'music','戏剧':"drama",'讲座':"salon",'聚会':"party",'电影':"film",'展览':"exhibition",'运动':"sports",'公益':"commonweal",'旅行':"travel","其他":"others"}
            self.cityList = ["beijing","shanghai","guangzhou"]
            self.timeType = "week"
            self.start_urls = []
            self.init_start_url()
            self.geoCoder = GeoCoder()

        #initlize start_urls
        def init_start_url(self):
            for city in self.cityList:
                for categoryCn,categoryEn in self.categoryDict.iteritems():
                    categoryUrl = "http://%s.douban.com/events/%s-%s" % (city,self.timeType,categoryEn)
                    self.start_urls.append(categoryUrl)
        name = "douban"
        #download_delay = 1

        #parse the response with beautifulsoup
        def parse(self, response):
            #print response.body.decode(response.encoding)
            soup=BeautifulSoup(response.body)
            allEventsInfo=soup.find(attrs={'class':'events-list events-list-pic100 events-list-psmall'}).find_all("li")

            catergorycn_re = re.compile(r'http\:\/\/\w+\.douban\.com\/events\/week-(\w+)')
            catergory_list = re.findall(catergorycn_re,response.url)
            categoryCn = ''
            if len(catergory_list) >0:
                for (k,v) in self.categoryDict.items():
                    if v == catergory_list[0]:
                        categoryCn = k

            for eventInfo in allEventsInfo:
                try:
                    eventTitle = eventInfo.find(attrs={'class':'title'}).get_text().strip().encode('utf-8')
                    eventTimeInfoList = eventInfo.find(attrs={'class':'event-time'}).find_all("time")
                    eventTimeDict = {"startDate":"","endDate":""}
                    for eventTimeInfo in eventTimeInfoList:
                        itemprop = eventTimeInfo["itemprop"]
                        DateTimeInfo = eventTimeInfo["datetime"]
                        if itemprop not in eventTimeDict.keys():
                            continue
                        eventTimeDict[itemprop] = DateTimeInfo.replace("T"," ")
                    eventLocation = eventInfo.find(attrs={'itemprop':'location'}).get("content","")
                except:
                    continue

                try:
                        longitude = float(eventInfo.find(attrs={'itemprop':'longitude'}).get("content",""))
                        latitude = float(eventInfo.find(attrs={'itemprop':'latitude'}).get("content",""))
                except:
                        longitude,latitude = lng,lat = self.geoCoder.geoCoding(eventLocation)
                ticketFee = eventInfo.find(attrs={'class':'fee'}).get_text().strip().encode('utf-8')

                date_time, start_time, end_time = getAvosTimeInfo(eventTimeDict["startDate"], eventTimeDict["endDate"])
                item = DoubanItem()
                item['name'] = eventTitle
                item['date'] = date_time
                item['start_time'] = start_time
                item['end_time'] = end_time
                item['ticket']= ticketFee
                item['region'] = eventLocation
                item['location'] = gps2GeoPoint(latitude,longitude)
                item['category'] = categoryCn
                item['source'] = DoubanSpider.__name__
                yield item



            #nextpage
            nextInfo = soup.find(attrs={'rel':"next"})
            if nextInfo!= None:
                next = nextInfo.get("href","")
            else:
                next = ""
            #http://guangzhou.douban.com/events/week-party
            #http://shanghai.douban.com/events/week-exhibition
            catergory_re = re.compile(r'(http\:\/\/\w+\.douban\.com\/events\/week-\w+)')
            catergory_list = re.findall(catergory_re,response.url)



            if len(catergory_list) > 0:
                categoryUrl = catergory_list[0]
            if next != "":
                nextPageUrl = categoryUrl + next
                print nextPageUrl
                yield Request(nextPageUrl, callback=self.parse)

            #else:
            #    nextPageUrl = ""



