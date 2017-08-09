# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql
from zxcs8 import settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

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


    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            yield scrapy.Request(url=file_url, headers={'Referer': item['downloadpage_url']}, meta={'item': item})


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        path = "%s/%s[%s][%s][%s]《%s》.%s" % (item['tag'][1], item['id'][0], item['tag'][1], item['tag'][2], item['author'][0], item['title'][0], item['file_urls'][0].split('.')[-1])
        return path


class MySQLPipeline(object):

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 查重处理
            self.cursor.execute(
                """select id from zxcs8 where id = %s""",
                item['id'][0])
            # 是否有重复数据
            repetition = self.cursor.fetchone()
            # 重复
            if not repetition:
            # 插入数据
                self.cursor.execute('insert into zxcs8(ID,TITLE,AUTHOR,DESCR,PAGE_URL,DOWNPAGE_URL,DOWNNODE,DOWN_URL_1,DOWN_URL_2,DOWN_URL_3,COVER_URL,RATING,TAG_1,TAG_2) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                    item['id'][0],
                    item['title'][0],
                    item['author'][0],
                    item['descr'][0],
                    item['page_url'][0],
                    item['downloadpage_url'],
                    "",
                    item['download_url'][0],
                    item['download_url'][1],
                    item['download_url'][2],
                    item['image_urls'][0],
                    "",
                    item['tag'][1],
                    item['tag'][2]
                    )
                )
                self.connect.commit()
            else:
                pass
        except Exception as error:
            # 出现错误时打印错误日志
            log(error)
        return item
