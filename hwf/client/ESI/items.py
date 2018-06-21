# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EsiItem(scrapy.Item):
    #http://apps.webofknowledge.com
    title = scrapy.Field()
    author = scrapy.Field()
    cited = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    #
