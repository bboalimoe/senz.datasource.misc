#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import urllib
import cookielib
import time
import datetime


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers = { 'User-Agent': ' Chrome/35.0.1916.114 Safari/537.36' }
#global cj,opener,headers

def get_source(url):
        #time.sleep(0.5)
        maxTryTimes = 5
        page=''
        for i in xrange(maxTryTimes):
                try:
                        req=urllib2.Request(url,headers=headers)
                        page=urllib2.urlopen(req,timeout=10).read()
                        # page=urllib2.urlopen(url,timeout=1).read()
                except:
                        print 'request again, retrytimes:%s' % i
                        time.sleep(0.5)
                        continue
                break;
        return page

def get_ajax_source(url,data):
        #time.sleep(0.5)
        maxTryTimes = 2
        page=''
        for i in xrange(maxTryTimes):
                try:
                        req=urllib2.Request(url,post_data,headers)
                        page=urllib2.urlopen(req).read()
                        # page=urllib2.urlopen(url,timeout=1).read()
                except:
                        print 'click problem, retrytimes:%s' % i
                        time.sleep(0.1)
                        continue
                break;
        return page

def timeConvet2utc(beijingTimeStr):
        datetimeTmp = datetime.datetime.strptime(beijingTimeStr,"%Y-%m-%d %H:%M:%S")
        utcTimeStr = (datetimeTmp - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        return utcTimeStr

def getUtcDate(beijingTimeStr):
        date_str = "%s 00:00:00" % beijingTimeStr.split(" ")[0]
        datetimeTmp = datetime.datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S")
        utcTimeStr = (datetimeTmp - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        return utcTimeStr

#By Zhong.zy, Get time info by avos format
def getAvosTimeInfo(startTime,endTime=''):  #存入后台的为UTC时间
        #convert date
        date_utc = getUtcDate(startTime)
        date_iso = date_utc.replace(" ","T") + ".000Z"
        date_time = dict(__type='Date',iso=date_iso)
        #convert start time
        start_utc = timeConvet2utc(startTime)
        start_iso = start_utc.replace(" ","T") + ".000Z"
        start_time = dict(__type='Date',iso=start_iso)
        #convert end time if exist
        if endTime:
                end_utc = timeConvet2utc(endTime)
                end_iso = end_utc.replace(" ","T") + ".000Z"
                end_time = dict(__type='Date',iso=end_iso)
                return date_time, start_time, end_time
        
        return date_time, start_time


#By Zhong.zy Convert to GeoPoint
def gps2GeoPoint(lat,lng):
        return dict(__type='GeoPoint',latitude=lat,longitude=lng)

if __name__=='__main__':
        a,b=getAvosTimeInfo('2014-10-11 11:12:32')

        print a,b
        print gps2GeoPoint(11,32)
        

        
