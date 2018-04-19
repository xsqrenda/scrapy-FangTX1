# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PricetrendItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    try:
        city = scrapy.Field()
        district = scrapy.Field()
        name = scrapy.Field()
        url = scrapy.Field()
        data = scrapy.Field()
        newcode = scrapy.Field()
        pass
    except Exception as es:
        print(es)
