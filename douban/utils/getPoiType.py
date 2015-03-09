# --*-- encoding=utf-8 --*-- 
import json
import urllib2
import cookielib
import time
import os

GPS_STEP=0.001

PoiTypes=set()
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
headers = { 'User-Agent': ' Chrome/35.0.1916.114 Safari/537.36' }

def get_source(url):
        #time.sleep(0.5)
        maxTryTimes = 5
        page=''
        for i in xrange(maxTryTimes):
                try:
                        req=urllib2.Request(url,headers=headers)
                        page=urllib2.urlopen(req,timeout=10).read()
                except:
                        print 'request again, retrytimes:%s' % i
                        time.sleep(0.5)
                        continue
                break;
        return page

def getPOI(lat, lng):
    url = "http://api.map.baidu.com/geocoder/v2/?coordtype=bd09ll&location=%s,%s&output=json&ak=fPnXQ2dVgLevy7GwIomnhEMg&pois=1" % (lat, lng)
    result_info = get_source(url)
    pois=[]
    if not result_info:
        return pois
    res = json.loads(result_info)
    if 'result' in res:
        res = res['result']
        if 'pois' in res:
            pois=res['pois']
    return pois

def getPoiType(lat, lng):
    pois = getPOI(lat, lng)
    if not pois:
        return False
    for poi in pois:
        PoiTypes.add(poi['poiType'].encode('utf-8'))
    return True
    
def show(Set,num):
    os.system("clear")
    print 'Current GPS number: '+str(num)
    for one in Set:
        print one
    print 'Current Total: ' + str(len(Set))

def main():
    lat_beg = 39.849713081441
    lat_end = 40.003754766807
    lng_beg = 116.28693749489
    lng_end = 116.48762815435
    
    num = 0
    lat = lat_beg
    while lat<lat_end:
        lng = lng_beg
        while lng<lng_end:
            if getPoiType(lat,lng):
                num +=1
            lng += GPS_STEP
            if num%10==0:
                show(PoiTypes,num)
    lat += GPS_STEP
    
    show(PoiTypes)
    print 'Finish!'

if __name__ == '__main__':
    main()
