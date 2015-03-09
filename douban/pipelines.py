# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban.utils.avos_manager import *

class DoubanPipeline(object):
    def __init__(self):
        self.avosManager = AvosManager()

    def process_item(self, item, spider):
        print item['name']
        dataDict = {"name":item['name'],"date":item['date'],
                    "start_time":item['start_time'],"end_time":item['end_time'],"ticket":item['ticket'],
                    "region":item['region'],
                    "location":item['location'],
                    "category":item['category'],
                    "source" : item['source']}

        try:
            self.avosManager.saveActivity(dataDict)
        except:
            print "avos exception!"

        return item
