# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from myspider.items import biquItem,bookItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
 
class MasterPipeline(object):
 
    def __init__(self):
        self.redis_url = 'reds://127.0.0.1:6379/0'
        self.r = redis.Redis.from_url(self.redis_url,decode_responses=True)
 
    def process_item(self, item, spider):
        self.r.lpush('biqu:start_urls', item['masterurls'])
class MMasterPipeline(object):
        
    def __init__(self):
        self.redis_url = 'reds://127.0.0.1:6379/1'
        self.r = redis.Redis.from_url(self.redis_url,decode_responses=True)
        
    def process_item(self, item, spider):
        if isinstance(item, biquItem):
            self.r.lpush('biqu:start_urls', item['masterurls'])
            #print('完成 start_url')
            return print('完成 start_url')
            
        else:
            #print('mm'+str(isinstance(item, biquItem)))
            return item


class MyspiderPipeline(object):
    
    def __init__(self, mongo_host, mongo_port,mongo_dbname):
         self.mongo_host = mongo_host
         self.mongo_port = mongo_port
         self.mongo_dbname = mongo_dbname

    @classmethod
    def from_crawler(cls, crawler):
    #
    #    scrapy为我们访问settings提供了这样的一个方法，这里，
    #    我们需要从settings.py文件中，取得数据库的URI和数据库名称
        pass
        return cls(
            mongo_host = crawler.settings.get('MONGODB_HOST'),
            mongo_port = crawler.settings.get('MONGODB_PORT'),
            mongo_dbname = crawler.settings.get('MONGODB_DBNAME'))
            

    def open_spider(self, spider):
    #   '''
    #    爬虫一旦开启，就会实现这个方法，连接到数据库
    #    '''
        self.client = pymongo.MongoClient(host=self.mongo_host,port=self.mongo_port)
        self.db = self.client[self.mongo_dbname]

    def close_spider(self, spider):
    #    '''
    #    爬虫一旦关闭，就会实现这个方法，关闭数据库连接
    #    '''
        self.client.close()

    def process_item(self, item, spider):  
    #    '''
    #        每个实现保存的类里面必须都要有这个方法，且名字固定，用来具体实现怎么保存
    #    '''   
        if isinstance( item, bookItem):
            table = self.db[item['bookname']]
            #table_url = self.db['contentlink']
            table.update({"_id":'heards'},{"_id":'heards','bookname':item['bookname'],'author':item['author'],'booktype':item['booktype'],'updatatime':item['updatatime']},True)
            #table_url.insert({'_id':item['contentlink']})
            #table.insert_one(data)
            return print('%s heards 完成！'%(item['bookname']))
            
        else:
            #print('book'+str(isinstance(item, biquItem))+str(type(item)))
            return item
            
