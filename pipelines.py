# -*- coding: utf-8 -*-

from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem


class PerCategoryJsonExportPipeline:
    """ Creates a .json file for each category and its respective data. """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.spider.name)

    def __init__(self, spider_name):
        self.spider_name = spider_name

    def open_spider(self, spider):
        self.category_to_exporter = dict()

    def close_spider(self, spider):
        for exporter in self.category_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        category = item['product_category']
        if category not in self.category_to_exporter:
            f = open('data/output/{0}/{1}_{2}.json'.format(self.spider_name, self.spider_name, category), 'wb')
            exporter = JsonLinesItemExporter(f)
            exporter.start_exporting()
            self.category_to_exporter[category] = exporter
        return self.category_to_exporter[category]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
