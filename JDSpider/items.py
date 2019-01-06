# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    uid = scrapy.Field()
    creationTime=scrapy.Field()
    firstCategory=scrapy.Field()
    secondCategory=scrapy.Field()
    thirdCategory=scrapy.Field()
    productId=scrapy.Field()
    content = scrapy.Field()
    score=scrapy.Field()
    #pass
