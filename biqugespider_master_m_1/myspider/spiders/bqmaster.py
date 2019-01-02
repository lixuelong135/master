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
    allowed_domains = ['m.biquyun.com']
#    custom_settings = {
#        'ITEM_PIPELINES':{
#            'myspider.pipelines.MyspiderPipeline': 300,
#            'myspider.pipelines.MMasterPipeline':300,
#        }
#    }
    start_urls = [
                'http://m.biquyun.com/wapsort/1_1.html',     #玄幻
                'http://m.biquyun.com/wapsort/2_1.html',     #修真
                'http://m.biquyun.com/wapsort/3_1.html',     #都市
                'http://m.biquyun.com/wapsort/4_1.html',     #历史
                'http://m.biquyun.com/wapsort/5_1.html',     #网游
                'http://m.biquyun.com/wapsort/6_1.html',     #科幻
                'http://m.biquyun.com/wapsort/7_1.html',     #恐怖
                'http://m.biquyun.com/wapsort/8_1.html',     #其他
                'http://m.biquyun.com/wapfull/1.html',       #完本
                ]

        
    
    rules = (
       Rule(LinkExtractor(allow=(r'\/wapfull\/\d*.html$'),),follow=True),
       Rule(LinkExtractor(allow=(r'\/wapsort\/\d*.html$'),),follow=True),
       Rule(LinkExtractor(allow=(r'\/wapsort\/\d*_\d*.html$'),),follow=True),
       Rule(LinkExtractor(allow=(r'\/wapbook\/\d*.html$'),restrict_xpaths=('//a')),callback='bookheards',follow=True),
       #Rule(LinkExtractor(allow=(r'\/wapbook\/\d*.html$'),restrict_xpaths=('//a')),follow=True),
       #Rule(LinkExtractor(allow=(r'\/\d*.html$'),restrict_xpaths=('//div[@class=page]')),follow=True),
       Rule(LinkExtractor(allow=(r'\/\d*_\d*_\d*\/$'),),callback = 'chapter',follow=True),  #章节页面
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
            url_a = 'http://m.biquyun.com' +urls
            #print(url_a)
            item = biquItem()
            item['masterurls'] = url_a
            yield item


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
