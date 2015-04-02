# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field

class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    date = Field()
    start_time = Field()
    end_time = Field()
    ticket = Field()
    region = Field()
    location = Field()
    category = Field()
    source = Field()
    pass

class DbMoiveItem(Item):
    name=Field()#电影
    score=Field()#豆瓣评分
    summary=Field()#电影简介
    classification=Field()#类型
    poster=Field()#海报
    source = Field()

class DzdpItem(Item):
    name=Field()#餐厅名称
    score=Field()#评分
    address=Field()#地点
    popularity=Field()#名人去过
    source = Field()

class WdjItem(Item):
    name = Field()#应用名称
    category = Field() #分类
    source = Field()

class AppStoreItem(Item):
    name = Field()#应用名称
    category = Field() #分类
    source = Field()
