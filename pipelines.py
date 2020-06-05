# -*- coding: utf-8 -*-

from scrapy.exporters import JsonLinesItemExporter
from scrapy.exceptions import DropItem


class PerCategoryCsvExportPipeline:
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


class DropNullValuesPipeline:

    def __init__(self):
        self.original_item = dict()

    def process_item(self, item, spider):
        if item['product_price'] or item['product_name'] == None:
            del item
        else:
            return item
        """
        for price, name in zip(item['product_price'].values(), item['product_name'].values()):
            if item[price] or item[name] == None:
                del item
                #raise DropItem('Null values detected in %s' % item)
            else:
                return item """


class TestPipeline:
    """ Pipeline for use in shell for debugging problems """

    def open_spider(self, spider):
        self.file = open('test.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
