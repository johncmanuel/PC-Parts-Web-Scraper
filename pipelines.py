# -*- coding: utf-8 -*-

from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem
from pathlib import Path


class PerCategoryJsonExportPipeline:
    """ Creates a .json file for each category and its respective data. """

    @classmethod
    def from_crawler(cls, crawler):
        """ Get spider's name """
        return cls(crawler.spider.name)

    def __init__(self, spider_name):
        self.spider_name = spider_name

    def open_spider(self, spider):
        """ Create a dictionary for product_category in object Item"""
        self.category_to_exporter = dict()

    def close_spider(self, spider):
        for exporter in self.category_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        """ Sort scraped data according to their spider and category """
        category = item['product_category']
        dir = 'data/output/{0}'.format(self.spider_name)

        """ Create a directory if it doesn't exist """
        Path(dir).mkdir(parents=True, exist_ok=True)

        """ Check if category exists in dictionary """
        if category not in self.category_to_exporter:
            """ Export scraped data into a json file with their spider name and category. """
            f = open('data/output/{0}/{1}_{2}.json'.format(self.spider_name, self.spider_name, category), 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.category_to_exporter[category] = exporter
        return self.category_to_exporter[category]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
