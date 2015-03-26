__author__ = 'batulu'
from twisted.python.log import FileLogObserver
from scrapy import signals
from twisted.python import log
import logging


class SpiderLog(object):

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls()
        crawler.signals.connect(obj.setup_logfile, signal=signals.spider_opened)
        return obj

    def setup_logfile(self, spider):
        logfile = '/Users/batulu/PycharmProjects/spider/douban/log/production_%s.log' % spider.name
        fl = FileLogObserver(open(logfile, 'w+'))
        fl.start()
        # logging.basicConfig(level=logging.INFO, filemode='w', filename='log.txt')
        # observer = log.PythonLoggingObserver()
        # observer.start()