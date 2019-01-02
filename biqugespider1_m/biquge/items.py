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
    link = scrapy.Field()
    chaptername = scrapy.Field()
    chapterlink = scrapy.Field()
    content = scrapy.Field()
    contentlink = scrapy.Field()
    masterurls = scrapy.Field()
    booktype = scrapy.Field()

