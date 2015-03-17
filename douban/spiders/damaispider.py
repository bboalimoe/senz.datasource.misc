#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from bidict import bidict

__author__ = 'batulu'
from scrapy.contrib.spiders import CrawlSpider,Rule
from bs4 import BeautifulSoup
from scrapy.http import Request
from douban.utils.geo_coding import GeoCoder
from douban.utils.util_opt import *
from douban.items import DoubanItem

class DamaiSpider(CrawlSpider):
    def __init__(self):
        self.mcid={u'演唱会':1,u'音乐会':2,u'话剧歌剧':3,u'舞蹈芭蕾':4,u'曲苑杂坛':5,u'体育比赛':6,u'度假休闲':7}
        self.ccid={'流行':9,'摇滚':10,'民族':11,'音乐节':12,'其他演唱会':13,
                  '管弦乐':14, '独奏':15,'室内乐及古乐':16, '声乐及合唱':17, '其他音乐会':18,
                  '话剧 ':19,'歌剧 ':20,'歌舞剧 ':21,'音乐剧 ':22,'儿童剧 ':23,
                  '舞蹈 ':24,'芭蕾 ':25,'舞剧 ':26,
                  '相声 ':27,'魔术 ':28,'马戏 ':29,'杂技 ':30,'戏曲 ':31,'其他曲苑杂坛 ':32,
                  '球类运动':33,'搏击运动':34,'其它竞技':35,
                  '主题公园':36, '风景区':37, '展会':38, '特色体验':39, '温泉':40, '滑雪':41, '游览线路':42, '度假村':43, '代金券':44, '酒店住宿':45
                  }
        self.mcidDict=~bidict(self.mcid)
        self.ccidDict=~bidict(self.ccid)
        self.geoCodingDict = {}
        self.geoCodingDictFile = "./geoCodingDict.txt"
        #self.readGeoCodingDict(self.geoCodingDictFile)
        self.geoCoder = GeoCoder()
        self.start_urls = []
        self.init_start_url()
        self.host = 'http://www.damai.cn'

    name = 'damai'
    # def readGeoCodingDict(self,filePath):
    #             with open(filePath) as fileInput:
    #                     self.geoCodingDict = json.loads(fileInput.read())
    #
    # def updateGeoCodingDict(self,filePath):
    #         with open(filePath,"w") as fileInput:
    #                 geoCodingDictJson = json.dumps(self.geoCodingDict,ensure_ascii=False)
    #                 fileInput.write(geoCodingDictJson)

    def init_start_url(self):
            # get_source('http://www.damai.cn/projectlist.do?mcid=1&ccid=9')
            # print get_source('http://item.damai.cn/66780.html')
            ccidThresh={1:13,2:18,3:23,4:26,5:32,6:35,7:45}
            startMcid=3
            startCcid=21
            mcid=startMcid
            ccid=startCcid

            while mcid<=7:
                    mcidName=self.mcidDict[mcid]
                    while ccid<=ccidThresh[mcid]: #
                            pageIndex=1
                            # index of page keep changing until there is no perform list in the page
                            performListPage='http://www.damai.cn/projectlist.do?mcid=%s&ccid=%s&pageIndex=%s' % (mcid,ccid,pageIndex)
                            print 'init page %s '%(performListPage)
                            self.start_urls.append(performListPage)
                            ccid+=1
                    mcid+=1


    def parse(self,response):
        #判断是否是列表页，
        listPage=response.body
        soup=BeautifulSoup(listPage)
        performList=soup.find(attrs={'id':'performList'})
        if performList == None: # indicate the index of page has come to an end,
            timeInfo=[]
            price=[]
            showpage=response.body
            # showpage=get_source('http://item.damai.cn/70686.html')
            #soup=BeautifulSoup(showpage,"html.parser")
            soup=BeautifulSoup(showpage)

            try:
                    title=soup.find(attrs={'class':'title'}).get_text().strip().encode('utf-8') # get the title
            except:
                    title='待定'
            #print title
            try:
                    location=soup.find(attrs={'itemprop':'location'}).get_text().strip().encode('utf-8') # get the location
            except:
                    location='待定'
            #print location

            try:
                #geocoding
                lng = 0.0
                lat = 0.0
                if location in self.geoCodingDict:
                        lng,lat = self.geoCodingDict[location]
                else:
                        locationList = location.split("-")
                        region = locationList[0].strip()
                        normRegion = region.replace(" ","").replace("（","").replace("）","").replace("(","").replace(")","")
                        if region in self.geoCodingDict:
                                lng,lat = self.geoCodingDict[normRegion]
                        else:
                                lng,lat = self.geoCoder.geoCoding(region)
                                self.geoCodingDict[region] = (lng,lat)
                                if lng==0.0 and lat==0.0 and len(locationList)>1:
                                        city = locationList[1].strip()
                                        if city in self.geoCodingDict:
                                                lng,lat = self.geoCodingDict[city]
                                        else:
                                                lng,lat = self.geoCoder.geoCoding(city)
                                                self.geoCodingDict[city] = (lng,lat)
                        self.geoCodingDict[location] = (lng,lat)

                #print location


                pidList=[]
                timeList=soup.find(attrs={'id':'perform'}).find_all('a') # get the time, which is a list
                for index,eachtime in enumerate(timeList): # get the price for each time
                        pid=eachtime['pid']
                        currentPerformTime = eachtime['time'].encode('utf-8')
                        timeInfo.append(currentPerformTime)

                        # print eachtime['class'],type(eachtime['class'])
                        if eachtime['class']==[u'grey']:
                                price.append('暂无')
                                continue

                        if index>0:
                                data={'type':'33',
                                          'performID':pid,
                                          'business':'1',
                                          'IsBuyFlow':'False',
                                          'sitestaus':'3'}
                                post_data=urllib.urlencode(data)
                                url='http://item.damai.cn/ajax.aspx?' + post_data
                                newpage=get_source(url)
                                soup=BeautifulSoup(newpage,"html.parser")
                                priceLinkList=soup.find_all('a',attrs={'class':True,'price':True})

                        else:
                                priceLinkList=soup.find(attrs={'id':'price'}).find_all('a')
                        priceList=[]
                        for eachlink in priceLinkList:
                                norlizedPrice=eachlink.get_text()
                                norlizedPrice=norlizedPrice.replace(u'暂时无货，登记试试运气~',u' ( 无货 )').replace(u'点击进行预定登记',u' ( 可预定 )')
                                priceList.append(norlizedPrice.encode('utf-8'))
                        price.append(priceList)
                        currentPerformPriceInfo = ",".join(priceList)
                        #no end time
                        date_time,start_time = getAvosTimeInfo(currentPerformTime)
                #print date_time,start_time,currentPerformPriceInfo
            except:
                print 'parse some error'


            item = DoubanItem()
            item['name'] = title
            item['date'] = date_time
            item['start_time'] = start_time
            item['end_time'] = start_time
            item['ticket']= currentPerformPriceInfo
            item['region'] = location
            item['location'] = gps2GeoPoint(lat,lng)
            item['category'] = self.transferDict(response.meta['CateName'])
            item['source'] = DamaiSpider.__name__
            yield item

        else:
            titleList=performList.find_all('h2')
            nextInfo = soup.find(attrs={'class':"next"})
            if nextInfo!= None:
                next = nextInfo.get("href","")
                next_page = self.host + next
                print 'list page %s '%(next_page)
                yield Request(next_page, callback=self.parse)
            else:
                next_page = ''

            catergorycn_re = re.compile(r'http\:\/\/www\.damai\.cn\/projectlist\.do\?mcid=(\d+)&ccid=.*')
            catergory_list = re.findall(catergorycn_re,next_page)
            if len(catergory_list) > 0:
                CateName = self.mcidDict[int(catergory_list[0])]
            else:
                CateName = u'演唱会'
            for each in titleList:
                a=each.find('a')
                print 'detail page %s '%a['href']
                request = Request(a['href'], callback=self.parse)
                request.meta['CateName'] = CateName
                yield request





    def transferDict(self,CateName):

        dataDict = {
        u"演唱会":"音乐",
        u"音乐会":"音乐",
        u"话剧歌剧":"戏剧",
        u"舞蹈芭蕾":"音乐",
        u"曲苑杂坛":"戏剧",
        u"体育比赛":"运动",
        u"度假休闲":"旅行",
        u"儿童亲子":"其他",
        }
        if dataDict.has_key(CateName) == True:
           return dataDict[CateName]
        else:
           return u"其他"


if __name__ == "__main__":
    # catergorycn_re = re.compile(r'http\:\/\/www\.damai\.cn\/projectlist\.do\?mcid=(\d+)&ccid=\d+')
    # catergory_list = re.findall(catergorycn_re,'http://www.damai.cn/projectlist.do?mcid=1&ccid=9')
    # print catergory_list
    ds = DamaiSpider()
    catergorycn_re = re.compile(r'http\:\/\/www\.damai\.cn\/projectlist\.do\?mcid=(\d+)&ccid=.*')
    #catergorycn_re = re.compile(r'http\:\/\/www\.damai\.cn\/projectlist\.do\?mcid=(\d+)&ccid=\d+&pageIndex=\d+')
    catergory_list = re.findall(catergorycn_re,'http://www.damai.cn/projectlist.do?mcid=7&ccid=39')
    print catergory_list
    if len(catergory_list) > 0:
        print int(catergory_list[0])
        CateName = ds.mcidDict[int(catergory_list[0])]
    else:
        CateName = u'演唱会'
    print CateName
    print ds.transferDict(CateName)
