"""

amazon_spider.py
by John Carlo Manuel
05/30/20
J.E Computers Inc.

"""

import scrapy
import json
import re
from ..items import PcpartsItem


class AmazonSpider(scrapy.Spider):
    """ Spider for crawling Amazon URLs given in data/websites.json and parsing its scraped data. """

    name = 'amazon'

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        """
        Loads JSON object containing the urls and its categories and queries, and extracts its data
        into two variables.
        1. start_urls is a list that contains all the urls related to the given keyword.
        2. categories_and_queries contains keywords used for organizing the scraped data in pipelines.
        """
        with open('data/websites.json') as f:
            data = json.loads(f.read())
            self.start_urls = data['amazon']['amazon_urls']
            self.categories_and_queries = data['amazon']['amazon_categories_and_queries']

    def parse(self, response):
        """ Gather scraped data recursively. """

        product_box = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "sg-col-20-of-28", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "sg-col-inner", " " ))]')

        """ Check each box in each product and gathers the name, price tag, and ratings data. """
        for box in product_box:
            item = PcpartsItem()
            name = box.xpath('.//span[contains(concat( " ", @class, " " ), concat( " ", "a-size-medium", " " ))]/text()').get()
            link = box.xpath('.//a[contains(concat( " ", @class, " " ), concat( " ", "a-link-normal", " " ))][contains(concat( " ", @class, " " ), concat( " ", "a-text-normal", " " ))]/@href').get()
            price = box.xpath('.//span[contains(concat( " ", @class, " " ), concat( " ", "a-offscreen", " " ))]/text()').get()
            stars = box.xpath('.//span/@aria-label').get()
            """ Check if both the price tag and name are available. If so, parse its data into the item object. """
            if price and name:
                item['product_category'] = next(category for category, query in self.categories_and_queries.items() if query in response.url)
                item['product_name'] = name
                item['product_price'] = price
                if stars:
                    item['product_stars'] = stars[0:3]
                item['product_link'] = 'amazon.com' + link
                yield item
            pass

        """ Go to the next page and call this method """
        next_page = response.css('.a-last a').css('::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
