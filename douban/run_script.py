__author__ = 'batulu'
# from twisted.internet import reactor
# from scrapy.crawler import Crawler
# from scrapy.settings import Settings
# from scrapy import log,signals
# from douban.spiders.dzdpspider import DzdpSpider
# from scrapy.utils.project import get_project_settings
#
# spider = DzdpSpider()
# settings = get_project_settings()
# settings._overrides
# crawler = Crawler(settings)
# crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
# crawler.configure()
# crawler.crawl(spider)
# crawler.start()
# log.start()
# reactor.run() # the script will block here until the spider_closed signal was sent

from scrapy.crawler import CrawlerProcess
from scrapy import log,signals
from douban.spiders.dzdpspider import DzdpSpider
from scrapy.settings import Settings
from scrapy.crawler import Crawler
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings

from scrapy import cmdline
cmdline.execute("scrapy crawl dzdp --set LOG_FILE=log/dzdp.log".split())  #followall is the spider's name
#cmdline.execute("scrapy crawl damai --set LOG_FILE=log/damai.log".split())  #followall is the spider's name
crawler.spider
# settings = get_project_settings()
# #settings.set('LOG_FILE','/Users/batulu/PycharmProjects/spider/douban/log/dzdp.log')
# spider = DzdpSpider()
# crawler = Crawler(settings)
# crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
# crawler.configure()
# crawler.crawl(spider)
# #log.start()
# #log.start(logfile ='/Users/batulu/PycharmProjects/spider/douban/log/dzdp.log', crawler=crawler)
# crawler.start()

