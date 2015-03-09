# -*- encoding=utf-8 -*- 

from avos import AVObject
import json
import datetime
import requests
import settings
from util_opt import *

import warnings
warnings.filterwarnings("ignore")

class AvosClass(AVObject):
    def __init__(self):
        super(AvosClass, self).__init__()

class AvosManager(object):

        def __init__(self):
                AvosClass.app_settings = [settings.avos_app_id, settings.avos_app_key]

        def saveData(self,className,dataDict):
                res = AvosClass._save_to_avos(className,dataDict)

                if 'createdAt' not in json.loads(res.content):
                        print res.content
                        return None
                else:
                        return res.content

        #By Zhong.zy, Create users
        def createUser(self,userInfo):
                res = requests.post(
                    url = AvosClass.Users,
                    headers = AvosClass.headers(),
                    data = json.dumps(userInfo),
                    verify=False)
                if 'createdAt' not in json.loads(res.content):
                    print 'Error: '+res.content
                    return None
                else:
                    print 'Create user success!\n'+res.content
                    
        #By Zhong.zy, Get user Id by username
        def getUserIdByName(self,username):
                with_params = {
                    'keys':'objectId',
                    'where':'{"username":"%s"}'%username
                    }
                res = requests.get(
                    url = AvosClass.Users,
                    headers=AvosClass.headers(),
                    params=with_params,
                    verify=False
                )
                if not res.ok:
                        print 'Error'+res.content
                        return None
                results = json.loads(res.content)['results']
                if results:
                        return results[0]['objectId']


        #By Zhong.zy, Get info by specified opt
        def getData(self,className,**kwargs):
                print kwargs


                for k in kwargs.keys():
                    #if type(kwargs[k]) not in [dict, list]:
                    if type(kwargs[k]) not in [str, unicode]:
                        kwargs[k] = json.dumps(kwargs[k])


                print "jsonify",type(json.dumps(kwargs))
                res = requests.get(
                    AvosClass.base_classes+className,
                    headers=AvosClass.headers(),
                    params=kwargs,
                    verify=False
                )
                if 'error' not in json.loads(res.content):
                        return res.content
                else:
                    print res.content
                    return None



        def getDateGreatData(self,className, timeName, date, **kwargs):
                #avos data type constrain the json's value should be a number or string

                #where={"start_time":{"$gte":{"__type": "Date", "iso": time.strftime("%Y-%m-%d %H:%M:%S") } }}
                a = '{"%s":{"$gte":{"__type": "Date", "iso": "%s"} }}'%(timeName,date)

                where_dict = {"where":a}
                kwargs.update(where_dict)
                """
                for k in kwargs.keys():
                    #if type(kwargs[k]) not in [dict, list]:
                    if type(kwargs[k]) not in [str, unicode]:
                        kwargs[k] = json.dumps(kwargs[k])

                """
                print "kwargs", json.dumps(kwargs)
                #print "jsonify",type(json.dumps(kwargs))
                res = requests.get(
                    AvosClass.base_classes+className,
                    #"http://httpbin.org/get",
                    headers=AvosClass.headers(),
                    params=kwargs,
                    verify=False
                )
                #print "FFFFICCCCC", res.content
                #time.sleep(11000000)
                if 'error' not in json.loads(res.content):
                        return res.content
                else:
                    print res.content
                    return None

        def getDateBetweenData(self,className, timeName, date1, date2, **kwargs):
                #avos data type constrain the json's value should be a number or string

                #where={"start_time":{"$gte":{"__type": "Date", "iso": time.strftime("%Y-%m-%d %H:%M:%S") } }}
                a = ' { "%s":{"$gte":{"__type": "Date", "iso": "%s"} ,"$lte":{"__type": "Date", "iso":"%s"}}}'\
                      %(timeName,date1,date2)
                #where={"score":{"$gte":1000,"$lte":3000}}
                where_dict = {"where":a}
                kwargs.update(where_dict)
                """
                for k in kwargs.keys():
                    #if type(kwargs[k]) not in [dict, list]:
                    if type(kwargs[k]) not in [str, unicode]:
                        kwargs[k] = json.dumps(kwargs[k])

                """
                print "kwargs", json.dumps(kwargs)
                #print "jsonify",type(json.dumps(kwargs))
                res = requests.get(
                    AvosClass.base_classes+className,
                    #"http://httpbin.org/get",
                    headers=AvosClass.headers(),
                    params=kwargs,
                    verify=False
                )
                #print "FFFFICCCCC", res.content
                #time.sleep(11000000)
                if 'error' not in json.loads(res.content):
                        return res.content
                else:
                    print res.content
                    return None

        def getDateBetweenDataByUser(self,className, timeName, date1, date2, userId, **kwargs):
                #avos data type constrain the json's value should be a number or string

                #where={"start_time":{"$gte":{"__type": "Date", "iso": time.strftime("%Y-%m-%d %H:%M:%S") } }}
                a = ' { "%s":{"$gte":{"__type": "Date", "iso": "%s"} ,"$lte":{"__type": "Date", "iso":"%s"}},"userId":"%s"}'\
                      %(timeName,date1,date2,userId)
                #where={"score":{"$gte":1000,"$lte":3000}}
                where_dict = {"where":a}
                kwargs.update(where_dict)
                """
                for k in kwargs.keys():
                    #if type(kwargs[k]) not in [dict, list]:
                    if type(kwargs[k]) not in [str, unicode]:
                        kwargs[k] = json.dumps(kwargs[k])

                """
                print "kwargs", json.dumps(kwargs)
                #print "jsonify",type(json.dumps(kwargs))
                res = requests.get(
                    AvosClass.base_classes+className,
                    #"http://httpbin.org/get",
                    headers=AvosClass.headers(),
                    params=kwargs,
                    verify=False
                )
                #print "FFFFICCCCC", res.content
                #time.sleep(11000000)
                if 'error' not in json.loads(res.content):
                        return res.content
                else:
                    print res.content
                    return None

        #By Zhong.zy, Save activity in a same interface
        def saveActivity(self,dataDict):
                self.saveData('activities',dataDict)

        #By Zhong.zy, Get id in order to update data
        def getIdByCondition(self,className,**kwargs):
                cond = json.dumps(kwargs)
                res = self.getData(className,keys='objectId',where=cond)
                if res:
                        results = json.loads(res)['results']
                        if results:
                                return results[0]['objectId']
                        else:
                            return None

        #By Zhong.zy, Get field in terms of some condition        
        def getFieldByCondition(self,className,field,**kwargs):
                cond = json.dumps(kwargs)
                res = self.getData(className,keys=field,where=cond)
                if res:
                        results = json.loads(res)['results']
                        if results:
                                return results[0][field]

        #By Zhong.zy, Get id in order to update data
        def getIdByName(self,className,objName):
                return self.getIdByCondition(className,name=objName)


        def updateDataById(self,className,objectId,dataDict):

            res = AvosClass._update_avos(className,str(objectId),dataDict)
            if 'error' not in json.loads(res.content):
                    return res.content
            else:
                    a = 'Update Error:'+json.loads(res.content)['error']
                    b =  'From: '+className
                    return {"error":a + b}



        #By Zhong.zy, insert or update
        def updateDataByName(self,className,objName,dataDict):  #this is activities‘s update！
                objectId =  self.getIdByName(className,objName)
                if objectId:
                        res = AvosClass._update_avos(className,str(objectId),dataDict)
                        if 'error' not in json.loads(res.content):
                                return res.content
                        else:
                                a = 'Update Error:'+json.loads(res.content)['error']
                                b =  'From: '+className+objName
                                return {"error":a + b}
                else:
                        return {"error":"no such object"}  # {"error":no}

        #By Zhong.zy, delete, param data is id or id list
        def deleteData(self,className,data):
                res = AvosClass._remove_avos(className,data)
                if 'error' in json.loads(res.content):
                    print res.content
                    return None
                else:
                    return '{}'  #leancloud's return data,but must be string not empty dict




