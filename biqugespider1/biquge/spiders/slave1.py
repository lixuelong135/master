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
        item['bookname'] = response.xpath('//*[@class="bottem1"]/a[3]/text()').extract()[0]

        item['chaptername'] = response.xpath('//*[@class="bookname"]/h1/text()').extract()[0]

        item['content'] = response.xpath('//*[@id="content"]/text()').extract()
        return item
        
                
if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl slave1".split()
    cmdline.execute(args)