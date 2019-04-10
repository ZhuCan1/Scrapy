# -*- coding: utf-8 -*-
import scrapy
from ..items import BeautyItem
import json

class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['image.so.com']
    url_pattern = 'http://image.so.com/zj?ch=beauty&sn={offset}&listtype=new&temp=1'

    #    start_urls = ['http://image.so.com/']
    def start_requests(self):
        step = 30
        for page in range(0, 1):
            url = self.url_pattern.format(offset=page * step)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        ret = json.loads(response.body)
        for row in ret['list']:
          yield BeautyItem(image_urls=[row['qhimg_url']], name=row['group_title'])