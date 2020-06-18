

import scrapy
import json
from ..items import PcpartsItem
from scrapy.http.request import Request


class NeweggSpider(scrapy.Spider):
    """ Spider for crawling Newegg URLs given in data/websites.json and parsing its scraped data. """

    name = 'newegg'

    def __init__(self, *args, **kwargs):
        super(NeweggSpider, self).__init__(*args, **kwargs)
        """
        Loads JSON object containing urls from Newegg and its categories and queries. It extracts its data
        into two important variables.
        1. start_urls is a list that contains all the urls related to the given keyword with an
        appended '1' at the end.
        2. categories_and_queries contains keywords used for organizing the scraped data in the pipelines.
        """
        with open('data/websites.json') as f:
            data = json.loads(f.read())
            self.newegg_urls = data['newegg']['newegg_urls']
            self.categories_and_queries = data['newegg']['newegg_categories_and_queries']
            self.start_urls = [url + "1" for url in self.newegg_urls]

        """ Class iterator for crawling through each page. """
        self.next_page = 1

        """ If user decides to crawl specific url(s) via command-line. """
        self.start_url_str = 'start_url'
        if self.start_url_str in kwargs:
            self.start_urls = [kwargs.get(self.start_url_str)]

    def returnMatchingUrl(self, urls, response_url, categories_and_queries):
        """
        Check if both the current url being crawled and the url in list variable, urls,
        contain the same query, or a matching substring. If they both do, return
        the url from urls.
        """
        for url, query in zip(urls, categories_and_queries.values()):
            if query in response_url and url:
                return url
        return None

    def parse(self, response):
        """ Gather scraped data recursively. """

        product_box = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "item-container", " " ))]')

        """ Check each box in each product and gathers the name, price tag, and ratings data. """
        for box in product_box:
            item = PcpartsItem()
            # TODO: Fix the xpaths
            name = box.xpath('.//a[contains(concat( " ", @class, " " ), concat( " ", "item-title", " " ))]/text()').get()
            link = box.xpath('.//a[contains(concat( " ", @class, " " ), concat( " ", "item-title", " " ))]/@href').get()
            price = box.xpath('.//li[contains(concat( " ", @class, " " ), concat( " ", "price-current", " " ))]//text()[preceding-sibling::strong][normalize-space()!=""]').get()
            stars = box.xpath('.//a[contains(concat( " ", @class, " " ), concat( " ", "item-rating", " " ))]//text()').get()
            """ Check if both the price tag and name are available. If so, parse its data into the item object. """
            if price and name:
                item['product_category'] = next(category for category, query in self.categories_and_queries.items() if query in response.url)
                item['product_name'] = name
                item['product_price'] = price
                item['product_stars'] = stars
                item['product_link'] = link
                yield item
            pass

        url = self.returnMatchingUrl(self.newegg_urls, response.url, self.categories_and_queries)
        if url is not None:
            self.next_page += 1
            """ Add next_page to url and call this method recursively. """
            yield Request(url + str(self.next_page), callback=self.parse)
