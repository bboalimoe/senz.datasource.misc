# -*- coding: utf-8 -*-

# Scrapy settings for douban project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'
ITEM_PIPELINES = ['douban.pipelines.DoubanPipeline']

# Retry many times since proxies often fail
RETRY_TIMES = 10
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

DOWNLOADER_MIDDLEWARES = {
    #'douban.download_middleware.duplicatefiltermiddware.DuplicatesFilterMiddleware': 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 300,
    #'douban.download_middleware.custom_retry_middleware.CustomRetryMiddleware': 500,
    'douban.download_middleware.rotate_useragent.RotateUserAgentMiddleware': 100,
    'douban.download_middleware.rotate_useragent.ProxyMiddleware': 200
    #'douban.download_middleware.retry.RetryMiddleware': 200
}

DOWNLOAD_DELAY = 0.25 # 250 ms of delay

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = '/Users/batulu/PycharmProjects/spider/douban/log/douban.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'
