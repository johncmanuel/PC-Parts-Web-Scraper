"""

amazon_spider.py
by John Carlo Manuel
05/30/20
J.E Computers Inc.

"""

import scrapy
import json
from ..items import PcpartsItem


class AmazonSpider(scrapy.Spider):
    """ Spider for crawling Amazon URLs given in data/urls.json and parsing its scraped data """

    name = 'amazon'

    """ Loads JSON object containing the urls and extracts a value as a list of urls
    from a given key """
    with open('data/urls.json') as f:
        spider_urls = json.loads(f.read())
        start_urls = spider_urls['amazon_urls']

    def parse(self, response):
        """ Gather scraped data """
        product_box = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sg-col-20-of-28", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "sg-col-inner", " " ))]')

        """ Loads JSON object and extract its value as dict with a given key """
        with open('data/categories_and_query.json') as b:
            spider_categories_queries = json.loads(b.read())
            categories_and_queries = spider_categories_queries['amazon_categories_and_queries']

        """ Check each box in each product and finds the name and price tag """
        for box in product_box:
            item = PcpartsItem()
            #item['product_category'] = next(category for category, query in categories_and_queries.items() if query in response.url)
            name = box.xpath('.//span[contains(concat( " ", @class, " " ), concat( " ", "a-size-medium", " " ))]/text()').get()
            price = box.xpath('.//span[contains(concat( " ", @class, " " ), concat( " ", "a-offscreen", " " ))]/text()').get()
            if price and name:
                item['product_category'] = next(category for category, query in categories_and_queries.items() if query in response.url)
                item['product_name'] = name
                item['product_price'] = price
                yield item
            pass

        """ Go to the next page """
        next_page = response.css('.a-last a').css('::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
