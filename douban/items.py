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


