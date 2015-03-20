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

    #By Hushuying,generate footprint
    def gen_footprint(self,item):
        str_item = str(item['name'])+item['start_time']['iso']+\
                   item['region']+str(item['ticket'])+\
                   str(item['location']['latitude'])+\
                   str(item['location']['longitude'])+\
                   str(item['date']['iso'])
        return self.avosManager.calMD5(str_item)

    def process_item(self, item, spider):
        if spider.name not in ['damai','douban']:
            return item
        print item['name']
        dataDict = {"name":item['name'],"date":item['date'],
                    "start_time":item['start_time'],"end_time":item['end_time'],"ticket":item['ticket'],
                    "region":item['region'],
                    "location":item['location'],
                    "category":item['category'],
                    "source" : item['source']}


        try:
            foot_print = self.gen_footprint(item)

            if not self.res_dict.has_key(item['name'].decode('utf-8')):
               self.avosManager.saveActivity(dataDict)
               print '插入数据'
            elif foot_print != self.res_dict[item['name'].decode('utf-8')]:
               self.avosManager.updateDataByName('activities',item['name'],dataDict)
               print '更新数据'
            else:
               print '已存在'
        except:
            print "avos exception!"

        return item


class DbMoviePipeline(object):
    def __init__(self):
        self.avosManager = AvosManager()
        self.res_dict = self.avosManager.getnfdict()

     #By Hushuying,generate footprint
    def gen_footprint(self,item):
        str_item = str(item['name'])+\
                   str(item['score'])+\
                   str(item['summary'])+\
                   str(item['poster'])+\
                   str(item['classification'])
        return self.avosManager.calMD5(str_item)

    def process_item(self, item, spider):
        if spider.name not in ['dbmovie']:
            return item
        print item['source']
        dataDict = {"name":item['name'],"score":item['score'],
                    "summary":item['summary'],
                    "classification":item['classification'],
                    "poster":item['poster'],
                    "source" : item['source']}


        try:
            foot_print = self.gen_footprint(item)

            if not self.res_dict.has_key(item['name'].decode('utf-8')):
               self.avosManager.saveData('dbmovie',dataDict)
               print '插入数据'
            elif foot_print != self.res_dict[item['name'].decode('utf-8')]:
               self.avosManager.updateDataByName('dbmovie',item['name'],dataDict)
               print '更新数据'
            else:
               print '已存在'
        except:
            print "avos exception!"

        return item


if __name__ == "__main__":
        dp = DoubanPipeline()
