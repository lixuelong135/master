# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import pymongo
import scrapy
from biquge.items import biquItem
import re
import random
from biquge.user_agents import agents



class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        
        
class BiqugeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    
    def process_spider_input(self,response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

#    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
#        for i in self.result:
#            yield i

    def process_spider_exception(self,esponse, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        print('爬虫异常！')
        pass

    def process_start_requests(self,start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in self,start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CheckContentLink(object):
    """
    url去重
    """
    dblink = pymongo.MongoClient(host='127.0.0.1',port=27017)
    db = dblink['biqu']
    table = db['contentlink']
    #urltable = table.find({},{'_id'})
    
    def process_request(self, request, spider):
    
        #print(request)
        #print(re.search(r'/\d*_\d*/\d*\.html$',request.url)
        if (re.search(r'/\d*_\d*/\d*\.html$',request.url)) == None:
            #print("非章节页面")
            return None
                
        else:
            try:
                self.table.insert({'_id':request.url})
            except Exception :
                #print("重复！请求取消")
                return spider.m_resquest
