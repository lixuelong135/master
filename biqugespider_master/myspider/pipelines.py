# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
from myspider.items import biquItem
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
        self.r.lpush('bq:start_urls', item['masterurls'])

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
        #item = biquItem()
        #collection = item['bookname']
        #if collection is None:
        #    return item
        #data={
            
        #    'bookname':item['bookname'],
        #    'content':item['content'],
        #}
        
        table = self.db[item['bookname']]
        #table_url = self.db['contentlink']
        table.update({"_id":item['chaptername']},{"_id":item['chaptername'],'bookname':item['bookname'],'content':item['content']},True)
        #table_url.insert({'_id':item['contentlink']})
        #table.insert_one(data)
        return print('%s %s 完成！'%(item['bookname'],item['chaptername'],))
        
