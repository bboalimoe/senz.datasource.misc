# -*- encoding: utf-8 -*-
# Run at a specific time everyday
# By Zhong Ziyuan

import time,sched

class SchedTimer(object):
    def __init__(self,hour,min,sec):
        self.hour = hour
        self.min = min
        self.sec = sec
        self.schedule = sched.scheduler(time.time, time.sleep)
    #
    #计算从现在到定时时间的秒数
    #
    def fromNow(self,hour,min,sec):
        now = time.localtime()
        sec_d,borrow = self.borrowMinus(sec, now.tm_sec, 60)
        min_d,borrow = self.borrowMinus(min, now.tm_min, 60, borrow)
        hour_d,borrow = self.borrowMinus(hour, now.tm_hour, 24, borrow)
            
        return hour_d*3600+min_d*60+sec_d
    #
    #借位相减
    #
    def borrowMinus(self,A1,A2,radix,borrow=0):
        res = A1-A2-borrow
        borrow=0
        if res<0:
            res+=radix
            borrow=1
        return res,borrow
    #
    #开启定时器
    #
    def start(self, function, args=()):
        while True:
            time_d = self.fromNow(self.hour,self.min,self.sec)
            self.schedule.enter(time_d, 0, function, args)
            self.schedule.run()
            time.sleep(1)

#
#Testing
#

def func():
    print 'Time is up!'

if __name__=="__main__":
    t = SchedTimer(15,18,0)
    t.start(func)

        
