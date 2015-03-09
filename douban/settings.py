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


DOWNLOADER_MIDDLEWARES = {
    #'douban.download_middleware.duplicatefiltermiddware.DuplicatesFilterMiddleware': 500,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'douban.download_middleware.custom_retry_middleware.CustomRetryMiddleware': 500,
    'douban.download_middleware.rotate_useragent.RotateUserAgentMiddleware': 500,
    'douban.download_middleware.rotate_useragent.ProxyMiddleware': 500
}

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = '/Users/batulu/PycharmProjects/douban/douban/log/douban.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douban (+http://www.yourdomain.com)'
