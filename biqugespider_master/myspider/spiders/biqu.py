# -*- coding: utf-8 -*-
import random
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
from bs4 import BeautifulSoup
from myspider import *
from myspider.items import biquItem
from scrapy_redis.spiders import RedisCrawlSpider
import redis
import sys
import logging

sys.setrecursionlimit(100000)

#import logging                         
class BiquSpider(CrawlSpider):
    name = "biqu"
    redis_key = 'biqu:start_urls'
    allowed_domains = ["www.biquge.com.tw"]
    start_urls = [
                'http://www.biquge.com.tw/',
                'http://www.biquge.com.tw/kehuan/',
                'http://m.biquge.com.tw/wapsort/3_1.html/',
                'http://m.biquge.com.tw/wapsort/4_1.html/',
                'http://m.biquge.com.tw/wapsort/5_1.html/',
                'http://m.biquge.com.tw/wapsort/6_1.html/',
                'http://m.biquge.com.tw/wapsort/7_1.html/',
                'http://m.biquge.com.tw/wapsort/8_1.html/',
                'http://m.biquge.com.tw/wapfull/1.html',
                ]

    rules = (
       Rule(LinkExtractor(allow=(r'/\/d*_/d*$',)),callback='chapter',),
        )
    def chapter(self, response):
        for urls in response.xpath('//*[@id="list"]/dl/dd/a/@href').extract():
            url_a = 'http://www.biquge.com.tw/' +urls
            item = biquItem()
            item['masterurls'] = url_a
            yield item
            #logging.debug('url_a')
        #    yield scrapy.Request(url=url_a,callback=self.parse_contents)
#    def parse(self, response):
#
        # collect `item_urls`

#        for item_url in item_urls:

#            yield scrapy.Request(item_url, self.parse_item)

#    def start_requests(self):
#        urls = [
#            'http://www.biquge.com.tw/',
            #'http://www.biquge.com.tw/quanben/',
#        ]
#        for url in urls:
#            yield scrapy.Request(url=url, callback=self.parse_link,)
    #response_start = start_requests('')
        
#    def parse(self, response):
        #data1 = response.body
        #global response_start
        #response_start = response
#        soup = BeautifulSoup(response.body,'html.parser') 
        #print(soup.contents)
#        for x in soup.find_all('a',attrs={'href':re.compile(r'/\d*_\d*/$')}):
#            link =[]
#            link = x.get('href')
            #link = item['link']
            #item['bookname'] = x.text
            #print(x)
#        for urls in response.xpath('//*[@id="list"]/dl/dd/a/@href'):
#            url_a = 'http://www.biquge.com.tw/' +urls
#            logging.debug('url')
#            yield scrapy.Request(url=url_a,callback=self.parse_contents)
#    m_resquest = scrapy.Request(url=(random.sample(start_urls,1))[0], callback=scrapy.Spider.parse,)
    def parse_link(self,response):
        #data2 = response.body
        #for soup in BeautifulSoup(response.body,'html.parser'):
        soup = BeautifulSoup(response.body,'html.parser') 
        #print(soup.contents)
        
        for data in soup.find_all('h1'):
            bookname = data.string
            #chapterlist = soup.find_all('div',attrs={'id':'list'})
        for chapter in soup.find_all('a',attrs={'href':re.compile(r'/\d*_\d*/\d*\.html$')}):
            chaptername = chapter.string
            #print(chapter)
            chapterlink = re.search(r'\d*\.html$',chapter.get('href')).group()

            logging.debug(chapterlink)
            chapterlink = response.url+chapterlink
            #global request_chapterlink
            #print(chapterlink)
        #    request_chapterlink = scrapy.Request(url=chapterlink,callback=self.parse_contents,meta={'bookname':bookname,
        #                                                                            'chaptername':chaptername,
        #                                                                            'contentlink':chapterlink})    
            yield scrapy.Request(url=chapterlink,callback=self.parse_contents,)
    #re = parse_link(self,response)
    def parse_contents(self,response):
        item = biquItem()
        item['bookname'] = response.xpath('//*[@class="bottem1"]/a[3]/text()').extract()[0]
    #    item['bookname'] = response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1/text()').extract()
        item['chaptername'] = response.xpath('//*[@class="bookname"]/h1/text()').extract()[0]
    #    item['contentlink'] = response.meta['contentlink']
        #response_html = response.body
        #html_soup = BeautifulSoup(response_html,'html.parser')
        #item['content'] = html_soup.find_all('div',attrs={'id':'content'})[0].text
        item['content'] = response.xpath('//*[@id="content"]/text()').extract()
    #    print(item['bookname'])
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
