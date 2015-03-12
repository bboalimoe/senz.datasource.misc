# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban.utils.avos_manager import *

class DoubanPipeline(object):
    def __init__(self):
        self.avosManager = AvosManager()
        self.res_dict = self.avosManager.getnfdict()

    def process_item(self, item, spider):
        print item['name']
        dataDict = {"name":item['name'],"date":item['date'],
                    "start_time":item['start_time'],"end_time":item['end_time'],"ticket":item['ticket'],
                    "region":item['region'],
                    "location":item['location'],
                    "category":item['category'],
                    "source" : item['source']}


        try:
            foot_print = self.avosManager.gen_footprint(item)
            dataDict['foot_print'] = foot_print
            if not self.res_dict.has_key(item['name']):
               self.avosManager.saveActivity(dataDict)
               print '插入数据'
            elif foot_print != self.res_dict[item['name']]:
               self.avosManager.updateDataByName('activities',item['name'],dataDict)
               print '更新数据'
        except:
            print "avos exception!"

        return item
