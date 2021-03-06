# -*- coding: utf-8 -*-
import random
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from bs4 import BeautifulSoup

from myspider.items import biquItem,bookItem
from scrapy_redis.spiders import RedisCrawlSpider
import redis
import sys
import logging

sys.setrecursionlimit(100000)

#import logging                         
class BiquSpider(CrawlSpider):
    name = "bqmaster"
    redis_key = 'biqu:start_urls'
    allowed_domains = ['http://m.biquge.com.tw']
#    custom_settings = {
#        'ITEM_PIPELINES':{
#            'myspider.pipelines.MyspiderPipeline': 300,
#            'myspider.pipelines.MMasterPipeline':300,
#        }
#    }
    start_urls = [
                'http://m.biquge.com.tw/wapsort/1_1.html',
                #'http://m.biquge.com.tw/wapsort/2_1.html',
                #'http://m.biquge.com.tw/wapsort/3_1.html',
                #'http://m.biquge.com.tw/wapsort/4_1.html',
                #'http://m.biquge.com.tw/wapsort/5_1.html',
                #'http://m.biquge.com.tw/wapsort/6_1.html',
                #'http://m.biquge.com.tw/wapsort/7_1.html',
                #'http://m.biquge.com.tw/wapsort/8_1.html',
                #'http://m.biquge.com.tw/wapfull/1.html',
                ]

        
    
    rules = (
       Rule(LinkExtractor(allow=(r'\/wapsort\/\d*_\d*.html$'),),follow=True),
       Rule(LinkExtractor(allow=(r'\/wapbook\/\d*.html$'),restrict_xpaths=('//a')),callback='bookheards',follow=True),
       #Rule(LinkExtractor(allow=(r'\/\d*.html$'),restrict_xpaths=('//div[@class=page]')),follow=True),
       Rule(LinkExtractor(allow=(r'\/\d*_\d*_\d*\/$'),),callback = 'chapter',follow=True),
       #Rule(LinkExtractor(allow=(r'\/\d*_\d*_\d*\/$'),),follow = True),
        )
    def bookheards(self,response):
        item = bookItem()
        #print(response.body)
        item['bookname'] = response.xpath('//div[@class="cataloginfo"]/h3/text()').extract()[0]
        item['author'] = response.xpath('//div[@class="infotype"]/p[1]/text()').extract()[0]
        item['booktype'] = response.xpath('//div[@class="infotype"]/p[2]/text()').extract()[0]
        item['updatatime'] = response.xpath('//div[@class="infotype"]/p[3]/text()').extract()[0]
        yield item
    def chapter(self, response):

        for urls in response.xpath('//ul[@class="chapters"]/li/a/@href').extract():
            #print(response.body)
            url_a = 'https://m.biquge.com.tw' +urls
            #print(url_a)
            item_url = biquItem()
            item_url['masterurls'] = url_a
            yield item_url


    if __name__ == '__main__':
        from scrapy import cmdline
        args = "scrapy crawl biqu".split()
        cmdline.execute(args)        
        
        #item['chapterurl'] = 
        #print(item['bookname'])
        #for xx in soup.find_all('div',attr={'id':list})
        #print(soup.contents)
        #print(bookname,url)
            
        
#.xpath('//div//a[contains(@href,"http://www.biquge.com.tw/")]/text()').extract():
