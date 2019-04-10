# -*- coding: utf-8 -*-
import scrapy
from ..items import FileItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['twistedmatrix.com']
    start_urls = ['https://twistedmatrix.com/documents/current/core/examples/']

    def parse(self, response):
        urls = response.css('a.reference.download.internal::attr(href)').extract()
        for url in urls:
           print(response.urljoin(url))
           item = FileItem()
           item['file_urls'] = [response.urljoin(url)]
           yield item

