#!/bin/sh
PATH=$PATH:/Library/Frameworks/Python.framework/Versions/2.7/bin
export PATH
cd /Users/batulu/PycharmProjects/spider/douban
#scrapy crawlall
scrapy crawl dbmovie  --set LOG_FILE=log/dbmovie.log
scrapy crawl douban --set LOG_FILE=log/douban.log
scrapy crawl damai --set LOG_FILE=log/damai.log
scrapy crawl dzdp --set LOG_FILE=log/dzdp.log