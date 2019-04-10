# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FiletestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FileItem(scrapy.Item):
    file_urls = scrapy.Field()  #指定文件下载的链接
    files = scrapy.Field()   #文件下载完成后会在里面写相关信息
