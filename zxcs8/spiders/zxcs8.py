# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from zxcs8.items import Zxcs8Item

class DmozSpider(scrapy.Spider):
    name = "zxcs"
    allowed_domains = ["www.zxcs8.com"]
    start_urls = ["http://www.zxcs8.com/post/" + str(x) for x in range(10010, 10012, 1)]


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        item = Zxcs8Item()
        item['id'] = response.xpath('//div[@id="ptop"]/a[4]/@href').re('post\/(.*)')
        item['title'] = response.xpath('//div[@id="content"]/h1/text()').re('《(.*)》')
        item['author'] = response.xpath('//div[@id="content"]/h1/text()').re('：(.*)')
        item['page_url'] = response.xpath('//div[@id="ptop"]/a[4]/@href').extract()
        item['cover'] = response.xpath('//img[@title="点击查看原图"]/@src').extract()
        item['tag'] = response.xpath('//p[@class="date"]//a//text()').extract()
        item['rating'] = response.xpath('//span[@id="moodinfo0"]').extract()
        item['desc'] = response.xpath('//div[@id="content"]//p[3]').extract()
        downloadpage_url = response.xpath(
            '//div[@class="down_2"]/a/@href').extract()[0]
        item['downloadpage_url'] = downloadpage_url
        yield scrapy.Request(downloadpage_url, meta={'item':item},callback=self.parse_down)
        # item['download_node'] = response.xpath('//div[@class="down_2"]/a/@href').extract()
        # item['download_url'] = response.xpath('//div[@class="down_2"]/a/@href').extract()

    def parse_down(self,response):
        item = response.meta['item']
        item['download_node'] = list(map(lambda a,b:a+b, response.xpath(
            '//span[@class="downfile"]/a/text()').extract(), ["TXT", "1_TXT", "2_TXT", "CHM", "CHM"]))
        item['download_url'] = response.xpath(
            '//span[@class="downfile"]/a/@href').extract()
        yield item
