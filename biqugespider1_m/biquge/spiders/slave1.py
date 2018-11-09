# -*- coding: utf-8 -*-
import random
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from bs4 import BeautifulSoup
from biquge import *
from biquge.items import biquItem
from scrapy_redis.spiders import RedisSpider
import redis
import sys
import logging

sys.setrecursionlimit(10000)
                       
class BiquSpider(RedisSpider):
    name = "slave1"
    redis_key = 'biqu:start_urls'
    allowed_domains = ["www.biquge.com.tw"]
    

    

    def parse(self,response):
        item = biquItem()
        #item['bookname'] = response.xpath('//h1[@id="chaptertitle"]/text()').extract()
        item['bookname'] = response.xpath('//meta[@name="keywords"]/@content').extract()[0].split(',')[0]
        #print(str(response.body).encode('utf-8').decode('gbk'))
        item['chaptername'] = response.xpath('//meta[@name="keywords"]/@content')[0].extract().split(',')[1]

        item['content'] = response.xpath('//div[@id="nr1"]/text()').extract()[0]
        
        return item
        
                
if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl slave1".split()
    cmdline.execute(args)