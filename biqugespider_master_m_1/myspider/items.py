# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class biquItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bookname = scrapy.Field()
    heards_url = scrapy.Field()    
    masterurls = scrapy.Field()
    
class bookItem(scrapy.Item):
    bookname = scrapy.Field()
    author = scrapy.Field()
    booktype = scrapy.Field()
    updatatime = scrapy.Field()