if __name__ == "__main__":
        avosManager = AvosManager()
        start = "2013-05-05 20:30:45"
        date_utc = getUtcDate(start)
        start_utc = timeConvet2utc(start)
        

        
        start_iso = start_utc.replace(" ","T")+".000Z"
        date_iso = date_utc.replace(" ","T")+".000Z"
        date_time = dict(__type='Date',iso=date_iso)    
        start_time = dict(__type='Date',iso=start_iso)
        end_time = dict(__type='Date',iso=start_iso)
        dataDict = {"name":"《文成公主》大型实景剧","date":date_time,
        "start_time":start_time,"end_time":end_time,"ticket":"220","region":"北京市海淀区北京邮电大学","location":gps2GeoPoint(39.970513,116.361834),"category":""}
        className = "testDate"
        #avosManager.saveData(className,dataDict)
        #avosManager.saveActivity(dataDict)
        #avosManager.updateDataByName('activities','《文成公主》大型实景剧',dict(ticket='200'))
        results = avosManager.getData("poiClass",order="longitude", where='{"type":"休闲娱乐"}',limit=10)
        results = json.loads(results)['results']
        results = results[0:3]
        for r in results:
            print r
        #print avosManager.getIdByCondition(className,name='《文成公主》大型实景剧')
        '''
        AvosClass.app_settings = [settings.avos_app_id, settings.avos_app_key]
        res = AvosClass.save(dataDict)
        if 'createdAt' in json.loads(res.content):
                print '\nSucceeded in creating test object in AvosClass!\n'
        else:
                print res.content
        '''
