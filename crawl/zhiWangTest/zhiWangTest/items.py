# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiwangtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ZhiwangFileItem(scrapy.Item):
    #文档来源网站名称(知网)
    url = scrapy.Field()
    #文档来源栏目名称(机器学习)
    column = scrapy.Field()
    # 文档类型(硕士论文)
    type = scrapy.Field()
    # 文档作者或创建者或发布者
    author = scrapy.Field()
    # 文档创建时间
    create_time = scrapy.Field()
    # 文档标题
    title = scrapy.Field()
    # 相关链接
    href = scrapy.Field()
    # 文档来源栏目技术方向
    techology =scrapy.Field()
    # 特征关键词
    words = scrapy.Field()
    # 文档评论数
    comment_counts = scrapy.Field()
    # 文档转载数
    redict_counts = scrapy.Field()
    # 文档点赞数
    like_counts = scrapy.Field()
    # 文档来源网站技术重要性权重
    weight = scrapy.Field()
    # 文档传播指标
    index = scrapy.Field()
    #文档下载地址
    file_urls = scrapy.Field()
    #文档相关信息
    files = scrapy.Field()
