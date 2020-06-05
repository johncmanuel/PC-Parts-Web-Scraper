# -*- coding: utf-8 -*-


import scrapy


class PcpartsItem(scrapy.Item):
    """ Main fields of data to be scraped. """
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    product_category = scrapy.Field()
    product_stars = scrapy.Field()
    pass
