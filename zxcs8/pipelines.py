# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline


class Zxcs8imagesPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(url=image_url, headers={'Referer': item['page_url'][0]}, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        path = "covers/%s.%s" % (item['id'][0],
                                item['image_urls'][0].split('.')[-1])
        return path


class Zxcs8filesPipeline(FilesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(url=file_url, headers={'Referer': item['downloadpage_url']}, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        path = "%s/%s[%s][%s][%s]《%s》.%s" % (item['tag'][1], item['id'][0], item['tag'][1], item['tag'][2], item['author'][0], item['title'][0], item['file_urls'][0].split('.')[-1])
        return path
