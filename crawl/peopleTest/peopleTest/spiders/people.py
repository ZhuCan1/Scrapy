# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import PeopleItem
from scrapy import Request
class PeopleSpider(scrapy.Spider):
    name = 'people'
    #allowed_domains = ['word.people.com.cn']
    query_urls = 'http://{type}.people.com.cn/'
    def start_requests(self):
        type = input('请输入新闻类别:(politics,world,tw(台湾),military,leaders,legal,society):')
        yield Request(self.query_urls.format(type=type),callback=self.parse)

    def parse(self, response):
        pattern = 'n1/[^\s]*html'
        link = LinkExtractor(allow=pattern)
        links = link.extract_links(response)
        if links:
            for link_one in links:
                yield Request(url=link_one.url,callback=self.parse_url)

    def parse_url(self, response):
        item = PeopleItem()
        column = response.xpath('//div[@class="box01"]/div[@class="fl"]/a/text()').extract_first()
        type = response.xpath('//div[@class="clearfix w1000_320 path path2 pos_re_search"]/div[@class="fl"]/span[@id="rwb_navpath"]').xpath('string(.)').extract_first()
        author = response.xpath('//div[@class="clearfix w1000_320 text_con"]/div[@class="fl text_con_left"]/div[@class="box_con"]/div[@class="edit clearfix"]/text()').extract_first()
        #记者
        journalist = response.xpath('//div[@class="clearfix w1000_320 text_title"]/p[@class="author"]').xpath('string(.)').extract_first()
        create_time = response.xpath('//div[@class="clearfix w1000_320 text_title"]/div[@class="box01"]/div[@class="fl"]/text()').extract_first()
        if len(create_time.split('\xa0\xa0')):
            create_time = create_time.split('\xa0\xa0')[0]
        title = response.xpath('//div[@class="clearfix w1000_320 text_title"]/h1/text()').extract_first()
        content = response.xpath('//div[@class="clearfix w1000_320 text_con"]/div[@class="fl text_con_left"]/div[@class="box_con"]').xpath('string(.)').extract_first()
         #来源
        item['url'] = response.url
        # 文档来源栏目名称('人民网－人民日报')
        item['column'] = column
        # 文档类型(人民网>>时政>>高层动态)
        item['type'] = type
        # 文档作者或创建者或发布者
        item['author'] = author
        # 文档创建时间
        item['create_time'] = create_time
        # 文档标题
        item['title'] = title
        # 文档链接
        item['file_urls'] = response.url
        # 新闻内容
        item['content'] = content
        yield item





