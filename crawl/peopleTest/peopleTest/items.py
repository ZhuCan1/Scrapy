# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeopletestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PeopleItem(scrapy.Item):
    #文档来源网站名称(知网)
    url = scrapy.Field()
    #文档来源栏目名称(人民网国际)
    column = scrapy.Field()
    # 文档类型()
    type = scrapy.Field()
    # 文档作者或创建者或发布者
    author = scrapy.Field()
    # 文档创建时间
    create_time = scrapy.Field()
    # 文档标题
    title = scrapy.Field()
    # 相关链接
    href = scrapy.Field()
    # 特征关键词
    words = scrapy.Field()
    #文档链接
    file_urls = scrapy.Field()
    # 新闻内容
    content = scrapy.Field()
