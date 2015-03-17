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

        # stri = '幸福互助-上海话学习与交流-公益'
        # print self.res_dict[stri.decode('utf-8')]
        # print self.res_dict.has_key(stri.decode('utf-8'))
        # if '幸福互助-上海话学习与交流-公益' in self.res_dict:
        #     print 'helo'
        # for (k,v) in self.res_dict.items():
        #     if v == 'ee2fb102c3406de04ccddaa65c09eaca':
        #         if k == '幸福互助-上海话学习与交流-公益':
        #             print 'hello'
        #     if k == '幸福互助-上海话学习与交流-公益':
        #         print v






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


if __name__ == "__main__":
        dp = DoubanPipeline()
