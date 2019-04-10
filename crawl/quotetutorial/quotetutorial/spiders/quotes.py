# -*- coding: utf-8 -*-
import scrapy

from quotetutorial import items


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        # 必须使用.extract()才能提取最终的数据
        for quote in quotes:
            item = items.QuotetutorialItem()
            text = quote.xpath('span[@class="text"]/text()').extract_first()
            author = quote.xpath('span/small[@class="author"]/text()').extract_first()
            tags = quote.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        next = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').extract_first()
        url = response.urljoin(next);
        yield scrapy.Request(url=url, callback=self.parse)
