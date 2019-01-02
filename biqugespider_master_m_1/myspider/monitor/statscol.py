# *-* coding:utf-8 *-*
'''

'''

import redis
from .settings import STATS_KEYS,REDIS_DB,TIMEINTERVAL
import time
import requests
import threading
from scrapy import signals
import inspect
import ctypes

from myspider.osinfo import cpu_percent , disk_percent


r = redis.Redis(host='localhost', port=6379, db=0)
#Time = lambda:time.strftime('%Y/%m/%d %H:%M:%S',time.localtime())
Time = lambda: time.time()*1000
#Time = lambda:time.strftime('%H:%M:%S',time.localtime())

class StatcollectorMiddleware(object):
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=REDIS_DB)
        self.stats_keys = STATS_KEYS

    def process_request(self, request, spider):
        
        #self.formatStats(spider.crawler.stats.get_stats())
        pass



class SpiderRunStatspipeline(object):
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=REDIS_DB)
        self.stats_keys = STATS_KEYS
        self.TIMEINTERVAL = TIMEINTERVAL
        self.end = False
    def open_spider(self, spider):
        #global end
        t_start =int(Time())
        def check_data(self, stats,t_start,TIMEINTERVAL,end):
            print(end)
            t_start = t_start
            for key in self.stats_keys:
                key_value = stats.get(key, None)
                if not key_value: continue
                value = {'value':[int(Time()), key_value]}
                #print('监控数据记录 ',key)
                self.r.rpush(key, value)
            
            self.r.rpush('cpu_percent',cpu_percent())
            self.r.rpush('disk_percent',disk_percent())
            print('监控数据记录完成 ')
            t_start = int(Time())
            if end is False:
                t = threading.Timer(int(TIMEINTERVAL/1000),check_data,(self,spider.crawler.stats.get_stats(),t_start,TIMEINTERVAL,self.end))
            else:
                return print('爬虫监控程序已退出')
            t.start()
            #print(t.is_alive)
        t = threading.Timer(1,check_data,(self,spider.crawler.stats.get_stats(),t_start,TIMEINTERVAL,self.end))
        t.start()
        r.set('spider_is_run', 1)
        requests.get('http://127.0.0.1:5000/signal?sign=running')
    def spider_closed(self):
        print("spider close")
        self.end = True
    def close_spider(self, spider,):
        #global end
        self.end = True
        
        print("爬虫关闭！")
        r.set('spider_is_run', 0)
        requests.get('http://127.0.0.1:5000/signal?sign=closed')